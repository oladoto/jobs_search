import requests
import bs4
import sqlite3
from jobs_search.data_manager import DataManager
import datetime
import csv
from datetime import datetime


class JobSearch:

    def __init__(self):

        self.cover_letters = {}

        self.conn = None
        self.comm = None
        self.job_id_dict = {}
        self.jobs_dict = []

    # this is active
    def get_complete_indeed(self, url, source, contract_type):

        self.open_database()

        count_contract = 0
        count_temp = 0
        next_page = None
        self.job_id_dict.clear()

        min_salary = '30,000'
        proximity = 30

        page_counter = 0
        num_pages = 0
        links = None
        # for k, contract_type in contract_types.items():
        for i, target_location in DataManager.target_locations.items():
            for k, role in DataManager.roles.items():
                if next_page is None:
                    c_location = target_location
                    next_page = '{}?q={}&l={}&jt={}'.format(url, role.replace('-', '+'),
                                                            target_location.replace('-', '+'),
                                                            contract_type.replace('-', ''))

                while next_page is not None:
                    soup = self.get_soup(next_page)
                    if soup is None:
                        break

                    job_list = soup.select('body > table > tr > td > table > tr > td > .result')
                    # titles = soup.select('body > table > tr > td > table > tr > td > .result > .title > a')
                    locations = soup.select('body > table > tr > td > table > tr > td > .result > .sjcl > span')
                    salaries = soup.select(
                        'body > table > tr > td > table > tr > td > .result > div > .salary > .salaryText')
                    summaries = soup.select('body > table > tr > td > table > tr > td > .result > .sjcl > summary')

                    next_page = None
                    if links is None:
                        links = soup.select('body > table > tr > td > table > tr > td > .pagination > a')
                        if len(links) > 0:
                            num_pages = len(links)
                            next_page = links[0].get('href')
                    else:
                        if page_counter < (num_pages - 1):
                            page_counter += 1
                            next_page = links[page_counter].get('href')

                    # for k in titles:
                    #     print('{} - {}'.format(k.getText(), k.get('href')))
                    # for k in locations:
                    #     print(k.get_text())

                    counter = -1
                    failure_stage = 0
                    for job in job_list:

                        try:
                            counter += 1
                            s_title = job.div.a.get_text()
                            if self.not_valid_title(s_title):
                                continue
                            failure_stage += 1
                            job_link = 'https://www.indeed.co.uk'
                            job_link = '{}{}'.format(job_link, job.div.a.get('href'))
                            salary = salaries[counter].get_text()  # job.div.span
                            failure_stage += 1
                            _type = contract_type.replace('-', '')
                            job_id = job.get('id')
                            failure_stage += 1

                            # if _type == 'flexible':
                            #     _type = 'Undetected'
                            self.insert(job_id, s_title, _type, salary, c_location, job_link[:600], source)
                            failure_stage += 1
                        except:
                            print('Error encountered...')

                    print('\nResults Position: {}, found: {}'.format(k, counter + 1))
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    print("\nTime =", current_time)


    def get_linkedin(self):
        # https://www.linkedin.com/jobs/search/?alertAction=viewjobs&f_TPR=a1574517660-&geoId=104116710&keywords=android%20developer&savedSearchId=593867474&searchAlertRefId=99bd2aa3-630b-417c-b7dd-165b2113191e
        print('linked...')

    # this is active
    def get_indeed(self, contract_type):
        url = 'https://www.indeed.co.uk/jobs?q=android+developer&l=Manchester'
        url = 'https://www.indeed.co.uk/jobs?q=android+developer&l=Manchester'
        # https://www.indeed.co.uk/jobs?q=android+developer&l=Manchester&ts=1575718339705&rq=1&rsIdx=0&fromage=last&newcount=6
        # https: // www.indeed.co.uk / jobs?q = solution + analyst & l = london & jt = contract
        # https: // www.indeed.co.uk / jobs?q = android + % C2 % A330, 000 & l = Manchester

        url = DataManager.job_sites['indeed']
        source = 'indeed'
        self.get_complete_indeed(url, source, contract_type)

    # this is active
    def get_jobsite(self, contract_type):
        url = 'https://www.jobsite.co.uk/jobs/unity-developer/in-manchester?radius=30'
        url = 'https://www.jobsite.co.uk/jobs/solution-architect/in-manchester?radius=20&s=header'

        # url = DataManager.job_sites['totaljobs']
        url = DataManager.job_sites['jobsite']
        source = 'jobsite'
        self.get_jobs(url, source, contract_type)

    # this is active
    def get_total_jobs(self, contract_type):
        # sample
        # https://www.totaljobs.com/jobs/part-time/android-developer/in-manchester?radius=30

        url = DataManager.job_sites['totaljobs']
        source = 'totaljobs'
        self.get_jobs(url, source, contract_type)

    # this is active
    def get_cwjobs(self, contract_type):
        # https://www.cwjobs.co.uk/jobs/android-developer/in-manchester?radius=30&salary=400&salarytypeid=4
        # https://www.cwjobs.co.uk/job/contract-developer/hotfoot-recruitment-job88727988               - single job

        url = DataManager.job_sites['cwjobs']
        source = 'cwjobs'
        self.get_jobs(url, source, contract_type)

    def get_reed(self, contract_type):
        # https://www.reed.co.uk/jobs/solution-architect-jobs-in-manchester-airport?proximity=30
        # https://www.reed.co.uk/jobs/solution-architect-jobs-in-manchester-airport?salaryfrom=38000&contract=True&proximity=30

        url = DataManager.job_sites['reed']
        source = 'reed'
        self.open_database()

        count_contract = 0
        count_temp = 0
        next_page = None
        self.job_id_dict.clear()
        min_salary = 30000
        # contract_type = DataManager.contract_types['contract']
        proximity = 30

        for i, target_location in DataManager.target_locations.items():

            for k, role in DataManager.roles.items():
                if next_page is None:
                    relative = role + '-jobs-in-' + target_location
                    relative += '?salaryfrom=' + str(min_salary)
                    relative += '&' + contract_type + '=True'
                    relative += '&proximity=' + str(proximity)

                    c_location = target_location

                    next_page = '{}{}'.format(url, relative)

                while next_page is not None:

                    soup = self.get_soup(next_page)
                    if soup is None:
                        break

                    table = soup.select('body > div > table > tbody > tr > .result')

                    titles = soup.select('.row > div > .job > .row > div > .job-title > a > h2')
                    title_ids = soup.select('.row > div > .job')
                    links = soup.select('.row > div > .job > .row > div > .job-title > a')
                    salaries = soup.select(
                        '.row > div > .job > .row > div > .detail-body > .row > div > .header-list > .salary')
                    locations = soup.select(
                        '.row > div > .job > .row > div > .detail-body > .row > div > .header-list > .location > span > a')
                    types = soup.select(
                        '.row > div > .job > .row > div > .detail-body > .row > div > .detail-list > .job-type > span')
                    # descriptions = soup.select('.container > div > .row > .job-content-top > div > .row > div > .job-description')
                    organisations = soup.select(
                        '.row > div > .job > .row > div > .detail-body > .row > div > .detail-list > .company > h3 > a')

                    next_page = None
                    head_links = soup.select('head > link')
                    for i, n in enumerate(head_links):
                        nk = n.get('rel')[0]
                        if nk == 'next':
                            next_page = n.get('href')
                            break

                    counter = -1
                    for title in titles:
                        counter += 1
                        s_title = self.padd(title)
                        #if self.not_valid_title(s_title):
                        #    continue
                        title_id = title_ids[counter]
                        salary = salaries[counter]
                        _type = types[counter]
                        # location = locations[counter]
                        # organisation = organisations[counter]
                        link = ''
                        if len(links) >= counter:
                            link = links[counter].get('href')

                        # Insert a row of data
                        _id = title_id.get('id')
                        self.insert(title_id.get('id'), s_title, self.padd(_type), self.padd(salary),
                                    c_location, link, source)

                    # print('\nRole: {}\nJob ID: {}\nType: {}\nSalary: {}\n'.format(self.padd(title), title_id.get('id'), self.padd(_type), self.padd(salary)))

                    print('\nResults Position: {}, found: {}'.format(k, counter + 1))

    # this is active
    def get_jobs(self, url, source, contract_type):
        self.open_database()

        count_contract = 0
        count_temp = 0
        next_page = None
        self.job_id_dict.clear()
        url_file = open('files/url_logs.csv', 'a+')

        self.jobs_dict.clear()

        # contract_type = self.contract_types['part_time']

        for i, target_location in DataManager.target_locations.items():
            for k, role in DataManager.roles.items():
                if next_page is None:
                    # relative = self.contract_types['part_time'] + '/'              # comment out role if enabling part-time/flexible
                    relative = contract_type + '/'
                    relative += role + '/'
                    relative += 'in-' + target_location
                    relative += '?radius=30'
                    if contract_type == 'permanent':
                        relative += '&salary=50000'  # minimum salary
                        relative += '&salarytypeid=1'  # daily
                    else:
                        relative += '&salary=200'  # minimum salary
                        relative += '&salarytypeid=4'  # daily
                    # relative += '&s=header'

                    # c_location = target_location

                    next_page = '{}{}'.format(url, relative)

                while next_page is not None:
                    url_file.write('\n{}'.format(next_page))
                    print(next_page)
                    soup = self.get_soup(next_page)
                    if soup is None:
                        continue

                    titles = soup.select('.row > div > .job > .row > div > .job-title > a > h2')
                    title_ids = soup.select('.row > div > .job')
                    links = soup.select('.row > div > .job > .row > div > .job-title > a')
                    salaries = soup.select(
                        '.row > div > .job > .row > div > .detail-body > .row > div > .header-list > .salary')
                    locations = soup.select(
                        '.row > div > .job > .row > div > .detail-body > .row > div > .header-list > .location > span > a')
                    types = soup.select(
                        '.row > div > .job > .row > div > .detail-body > .row > div > .detail-list > .job-type > span')
                    # descriptions = soup.select('.container > div > .row > .job-content-top > div > .row > div > .job-description')
                    organisations = soup.select(
                        '.row > div > .job > .row > div > .detail-body > .row > div > .detail-list > .company > h3 > a')

                    next_page = None
                    head_links = soup.select('head > link')
                    for i, n in enumerate(head_links):
                        nk = n.get('rel')[0]
                        if nk == 'next':
                            next_page = n.get('href')
                            break

                    try:
                        counter = -1
                        for title in titles:
                            counter += 1
                            s_title = self.padd(title)
                            if self.not_valid_title(s_title):
                                continue

                            # s_title = s_title.replace("'", " ")
                            """
                            for k, v in self.exclude_titles.items():
                                if s_title.find(v) != -1:
                                    continue
                            """
                            title_id = title_ids[counter]
                            salary = salaries[counter]
                            if len(types) >= counter:
                                _type = types[counter]
                            else:
                                _type = ''
                            # location = locations[counter]
                            # organisation = organisations[counter]
                            link = ''
                            if len(links) >= counter:
                                link = links[counter].get('href')

                            # Insert a row of data
                            _id = title_id.get('id')
                            self.insert(title_id.get('id'), s_title, self.padd(_type), self.padd(salary),
                                        target_location, link, source)
                            """
                            self.jobs_dict.append({
                                'job_code': title_id.get('id'),
                                'title': s_title,
                                'contract': self.padd(_type),
                                'salary': self.padd(salary),
                                'location': target_location,
                                'link': link,
                                'source': source
                            })
                            """
                    except:
                        print("An exception occurred")

                    print('\nResults Position: {}, found: {}'.format(k, counter + 1))
        # self.clean_database()
        # self.send_to_cloud()
        self.close_database()
        url_file.close
        print('\nContracts: {}   Temp: {}'.format(count_contract, count_temp))

    def padd(self, pad):
        s_pad = pad.getText().strip()
        s_r = s_pad.replace("'", "")
        return s_r

    def send_to_cloud(self):

        if len(self.jobs_dict) > 0:
            job_upload_url = 'https://codestrain.com/api/jobsch/insert_jobs_api.php'
            data = self.jobs_dict
            headers = {'Content-Type': 'application/json'}
            response = requests.post(job_upload_url, params={'data': data}, headers=headers)
            response.raise_for_status()
            self.jobs_dict.clear()
            print(response.text)

    def get_soup(self, url):

        soup = None
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, features='html.parser')  # 'lxml')
        except:
            print('Url retrieval failed...')
        return soup

    def open_database(self):

        self.conn = sqlite3.connect('jobs_db.db')
        self.comm = self.conn.cursor()

    def clear_database(self):
        self.open_database()

        query = "DELETE FROM Jobs"
        self.comm.execute(query)

        self.conn.commit()
        self.close_database()

    def insert(self, job_id, title, _type, salary, location, link, source):
        self.job_id_dict.update({job_id: job_id})
        query = "Select * from Jobs where job_code='" + job_id + "'"
        self.comm.execute(query)
        rows = self.comm.fetchall()
        count = len(rows)

        file = '../files/logs.csv'
        if count <= 0:
            query = "INSERT INTO Jobs(job_code, job_title, type_, salary, location, link, source, seen) "
            query += "VALUES('" + job_id + "','" + title.strip() + "','" + _type + "','" + salary + "','" + location + "','" + link + "','" + source + "', 0)"
            self.comm.execute(query)

            # query = "INSERT INTO Jobs(job_code, job_title, type_, salary, location, link_, source_, seen) "
            # query += "VALUES('" + job_id + "','" + title.strip() + "','" + _type + "','" + salary + "','" + location + "','" + link + "','" + source + "', 0);"

            output = open('../files/logs.csv', 'a+')
            output.write('\n')
            output.write(query)
            output.close()

        self.conn.commit()
        return

    def not_valid_title(self, title):
        not_valid = False
        for i, e in enumerate(DataManager.delete_terms):
            if title.find(DataManager.delete_terms[i]) > 0:
                not_valid = True
                break
        return not_valid

    def clean_database(self):
        self.open_database()

        output = open('files/delete_queries.csv', 'a+')
        query = "Delete from Jobs where TRIM(job_title) like '' OR job_title like 'NULL';"
        self.comm.execute(query)

        for i, v in enumerate(DataManager.delete_terms):
            query = "Delete from Jobs where job_title like '%{}%'".format(v)
            self.comm.execute(query)
            output.write(query + ';\n')

        output.close()
        self.conn.commit()
        self.close_database()

    def close_database(self):
        self.conn.close()

    def process_jobs_search(self):

        output = open('files/logs.csv', 'w+')
        # output.write(str(datetime.datetime.now()))
        output.close()
        output = open('files/url_logs.csv', 'w+')
        output.close()
        output = open('./files/delete_queries.csv', 'w+')
        output.close()

        print(datetime.now())
        for k, v in DataManager.contract_types.items():
            self.get_jobsite(v)
            self.get_total_jobs(v)
            self.get_cwjobs(v)
            self.get_indeed(v)
            # self.get_reed()

        self.clean_database()
        print(datetime.datetime.now())

    def read_employer_csv(self):
        with open('../perm_jobs_process/data_files/tier4_sponsors_original.csv', newline='') as csvfile:
            ...
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        ...
        for row in spamreader:
            ...
            print(', '.join(row))

    def send_to_cloud_new(self):

        # Clear jobs data
        job_upload_url = 'https://codestrain.com/api/jobsch/delete_jobs.php'
        requests.get(job_upload_url)  # , headers=headers)

        self.conn = sqlite3.connect('jobs_db.db')
        self.comm = self.conn.cursor()

        # def insert(self, job_id, title, _type, salary, location, link, source):

        query = "Select id, job_code, job_title, type_, salary, location, link, source, retrieval from Jobs"
        self.comm.execute(query)
        rows = self.comm.fetchall()
        job_upload_url = 'https://codestrain.com/api/jobsch/insert_jobs.php'
        headers = {'Content-Type': 'application/json'}
        print('Uploading data...')

        total_jobs = len(rows)
        for row in rows:
            print(row[2])
            data = {
                "job_code": row[1],
                "job_title": row[2],
                "type_": row[3],
                "salary": row[4],
                "location": row[5],
                "link": row[6],
                "source": row[7]
            }

            feedback = requests.post(job_upload_url, params=data)  # , headers=headers)

        self.conn.close()

        data = {"feature": "jobs_count", "score": total_jobs}
        job_upload_url = 'https://codestrain.com/api/jobsch/update_analytics.php'
        feedback = requests.post(job_upload_url, params=data)

        print('Data Uploaded...')


class CoverLetters:

    def __init__(self):
        self.start_string = "Dear Sir/Madam,\n\nPlease find attached my application for your consideration.\n"
        self.end_string = "\nI do look forward to hearing from you.\n\nYours faithfully\nOladotun Omosebi"
        self.cover_letters = {
            "0": self.start_string + "I believe that with my wide experience with wide experience in systems design and mobile application development, I could bring a lot to the task at hand. Even though my level of experience with Kotlin, though growing, could be below the requisite level, I can state that my pickup and execution would not in any way impact the timelines of the project. " + self.end_string,
            "1": self.start_string + " have had a great deal of experience in Android development, including using other methods and integration with various cloud options. I believe that given the opportunity, I can bring my wide experience, adaptive learning approach, and personal agitation for designing and developing effective systems and solutions, to bear on the goal of the project. " + self.end_string,
            "2": self.start_string + " have had a great deal of experience in Android and iOS native development, with integration with various cloud and non-cloud backends. I have also had extensive experience in systems analysis and design while managing several disconnected teams to implement a solution based on a written technical design document. I believe that these, and various other personal capabilities can be brought to bear on the project in order to achieve the most optimized solutions under the given timelines." + self.end_string,
            "2": self.start_string + " I believe that I would qualify as an excellent candidate for this position as I have extensive experience in Unity development, C++ and some integration with GIS. Beyond using Unity for a few games published on the app store, I recently worked on developing an AR/ GIS app using Vuforia and Google Maps respectively. I have also worked on Cesium, Harp.gl and Google Maps GIS tools to implement a web/mobile-friendly terrain browsable app. In addition, I have done some extensive C++ programming in the last one and half years within my research developing simulations in NS3 and Ubuntu. I do believe that these, combined with my adaptability for learning new technologies, very much qualify for this role." + self.end_string,
            "2": self.start_string + " Please find attached my application for your consideration. I believe I qualify as an excellent candidate for this vacancy. I have had extensive experience in HTML, CSS, and JavaScript under various frameworks. I also have the conviction that my extensive stint in solution design would enable me to contribute immensely to be able to manage both current and new solutions." + self.end_string,
            "3": self.start_string + "" + self.end_string
        }
