from jobs_search.job_search import *


class Main:

    def __init__(self):
        jobSearch = JobSearch()
        jobSearch.clear_database()
        jobSearch.process_jobs_search()
        # jobSearch.send_to_cloud_new()

main = Main()