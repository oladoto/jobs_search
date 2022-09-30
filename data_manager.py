

class DataManager:

    job_sites = {
        'cwjobs': 'https://www.cwjobs.co.uk/jobs/',
        'totaljobs': 'https://www.totaljobs.com/jobs/',
        'indeed': 'https://www.indeed.co.uk/jobs/',
        'jobserve': 'https://www.jobserve.com/',
        'ziprecruiter': 'https://www.ziprecruiter.co.uk/',
        # jobs/search?utf8=%E2%9C%93&q=Android&l=Manchester%2C+UK&lat=53.48095&long=-2.23743&d=
        'reed': 'https://www.reed.co.uk/jobs/',
        'linkedin': 'https://www.linkedin.com/jobs/',
        'jobsite': 'https://www.jobsite.co.uk/jobs/',
        'hirehub': 'https://www.hirehub.io/',
        'neuvoo': 'https://neuvoo.co.uk/jobs/'
        # 'jobozio': 'https://jobozio.com/jobs'
    }

    target_locations = {
        'warrington': 'warrington',
        'liverpool': 'liverpool',
        'lancashire': 'lancashire',
        'preston': 'preston',
        'lancaster': 'lancaster',
        'chester': 'chester',
        'bolton': 'bolton',
        'blackburn': 'blackburn',
        'halifax': 'halifax',
        'nottingham': 'nottingham',
        'wigan': 'wigan',
        'bristol': 'bristol',
        'manchester': 'manchester',
        'manchester_airport': 'manchester-airport',
        'northwich': 'northwich',
        'middlesbrough': 'middlesbrough',
        'shrewsbury': 'shrewsbury',
        'manchester_industrial-centre': 'manchester-industrial-centre_manchester',
        'leeds': 'leeds',
        'birmingham': 'birmingham',
        'stoke-on-trent': 'stoke-on-trent',
        'coventry': 'coventry',
        'yorkshire': 'yorkshire',
        'sheffield': 'sheffield',
        'rochdale': 'rochdale',
        'london': 'london',
        'huddersfield': 'huddersfield',
        'london_heathrow_airport': 'london-heathrow-airport',
        'bradford': 'bradford',
        'salford': 'salford',
    }
    # simply copied from the url and pasted in value of each dictionary component, key replaces dash with underscore for easy use in code
    roles_original = {
        'solution_architect': 'solution-architect',
        'senior_solution_architect': 'senior-solution-architect',
        'solution_architect_developer': 'solution-architect-developer',
        'business_analyst': 'business-analyst',
        'solution_analyst': 'solution-analyst',
        'systems_design': 'systems-design',
        'senior_developer_java': 'senior-developer-java',
        'software_developer': 'software-developer',
        'software_engineer': 'software-engineer',
        'ios_developer': 'ios-developer',
        'android': 'android',
        'android_developer': 'android-developer',
        'java_developer': 'java-developer',
        'java': 'java',
        'c#_developer': 'c#-developer',
        'net_developer': 'net-developer',
        'net_architect': 'net-architect',
        'mobile_developer': 'mobile-developer',
        'mobile_application': 'mobile-application',
        'front_end_developer': 'front-end-developer',
        'javascript': 'javascript',
        'javascript_developer': 'javascript-developer',
        'customer_service': 'customer-service',
        'customer_service_personnel': 'customer-service-personnel',
        'customer advisor': 'customer-advisor',
        'customer assistant': 'customer-assistant',
        'customer manager': 'customer-manager',
        'call center': 'call-center',
        'administrative_officer': 'administrative-officer',
        'clerk': 'clerk',
        'parcel_sorter': 'parcel-sorter',
        'store_assistant': 'store-assistant',
        'post_office': 'post-office'
    }
    roles = {
        'data_visualization': 'data-visualization',
        'data_analytics': 'data-analytics',
        'data_analyst': 'data-analyst',
        'systems_design': 'systems-design',
        'systems_design_engineer': 'systems-design-engineer',
        'solution_architect': 'solution-architect',
        'business_analyst': 'business-analyst',
        'software_developer': 'software-developer',
        'c#_developer': 'c#-developer',
        'net_developer': '.net-developer',
        'net_architect': 'net-architect',
        'mobile_developer': 'mobile-developer',
        'mobile_application': 'mobile-application',
        'customer_service': 'customer-service',
        'customer_service_personnel': 'customer-service-personnel',
        'customer advisor': 'customer-advisor',
        'customer assistant': 'customer-assistant',
        'customer manager': 'customer-manager',
        'call center': 'call-center',
        'administrative_officer': 'administrative-officer',
        'clerk': 'clerk',
        'php': 'php',
        'parcel_sorter': 'parcel-sorter',
        'store_assistant': 'store-assistant',
        'post_office': 'post-office',
        'kotlin': 'kotlin',
        'kotlin_developer': 'kotlin-developer',
        'games_developer': 'games-developer',
        'python': 'python',
        'unity': 'unity',
        'web_developer': 'web-developer',
        'python_developer': 'python-developer',
        'java_developer': 'java-developer'
    }
    """
        'java_coach': 'java-coach',
        'python': 'python',
        'web_developer': 'web-developer',
        'python_developer': 'python-developer',
        'aws_engineer': 'aws-engineer',
        'aws_architect': 'aws-architect',
        'azure_engineer': 'azure-engineer',
        'azure_architect': 'azure-architect',
        'php': 'php',
        'ios': 'ios',
        
        'google_cloud': 'google-cloud',
        'devops_engineer': 'devops-engineer',
        'devops_architect': 'devops-architect',
        'three_js': 'threejs',
        'three_js': 'three-js',
        'blockchain': 'blockchain',
        'enterprise_architect': 'enterprise-architect',
        'network_administrator': 'network-administrator',
        'system_networking': 'system-networking',
        'network_engineer': 'network-engineer',
        'network_design': 'network -design',
        'wordpress_developer': 'wordpress-developer',
        'wordpress_admin': 'wordpress-admin',
        'wordpress_plugin': 'wordpress-plugin',
        'hardware_analysis': 'hardware-analysis',
        'software_analysis': 'software-analysis',
        'hardware_maintenance': 'hardware-maintenance',
        'software_maintenance': 'software-maintenance'
    }
    """

    # contract_types = {'permanent': 'permanent'}
    contract_types = {'contract': 'contract', 'temporary': 'temporary', 'temp': 'temp', 'flexible': 'flexible', 'part_time': 'part-time', 'part': 'part'}
    # contract_types = {'part_time': 'part-time', }
    # contract_types = {'part_time': 'part-time', 'temporary': 'temporary', 'flexible': 'flexible'}

    delete_terms = [
        'Driver',
        'Mechanical',
        'LGV Cat',
        'Civil',
        'Agricultural',
        'Agriculture',
        'Warehouse Operatives',
        'Orthodontist',
        'Therapist',
        'Merchandiser',
        'Repair Engineer',
        'Legal',
        'TacCIS Systems',
        'HGV Class',
        'Electrician',
        'Mobile Merchandiser',
        'Repair Engineer',
        'Bookkeeper',
        'Incubator',
        'Cosmetics',
        'Controller',
        'Spare Parts',
        'Technician',
        'Community',
        'Cleaner',
        'Electrical',
        'Director',
        'Buildings',
        'Arranger',
        'Surveyor',
        'Machinist',
        'Turner',
        'Setter',
        'Miller',
        'Radiographer',
        'Worker',
        'Sonographer',
        'Coach',
        'Supply',
        'Executive',
        'Mechanical',
        'Representative',
        'Practitioner',
        'Registered',
        'Therapy',
        'Orthodontist',
        'Cisco',
        'Network',
        'Workshop',
        'Safety',
        'Infrastructure',
        'CAD Designer',
        'Agents',
        'Mechanical',
        'Marshall',
        'Investigator',
        'Opportunity',
        'Distributors',
        'Construction',
    ]

    delete_terms2 = [
        'Retail Food Sampler',
        'Registered Nurse',
        'Sales',
        'Teacher',
        'Assistant',
        'Mechanical',
        'Civil',
        'Agricultural',
        'Agriculture',
        'Warehouse Operatives',
        'Administrator',
        'Orthodontist',
        'Office Manager',
        'Manager',
        'Nurse',
        'Therapist',
        'Merchandiser',
        'Service Desk Analyst',
        'Analyst - Operations',
        'Repair Engineer',
        'Legal',
        'TacCIS Systems',
        'HGV Class',
        'Electrician',
        'Mobile Merchandiser',
        'Repair Engineer',
        'Trainee',
        'Bookkeeper',
        'Incubator',
        'Cosmetics',
        'Controller',
        'Assistant',
        'spare parts',
        'Technician',
        'Carer',
        'Care Assistant',
        'Head of Finance',
        'Officer',
        'Invigilator',
        'Community',
        'Cleaner',
        'Advisor',
        'AVON',
        'Warehouse',
        'Staff',
        'Learning',
        'Apprenticeship',
        'Electrical',
        'SAP',
        'Administrator',
        'Director',
        'Buildings',
        'Arranger',
        'Surveyor',
        'Operator',
        'Customer Service',
        'Machinist',
        'Turner',
        'Operative',
        'Setter',
        'Miller',
        'Supervisor',
        'Radiographer',
        'Worker',
        'Sonographer',
        'Coach',
        'Supply',
        'Executive',
        'Mechanical',
        'Representative',
        'Practitioner',
        'Registered',
        'Nurse',
        'Customer',
        'Beauty',
        'Therapy',
        'Assistant',
        'Orthodontist',
        'Cisco',
        'Network',
        'Workshop',
        'Safety',
        'Infrastructure',
        'CAD Designer',
        'Agents',
        'Accountant',
        'Mechanical',
        'Consultant',
        'Accounts',
        'Coordinator',
        'Reception',
        'Marketing',
        'Grocery',
        'Marshall',
        'Customer Support',
        'Investigator',
        'Opportunity',
        'Distributors',
        'Paid Research',
        'Construction',
        'Call Triage',
        'Worker',
    ]