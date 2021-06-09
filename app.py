#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, request, jsonify, send_from_directory, make_response, send_file
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
import pdfplumber
import json
import boto3
from dotenv import load_dotenv
import os
import random


# In[2]:


load_dotenv()


# In[3]:


def getKey(skills, value):
    for key in skills.keys():
        for i in skills[key]:
            if i.lower() == value:
                return key
    return 'None'


# In[4]:


def preprocess(IT_Skills, IT_Skills_Experience):
    ITSkills = ['XCBL', 'IDIT', 'CUDA', 'HTML',  'jQuery', 'Ajax', 'HILS', 'One Note', 'iBATIS', 'Flask', 'Citrix', 'NoSQL', 'SQL', 'ISTQB', 'Andriod Studio', 'Glue', 'Paradox', 'WDS', 'Perl', 'TCPDUMP', 'Java', 'FileNet', 'Putty', 'Eroom', 'HIVE', 'Nexus', 'SAP', 'Ado.net', 'Vsphere', 'Unix', 'PyTest', 'Splunk', 'Mokito', 'Balsamiq', 'Eclipse', 'Hibernate', 'JDBC', 'Tableau', 'Power BI', 'TensorFlow', 'Siebel', 'Solution Architecture', 'CANalyser', 'VB.Net', 'Apache', 'SolarWinds', 'J2SE', 'Netbackup', 'Redis','Salesforce', 'Windows', 'Linux', 'XML', 'JDK', 'TOAD', 'DUKPT', 'Gitlab', 'Webmethods', 'Devops', 'IWS Workspace', 'VHDL', 'Verilog', 'Git', 'SVN', 'VMWARE', 'HYBRIS', 'CISCO Packet Tracer', 'SDN', 'NFV', 'Rest API', 'J2EE', 'Solaris', 'GCP', 'PHP', 'DAC', 'Restful Web Services', 'Jenkins', 'MVC', 'QC', 'CSS', 'Selenium', 'Entity Framework', 'JSON', 'ThingWorx', 'NX', 'Log4j', 'Django', 'GO', 'Python', 'LibreOffice', 'Laravel', 'Active Directory', 'Iconic Framework', 'Docker', 'JSP', 'MeteorJS', 'Keil', 'UCSM',  'Minitab', 'DAQ', 'JPA', 'Ansible', 'Netbeans', 'JIRA', 'Ubuntu', 'Postman', 'Tally', 'Sublime', 'Action Script', 'LINQ', 'AEM', 'Telerik', 'ALM', 'Rally', 'AOP', 'APEX', 'API', 'ARM', 'AUTOSYS', 'ATG', 'AWT', 'Swing', 'AXIS', 'AXURE', 'ActiveMQ', 'Activiti', 'Adobe Analytics', 'Adobe Illustrator', 'Help Desk', 'Aerospike', 'Agilent', 'Aginity', 'Akka', 'Aldon', 'Alexa', 'Altiris', 'Android Studio', 'Aptana', 'Assembly', 'Atmega', 'Aurora', 'Auto Scaling', 'AutoSys', 'SAS', 'BMC', 'RDBMS', 'DBMS', 'Spark', 'DevSecOps', 'Beautiful Soup', 'Map Reduce', 'Blender', 'Block Chain', 'Bizagi', 'Blue Prism', 'CANOE', 'CATIA', 'Cordyd BPM', 'CTM', 'Cypress', 'Camunda', 'Cassandra', 'CloudWatch', 'Cloud Taleo', 'Confluence', 'Cosmos', 'CouchDB', 'Cron', 'Crystal Report', 'Crystal Xcelsius', 'Cucumber', 'DDS', 'DGLUX', 'Drupal', 'DT Studio', 'DOXYGEN', 'Data Director', 'Dell Boomi', 'Delphi', 'Discoverer', 'DocApp', 'Dojo', 'ECMAScript', 'EJB', 'ENOVIA', 'ESXI', 'ETL', 'EXTJS', 'Elastic Load Balancing', 'Flutter', 'Kotlin', 'Force.com', 'Fortify', 'Foundation', 'FreeBSD', 'FreeRTOs', 'Gerrit', 'Groovy', 'Gentran Integration suite', 'Gentran EDI suite', 'Glacier', 'Golden Gate', 'Google Cloud', 'GrayLog', 'Greenplum', 'Guidewire', 'Hana', 'HBASE', 'HUDSON', 'HighChart', 'Hiplink', 'Hortonworks', 'IBM BPM', 'IBM Clear Quest', 'IBM Cognos', 'IBM DB2', 'IBM MQ', 'IBM SPSS Modeler', 'IBM Sterling Integrator', 'IBM-WTX', 'IIS', 'Image Processing', 'IntelliJ', 'Installrite', 'Ionic', 'IOS', 'IOT', 'ITEXT', 'ITX', 'Impala', 'Incident Management', 'Informatica', 'Jasper', 'JBOSS', 'JD Edwards', 'JDeveloper', 'JEE', 'JSF', 'JUnit', 'JWT', 'JaCoCo', 'Design Patterns', 'Kibana', 'Loopback', 'Load Runner', 'Magento', 'MATLAB', 'MERN Stack', 'MEAN Stack', 'MQTT', 'MS Visio',  'Management Studio', 'Microsoft Exchange', 'Middleware', 'Numpy', 'Gunicorn', 'Httpd', 'Nifi', 'Scipy', 'Pandas', 'OAuth', 'OBIEE', 'Networking', 'Oozie', 'OpenCV', 'PEGA PRPC', 'PIG', 'Powershell', 'PeopleSoft', 'Perforce', 'Power Automate', 'PyCharm', 'Data Science', 'Cyclone', 'PyTorch', 'QAC', 'QT Creator', 'RPA', 'Redux', 'Remedy', 'SCALA', 'SCCM', 'SITECORE', 'SLES', 'SSIS', 'STRUTS', 'Zendesk', 'Servlet', 'SOAP', 'SOA', 'Sqoop', 'Swagger', 'Sybase', 'Teamcenter', 'Terraform', 'OATS', 'Toad', 'Tortoise', 'UML', 'VMWare', 'WINSCP', 'Websphere', 'Workbench', 'Gradle', 'iReport', 'Oracle']

    skills = {}
    skills['Scikit-Learn'] = ['Scikit-Learn', 'Scikit Learn', 'Scikit- Learn', 'Sci-kit Learn', 'Sciki Learn']
    skills['MS SQL Server'] = ['MS SQL Server', 'MS SQL-Server', 'MS SQLServer', 'MS-SQL Server', 'SQL Server', 'Microsoft SQL Server']
    skills['MS Office'] = ['MS PowerPoint', 'MS Power Point', 'MS Office', 'M S OFFICE', 'Excel', 'OFFICE365', 'Powerpoint', 'Microsoft Office', 'Word', 'Access', 'MS-Access', 'MS Excel', 'MS.Office', 'Power Point', 'Office 365']
    skills['Google Firebase'] = ['Google Firebase', 'Google Fire Base']
    skills['React JS'] = ['React.js', 'React JS', 'Reactjs', 'React']
    skills['Node JS'] = ['Node JS', 'Node.js', 'Nodejs', 'Node', 'Node-JS']
    skills['Vue JS'] = ['Vue JS', 'Vue.js', 'Vuejs', 'Vue']
    skills['Angular JS'] = ['Angular JS', 'Angular.js', 'Angularjs', 'Angular']
    skills['Express JS'] = ['Express JS', 'Express.js', 'Expressjs', 'Express', 'Express-JS']
    skills['Backbone JS'] = ['Backbone JS', 'Backbone.js', 'Backbonejs', 'Backbone']
    skills['Knockout JS'] = ['Knockout JS', 'Knockout.js', 'Knockoutjs', 'Knockout']
    skills['Next JS'] = ['Next JS', 'Next.js', 'Nextjs', 'Next']
    skills['D3 JS'] = ['D3 JS', 'D3.js', 'D3js', 'D3']
    skills['TyepScript'] = ['TypeScript', 'Type Script']
    skills['MySQL'] = ['MySQL', 'My-SQL', 'My SQL']
    skills['MS SQL'] = ['MSSQL', 'MS-SQL', 'MS SQL', 'MS - SQL']
    skills['React Native'] = ['React Native', 'React-Native']
    skills['SharePoint'] = ['SharePoint', 'Share Point']
    skills['Mobile Application Development'] = ['Mobile Application Development', 'Mobile App Dev', 'Mobile App Development']
    skills['Full Stack Development'] = ['Full Stack Development', 'Full Stack']
    skills['Unit Testing'] = ['Unit Test', 'Unitest']
    skills['Workflow'] = ['WorkFlow', 'Work Flow']
    skills['MongoDB'] = ['MonogDB', 'Mongo DB']
    skills['Spring Framework'] = ['Spring', 'Spring MVC', 'Maven', 'Spring Boot', 'Spring Maven', 'SpringBoot']
    skills['AWS'] = ['AWS', 'Amazon Web Services', 'Amazon Web Service']
    skills['CodeIgniter'] = ['CodeIgniter', 'Code Igniter']
    skills['TIBCO'] = ['TIBCO', 'TIBCO Administrator']
    skills['C++'] = ['C++', 'C ++', 'Cpp']
    skills['Apache Hadoop'] = ['Apache Hadoop', 'Hadoop', 'HDFS']
    skills['Javascript'] = ['Javascript', 'Java Script', 'JS']
    skills['Microsoft Visual Studio'] = ['Visual Studio', 'VS Code', 'VS-Code']
    skills['Microsoft Azure'] = ['Azure']
    skills['GitHub'] = ['Git Hub', 'GitHub']
    skills['Agile Methodolgy'] = ['Agile', 'Scrum']
    skills['Notepad++'] = ['Notepad++', 'Notepad ++']
    skills['.Net'] = ['.Net', 'Dot Net', 'DOTNET', '. Net']
    skills['C#'] = ['C#', 'C #', 'C Sharp']
    skills['C'] = [' C ', '\'C\'']
    skills['R'] = [' R ', '\'R\'', ' R;', 'R-', 'R)']
    skills['VBScript'] = ['VBScript', 'VBS']
    skills['Micro Services'] = ['Micro Services', 'Microservices']
    skills['Microsoft Dynamics'] = ['Microsoft Dynamics', 'MS Dynamics', 'AX', 'Dynamics', 'Navision', 'NAV']
    skills['Artificial Intelligence'] = ['Artificial Intelligence', 'AI']
    skills['Machine Learning'] = ['Machine Learning', 'MachineLearning']
    skills['Qlik'] = ['Qlikview', 'Qlik']
    skills['ASP.NET'] = ['ASP.NET', 'ASP .NET', 'ASP. NET']
    skills['Visual Basic'] = ['Visual Basic', 'VB']
    skills['Atom'] = ['Atom', 'Atomm']
    skills['Ab Initio'] = ['Ab Initio', 'Ab-Initio', 'AbInitio']
    skills['Adobe FrameMaker'] = ['Adobe FrameMaker', 'Adobe Frame Maker', 'FrameMaker', 'Frame Maker']
    skills['Adobe Photoshop'] = ['Adobe Photoshop', 'Photoshop', 'Adobe PS', 'Photo Shop']
    skills['Algorithms'] = ['Algorithm', 'Algorithms']
    skills['Data Structures'] = ['Data Structures', 'Data Structure', 'DS']
    skills['Android Development'] = ['Android Development', 'Android Application Development', 'Android App Development']
    skills['ArborText Epic Editor'] = ['ArborText Epic Editor', 'Arbor Text Epic Editor']
    skills['Autocad'] = ['Autocad', 'Auto cad', 'Auto - cad']
    skills['Apache Tomcat'] = ['Apache Tomcat', 'Tomcat']
    skills['Automation Anywhere'] = ['Automation Anywhere', 'AutomationAnywhere']
    skills['WebLogic'] = ['WebLogic', 'Web Logic']
    skills['Bitbucket'] = ['Bitbucket', 'Bit Bucket', 'Big-buket', 'Bitbuket']
    skills['BASH Shell'] = ['BASH Shell', 'Bash']
    skills['Big Data'] = ['Big Data', 'Big-Data', 'BigData']
    skills['Bootstrap'] = ['Bootstrap', 'Boot Strap']
    skills['Bugzilla'] = ['Bugzilla', 'Bug zilla', 'Bugzila']
    skills['Business Objects'] = ['Business Objects', 'Business Object']
    skills['CentOS'] = ['CentOS', 'Cent OS']
    skills['ClearCase'] = ['ClearCase', 'Clear Case', 'ClearC ase']
    skills['ClearQuest'] = ['ClearQuest', 'Clear Quest']
    skills['ClickUp'] = ['ClickUp', 'Click Up']
    skills['ColdFusion'] = ['ColdFusion', 'Cold Fusion']
    skills['Collection Framework'] = ['Collection Framework', 'Collections Framework']
    skills['Control-M'] = ['Control-M', 'Control - M', 'Control -M', 'ControlM']
    skills['CyberArk'] = ['CyberArk', 'CyberArc', 'Cyber Ark', 'Cyber Arc']
    skills['Data Warehousing'] = ['Data Warehousing', 'Datawarehousing', 'Dataware housing']
    skills['Distributed Systems'] = ['Distributed Systems', 'Distributed System']
    skills['Draw.io'] = ['Draw.io', 'Draw I.O', 'Draw IO', 'Drawio']
    skills['Adobe Dreamweaver'] = ['Dreamweaver', 'Dream Weaver']
    skills['Dynamo DB'] = ['DynamoDB', 'Dynamo DB']
    skills['EditPlus'] = ['EditPlus', 'Edit+', 'Edit Plus']
    skills['Elastic Search'] = ['Elastic Search', 'Elastic Seach', 'ElasticSearch']
    skills['Ehcache'] = ['Ehcache', 'Eh cache']
    skills['GlassFish'] = ['GlassFish', 'Glass Fish']
    skills['HP Quality Center'] = ['HP Quality Center', 'HP Quality Centre', 'Quality Center', 'Quality Centre']
    skills['IBM AIX'] = ['IBM -AIX', 'IBM AIX', 'AIX']
    skills['OOPS'] = ['OOP', 'OOPS', 'OOP\'S', 'Object Oriented Programming', 'Object Orient Programming', 'Object-Oriented Programming']
    skills['Kali Linux'] = ['Kali Linux', 'Kali']
    skills['Kubernetes'] = ['Kubernetes', 'Kubernates', 'Kubernets', 'Kubernities']
    skills['Red Hat Linux'] = ['Red Hat Linux', 'Red Hat', 'RHEL', 'RedHat']
    skills['Micro Services'] = ['Micro Services', 'MicroServices', 'Micro Service', 'Microservice', 'Micro-Service']
    skills['Mainframes'] = ['Mainframe', 'Mainframes']
    skills['Multithreading'] = ['Multithreading', 'Multi-Threading', 'Multi Threading']
    skills['Net Beans'] = ['Net Bean', 'Net Beans', 'Net-Bean', 'NetBean', 'Net-Beans', 'NetBeans']
    skills['NLP'] = ['Natural Language Processing', 'NLP']
    skills['Neural Networks'] = ['Neural Net', 'Neural Network']
    skills['Nginx'] = ['Nginx', 'Nginix']
    skills['Objective C'] = ['Objective C', 'Objective-C', 'ObjectiveC']
    skills['PostgreSQL'] = ['Postgres', 'PostgreSQL', 'Postgre']
    skills['ServiceNow'] = ['ServiceNow', 'Service Now', 'Service-Now', 'Service- Now']
    skills['Socket.IO'] = ['Socket.IO', 'Socket .io', 'SocketIO']
    skills['WildFly'] = ['Wild Fly', 'WildFly']
    skills['IBM DataStage'] = ['DataStage']

    dict_values = []
    for i in skills.keys():
        dict_values.extend(skills[i])

    Overall_Skills = []
    Overall_Skills.extend(ITSkills)
    Overall_Skills.extend(dict_values)

    Overall_Skills = sorted(Overall_Skills, key = len, reverse=True)

    updated_IT_Skills = []
    updated_IT_Skills_Experience = []
    
    size = 0
    for IT_Skill in IT_Skills:
        flag = 0
        skill = IT_Skill.lower()
        for i in Overall_Skills:
            if i.lower() in skill.lower():
                key = getKey(skills, i.lower())
                if key != 'None':
                    updated_IT_Skills.append(key)
                    if len(IT_Skills_Experience) > 0:
                        updated_IT_Skills_Experience.append(IT_Skills_Experience[size])
                else:
                    updated_IT_Skills.append(i)
                    if len(IT_Skills_Experience) > 0:
                        updated_IT_Skills_Experience.append(IT_Skills_Experience[size])
                flag = 1
                skill = skill.replace(i.lower(),'')
            if len(skill) == 0:
                break
        if flag == 0:
            updated_IT_Skills.append(IT_Skill)
            if len(IT_Skills_Experience) > 0:
                updated_IT_Skills_Experience.append(IT_Skills_Experience[size])
        size += 1
    return updated_IT_Skills,updated_IT_Skills_Experience


# In[6]:


def recommend_jobs(input_resume):
    # Recommend Job Requirements for a given resume
    # job_data = pd.read_csv('Jobs.csv', low_memory=False)
    job_data = pd.read_csv('Job Requirements.csv')
    key_skills = job_data['Key Skills'].tolist()
    it_skills = job_data['IT Skills'].tolist()
    for i in range(len(key_skills)):
        if isinstance(key_skills[i],float):
            key_skills[i] = ''
        if isinstance(it_skills[i],float):
            it_skills[i] = ''
    job_data['Key Skills'] = key_skills
    job_data['IT Skills'] = it_skills

    IT_Skills = [x.lower() for x in input_resume['IT Skills'].tolist()[0].split(',')]
    IT_Skills_Experience = []
    if input_resume['IT Skills Experience'].tolist()[0] != 'None':
        IT_Skills_Experience = [float(x) for x in input_resume['IT Skills Experience'].tolist()[0].split(',')]
    Key_Skills = [x.lower() for x in input_resume['Key Skills'].tolist()[0].split(',')]

    resume_experience = input_resume['Total Experience'].tolist()[0].strip().split(' ')
    experience_years = 0
    experience_months = 0
    if 'Year(s)' in resume_experience:
        experience_years = resume_experience[resume_experience.index('Year(s)') - 1]
    if 'Month(s)' in resume_experience:
        experience_months = resume_experience[resume_experience.index('Month(s)') - 1]
    resume_experience = float(str(experience_years)+"."+str(experience_months))

    Total_Score = []
    for num in range(5090):
        score = 0
        job = job_data.iloc[[num]]

        job_experience = job['Experience'].tolist()[0].replace('years','').strip()

        if '-' in job_experience:
            job_experience_lower = int(job_experience.split(' ')[0].strip())
            job_experience_upper = int(job_experience.split(' ')[2].strip())
        else:
            job_experience_lower = job_experience_upper = int(job_experience.strip())

        if job_experience_lower == job_experience_upper and job_experience_lower > resume_experience:
            Total_Score.append(score)
            continue

        if job_experience_lower != job_experience_upper and (resume_experience < job_experience_lower or resume_experience > job_experience_upper):
            Total_Score.append(score)
            continue  

        Job_IT_Skills = [x.lower() for x in job['IT Skills'].tolist()[0].split(',')]
        Job_Key_Skills = [x.lower() for x in job['Key Skills'].tolist()[0].split(',')]

        for i in range(len(IT_Skills)):
            if IT_Skills[i] in Job_IT_Skills:
                score = score + (IT_Skills_Experience[i] * 1 + 5) * (Job_IT_Skills.count(IT_Skills[i]))
        for i in range(len(Key_Skills)):
            if Key_Skills[i] in Job_Key_Skills:
                score = score + 1
        Total_Score.append(score)
    # print(Total_Score)
    output = np.argsort(np.array(Total_Score))[::-1]
    # input_resume.to_csv('Input(Resume).csv')
    return job_data.iloc[output[0:10]]


# In[7]:


def matched_skills(input_resume,job_data):
    IT_Skills = [x.lower() for x in input_resume['IT Skills'].tolist()[0].split(',')]
    IT_Skills_U = input_resume['IT Skills'].tolist()[0].split(',')
    # IT_Skills_Experience = [float(x) for x in input_resume['IT Skills Experience'].tolist()[0].split(',')]
    Key_Skills = [x.lower() for x in input_resume['Key Skills'].tolist()[0].split(',')]
    Key_Skills_U = input_resume['Key Skills'].tolist()[0].split(',')

    matched_skills = []
    for num in range(10):
        sample_set = set()
        job = job_data.iloc[[num]]
        
        Job_IT_Skills = [x.lower() for x in job['IT Skills'].tolist()[0].split(',')]
        Job_Key_Skills = [x.lower() for x in job['Key Skills'].tolist()[0].split(',')]
        Job_IT_Skills_U = job['IT Skills'].tolist()[0].split(',')
        Job_Key_Skills_U = job['Key Skills'].tolist()[0].split(',')

        for i in range(len(IT_Skills)):
            if IT_Skills[i] in Job_IT_Skills:
                sample_set.add(IT_Skills_U[i])
                sample_set.add(Job_IT_Skills_U[Job_IT_Skills.index(IT_Skills[i])])
        for i in range(len(Key_Skills)):
            if Key_Skills[i] in Job_Key_Skills:
                sample_set.add(Key_Skills_U[i])
                sample_set.add(Job_Key_Skills_U[Job_Key_Skills.index(Key_Skills[i])])
        matched_skills.append(list(sample_set))
    return matched_skills


# In[8]:


def getResumeText(file):
    cols = ['Current Location', 'Preferred Location', 'Functional Area', 'Industry', 'Total Experience', 'Highest Degree', 'UG', 'PG', 'Category', 'Job Type', 'Employment Status', 'Physically Challenged', 'Key Skills', 'Name', 'Role', 'Summary', 'IT Skills', 'IT Skills Experience','Languages Known', 'Work Experience', 'Resume']
    df = pd.DataFrame(columns = cols)

    resume = {}

    with pdfplumber.open(file) as pdf:
        data = ""
        for page in pdf.pages:
            data = data + page.extract_text()

    data = data.split('\n')

    data = [i for i in data if i and i != ' ' and 'naukri' not in i]

    size = 0

    resume['Name'] = data[0].strip()

    for i in data:
        #Current Location -- Total Experience; Current Designation -- Total Experience
        #Preferred Location -- Highest Degree; Current Location -- Highest Degree
        #Current Company -- Highest Degree;
        if i[0:16] == 'Current Location':
            if 'Total Experience' not in resume and 'Total Experience:' in i:
                index = i.find('Total Experience')
                current_location = i[0:index]
                total_experience = i[index:]
                temp = current_location.split(':')
                resume['Current Location'] = temp[1].strip()
                temp = total_experience.split(':')
                resume['Total Experience'] = temp[1].strip()
            elif 'Highest Degree' not in resume and 'Highest Degree:' in i:
                index = i.find('Highest Degree')
                current_location = i[0:index]
                highest_degree = i[index:]
                temp = current_location.split(':')
                resume['Current Location'] = temp[1].strip()
                temp = highest_degree.split(':')
                resume['Highest Degree'] = temp[1].strip()

        if i[0:14] == 'Pref. Location':
            if 'Highest Degree' not in resume and 'Highest Degree:' in i:
                index = i.find('Highest Degree')
                preferred_location = i[0:index]
                highest_degree = i[index:]
                temp = preferred_location.split(':')
                resume['Preferred Location'] = temp[1].strip()
                temp = highest_degree.split(':')
                resume['Highest Degree'] = temp[1].strip()
            else:
                temp = i.split(':')
                resume['Preferred Location'] = temp[1].strip()
        
        if i[0:19] == 'Current Designation' and 'Total Experience' in i and 'Total Experience' not in resume:
            index = i.find('Total Experience')
            total_experience = i[index:]
            temp = total_experience.split(':')
            resume['Total Experience'] = temp[1].strip()
        
        if i[0:15] == 'Current Company' and 'Highest Degree' in i and 'Highest Degree' not in resume:
            index = i.find('Highest Degree')
            total_experience = i[index:]
            temp = total_experience.split(':')
            resume['Highest Degree'] = temp[1].strip()

        if i[0:15] == 'Functional Area':
            temp = i.split(':')
            value = temp[1].strip()
            temp_size = size + 1
            while data[temp_size][0:5] != 'Role:':
                value += ' ' + data[temp_size]
                temp_size += 1
            resume['Functional Area'] = value.strip()


        if i[0:9] == 'Industry:':
            temp = i.split(':')
            resume['Industry'] = temp[1].strip()

        if i[0:3] == 'UG:':
            temp = i.split(':')
            value = temp[1].strip()
            temp_size = size+1
            while data[temp_size][0:2] != 'PG' and data[temp_size] != 'IT Skills':
                value += ' '+data[temp_size]
                temp_size += 1
            resume['UG'] = value

        if i[0:3] == 'PG:':
            temp = i.split(':')
            resume['PG'] = temp[1].strip()

        #Category -- Job Type; Physically Challenged -- Employment Status
        #Physically Challenged -- Job Type
        #Employment Status
        #Job Type
        # if i[0:9] == 'Category:':
        #     index = i.find('Job Type')
        #     category = i[0:index]
        #     job_type = i[index:]
        #     temp = category.split(':')
        #     resume['Category'] = temp[1].strip()
        #     temp = job_type.split(':')
        #     resume['Job Type'] = temp[1].strip()

        # if i[0:22] == 'Physically Challenged:':
        #     index = i.find('Employment Status')
        #     physically_challenged = i[0:index]
        #     employment_status = i[index:]
        #     temp = physically_challenged.split(':')
        #     resume['Physically Challenged'] = temp[1].strip()
        #     temp = employment_status.split(':')
        #     resume['Employment Status'] = temp[1].strip()

        if i[0:11] == 'Key Skills:':
            temp_size = size+1
            value = i.split(':')[1].strip()+','
            while data[temp_size][0:10] != 'Verified :' and data[temp_size][0:12] != 'Last Active:' and data[temp_size][0:7] != 'Summary':
                value += data[temp_size]+","
                temp_size += 1
            value = value.strip()[0:-1]
            if value[-1] == ',' or value[-1] == '.':
                value = value[0:-1]
            key_skills_list = value.split(',')
            for skill in range(len(key_skills_list)):
                key_skills_list[skill] = key_skills_list[skill].strip()
            resume['Key Skills'] = (',').join(key_skills_list)

        if i[0:5] == 'Role:':
            temp = i.split(':')
            resume['Role'] = temp[1].strip()

        if i[0:7] == 'Summary':
            value = ''
            temp_size = size+1
            while data[temp_size] != 'Work Experience':
                value += data[temp_size].strip()+' '
                temp_size += 1
            resume['Summary'] = value.strip()

        if i[0:9] == 'IT Skills':
            IT_Skills = []
            IT_Skills_Experience = []
            temp_size = size+2
            while temp_size < len(data) and data[temp_size] != 'Languages Known':
                value = data[temp_size].strip()
                temp_list = [g.strip() for g in value.split(',')]
                experience = 0
                last_element = temp_list[-1]
                years = 0
                months = 0
                last_skill = ''
                last_element_list = last_element.split(' ')
                for j in range(len(last_element_list)):
                    if last_element_list[j] == 'Year(s)':
                        years = int(last_element_list[j-1])
                    if last_element_list[j] == 'Month(s)':
                        months = int(last_element_list[j-1])
                for j in range(len(temp_list)-1):
                    IT_Skills.append(temp_list[j].strip())
                for j in last_element_list:
                    try:
                        number = int(j)
                        break
                    except:
                        last_skill += j+' '
                count = len(temp_list)-1
                if len(last_skill) > 0:
                    IT_Skills.append(last_skill.strip())
                    count += 1
                for j in range(count):
                    IT_Skills_Experience.append(str(years)+'.'+str(months))
                temp_size += 1

            resume['IT Skills'] = (',').join(IT_Skills)
            resume['IT Skills Experience'] = (',').join(IT_Skills_Experience)

        if i[0:15] == 'Languages Known':
            value = ''
            temp_size = size+2
            while temp_size < len(data) and data[temp_size][0:18] != 'Affirmative Action':
                value += data[temp_size].strip()+', '
                temp_size += 1
            resume['Languages Known'] = value.strip()[0:-1]
        
        if i[0:15] == 'Work Experience':
            temp_size = size+1
            value = ''
            while (data[temp_size][0:9] != 'Education'):
                value += data[temp_size]+" "
                temp_size += 1
            value = value.strip()
            resume['Work Experience'] = value

        size += 1

    if 'PG' not in resume:
        resume['PG'] = 'None'

    if 'Languages Known' not in resume:
        resume['Languages Known'] = 'None'
    
    for j in cols:
        if j not in resume:
            resume[j] = 'None'
    
    updated_IT_Skills,updated_IT_Skills_Experience = preprocess(resume['IT Skills'].split(','),resume['IT Skills Experience'].split(','))
    resume['IT Skills'] = ",".join(updated_IT_Skills) #Logic change
    resume['IT Skills Experience'] = ",".join(updated_IT_Skills_Experience)
    df = df.append(resume, ignore_index = True)
    output = recommend_jobs(df)
    matchedSkills = matched_skills(df, output)
    output = output[['Job Title', 'Company', 'Experience', 'Salary', 'Location', 'Job Description', 'Industry Type', 'Functional Area', 'Role Category', 'Key Skills', 'Link']].reset_index()
    output = output.to_dict()
    output['Matched Skills'] = matchedSkills
    return output
    # df.to_csv('Resume.csv', index = False)


# In[9]:


def addITSkills(df):
    resume_data = pd.read_csv('Resume Data.csv')

    IT_Skills = set()

    for i in range(1,31):
        for skill in resume_data['IT Skill ' + str(i)]:
            if not isinstance(skill, float):
                try:
                    skill = float(skill)
                except:
                    if len(skill) > 2:
                        IT_Skills.add(skill)

    IT_Skills = list(IT_Skills)
    IT_Skills = sorted(IT_Skills, key=len, reverse=True)

    Job_IT_Skills = []
    description = df['Job Description'].tolist()[0]
    for skill in IT_Skills:
        if skill.lower() in description.lower():
            Job_IT_Skills.append(skill)
            description = description.replace(skill.lower(), '')
    
    df['IT Skills'] = ','.join(Job_IT_Skills)
    return df


# In[10]:


def recommend_resumes(df):
    # Recommend Resumes for a given Job Requirement
    input_job = df
    IT_Skills = [x.lower() for x in input_job['IT Skills'].tolist()[0].split(',')]
    # IT_Skills_Experience = [float(x) for x in input_job['IT Skills Experience'].tolist()[0].split(',')]
    Key_Skills = [x.lower() for x in input_job['Key Skills'].tolist()[0].split(',')]

    resume_data = pd.read_csv('Resume Data.csv')

    job_experience = input_job['Experience'].tolist()[0].replace('years','').strip()

    if '-' in job_experience:
        job_experience_lower = int(job_experience.split(' ')[0].strip())
        job_experience_upper = int(job_experience.split(' ')[2].strip())
    else:
        job_experience_lower = job_experience_upper = int(job_experience.strip())

    # print(job_experience_lower,job_experience_upper)

    Total_Score = []
    for num in range(4626):
        score = 0
        resume = resume_data.iloc[[num]]
        
        resume_experience = 0
        if resume['Total Experience'].tolist()[0] != 'None':
            resume_experience = float(resume['Total Experience'].tolist()[0].strip())

        if job_experience_lower == job_experience_upper and job_experience_lower > resume_experience:
            Total_Score.append(score)
            continue

        if job_experience_lower != job_experience_upper and (resume_experience < job_experience_lower or resume_experience > job_experience_upper):
            Total_Score.append(score)
            continue

        Resume_IT_Skills = []
        if isinstance(resume['IT Skills'].tolist()[0],str):
            Resume_IT_Skills = [x.lower() for x in resume['IT Skills'].tolist()[0].split(',')]
    
        IT_Skills_Experience = [float(x) for x in resume['IT Skills Experience'].tolist()[0].split(',')]
        Resume_Key_Skills = [x.lower() for x in resume['Key Skills'].tolist()[0].split(',')]

        for i in range(len(Resume_IT_Skills)):
            if Resume_IT_Skills[i] in IT_Skills:
                score = score + (IT_Skills_Experience[i] * 1 + 5)
        for i in range(len(Key_Skills)):
            if Key_Skills[i] in Resume_Key_Skills:
                score = score + 1
        score = score + resume_experience
        Total_Score.append(score)
    # print(Total_Score)
    output = np.argsort(np.array(Total_Score))[::-1]
    # input_job.to_csv('Input(Job).csv')
    return resume_data.iloc[output[0:10]]


# In[11]:


def getJobText(file):
    data = json.load(file)
    columns = data.keys()
    data['Key Skills'] = ','.join(data['Key Skills'])
    df = pd.DataFrame(columns=columns)
    df = df.append(data, ignore_index=True)
    df = addITSkills(df)
    output = recommend_resumes(df)
    matchedSkills = matched_skills(df, output)
    files = ["http://localhost:5000/getResume/Resume"+str(x+1)+".pdf" for x in list(output.index)]
    out = {}
    # with open('./Resumes/Resume1.pdf') as f:
    #     out['Resume'] = io.BytesIO(f.read())
    out['data'] = data
    out['Files'] = files
    out['Matched Skills'] = matchedSkills
    return out


# In[12]:


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# In[13]:


@app.route('/')
@cross_origin()
def start():
    return "Server is Up and Running"


# In[14]:


@app.route('/jobRecommendation', methods=['POST'])
@cross_origin()
def getResumeFile():
    # print(request.files)
    file = request.files['File']
    # print("Reached")
    response = getResumeText(file)
    return jsonify(response)


# In[15]:


@app.route('/resumeRecommendation', methods=['POST'])
@cross_origin()
def getJobFile():
    # print(request.files)
    file = request.files['File']
    # print("Reached")
    response = getJobText(file)
    return jsonify(response)


# In[17]:


@app.route('/getResume/<resume_filename>', methods=['GET'])
@cross_origin()
def getResume(resume_filename):
    try:
        s3 = boto3.resource(service_name='s3',region_name='us-east-2',aws_access_key_id=os.getenv('aws_access_key_id'),aws_secret_access_key=os.getenv('aws_secret_access_key'))
        s3.Bucket('recommendation-system-1').download_file(Filename='Resume.pdf',Key=resume_filename)
        return send_file('Resume.pdf')
    except FileNotFoundError:
        return "Something went wrong"


# In[18]:
@app.route('/sampleResume', methods=['POST','GET'])
@cross_origin()
def sampleResume():
    arr = [1,2,5,7,11,12,18,21,30,44]
    resume_filename = 'Resume'+str(arr[random.randint(1,10)-1])+'.pdf'
    try:
        s3 = boto3.resource(service_name='s3',region_name='us-east-2',aws_access_key_id=os.getenv('aws_access_key_id'),aws_secret_access_key=os.getenv('aws_secret_access_key'))
        s3.Bucket('recommendation-system-1').download_file(Filename='Resume.pdf',Key=resume_filename)
        return send_file('Resume.pdf')
    except FileNotFoundError:
        return "Something went wrong"


@app.route('/sampleJob', methods=['POST','GET'])
@cross_origin()
def sampleJob():
    job_filename = str(random.randint(1,10))+'.json'
    try:
        s3 = boto3.resource(service_name='s3',region_name='us-east-2',aws_access_key_id=os.getenv('aws_access_key_id'),aws_secret_access_key=os.getenv('aws_secret_access_key'))
        s3.Bucket('recommendation-system-1').download_file(Filename='Job.json',Key=job_filename)
        return send_file('Job.json')
    except FileNotFoundError:
        return "Something went wrong"

@app.route('/resumeForm', methods=['POST'])
@cross_origin()
def resumeForm():
    # try:
        data = request.get_json()
        
        data['IT_Skills'] = ','.join([x.strip() for x in data['IT_Skills'].split(',')])

        IT_Skills = []
        IT_Skills_Experience = []

        for element in data['IT_Skills'].split(','):
            index1 = element.index('(')
            # index2 = element.index(')')
            IT_Skills.append(element[0:index1])
            exp = element[index1+1:].split(' ')
            experience_years = 0
            experience_months = 0
            if 'year(s)' in exp:
                experience_years = exp[exp.index('year(s)') - 1]
            if 'month(s)' in exp:
                experience_months = exp[exp.index('month(s)') - 1]
            exp = str(experience_years)+"."+str(experience_months)
            IT_Skills_Experience.append(exp)
        
        data['IT_Skills'] = ",".join(IT_Skills)

        cols = ['Current Location', 'Preferred Location', 'Functional Area', 'Industry', 'Total Experience', 'Highest Degree', 'UG', 'PG', 'Category', 'Job Type', 'Employment Status', 'Physically Challenged', 'Key Skills', 'Name', 'Role', 'Summary', 'IT Skills', 'IT Skills Experience','Languages Known', 'Work Experience', 'Resume']
        df = pd.DataFrame(columns = cols)

        resume = {}

        resume['Current Location'] = data['location']
        resume['Preferred Location'] = resume['Functional Area'] = resume['Industry'] = 'None'
        resume['Total Experience'] = data['experience']
        resume['Highest Degree'] = 'None'
        resume['UG'] = data['ug']
        resume['PG'] = data['pg']
        resume['Category'] = resume['Job Type'] = resume['Employment Status'] = resume['Physically Challenged'] = resume['Key Skills'] = resume['Resume'] = 'None'
        resume['Name'] = data['name']
        resume['Role'] = data['role']
        resume['IT Skills Experience'] = ','.join(IT_Skills_Experience)
        resume['Summary'] = data['summary']
        resume['Work Experience'] = data['workExperience']
        resume['IT Skills'] = data['IT_Skills']
        resume['Languages Known'] = data['languages']
        
        updated_IT_Skills,updated_IT_Skills_Experience = preprocess(resume['IT Skills'].split(','),resume['IT Skills Experience'].split(','))
        resume['IT Skills'] = ",".join(updated_IT_Skills) #Logic change
        resume['IT Skills Experience'] = ",".join(updated_IT_Skills_Experience)
        
        df = df.append(resume, ignore_index = True)
        output = recommend_jobs(df)
        matchedSkills = matched_skills(df, output)
        output = output[['Job Title', 'Company', 'Experience', 'Salary', 'Location', 'Job Description', 'Industry Type', 'Functional Area', 'Role Category', 'Key Skills', 'Link']].reset_index()
        output = output.to_dict()
        output['Matched Skills'] = matchedSkills
        return output
    # except Exception as e:
    #     print(e)
    #     return "Something went wrong! Check the format of the resume form and try again"

@app.route('/jobForm', methods=['POST'])
@cross_origin()
def jobForm():
    # try:
        data = request.get_json()
        original = data.copy()

        data['IT_Skills'] = ','.join([x.strip() for x in data['IT_Skills'].split(',')])
        data['location'] = ','.join([x.strip() for x in data['location'].split(',')])

        columns = ['Job Title', 'Company', 'Experience', 'Salary', 'Location', 'Job Description', 'Link', 'Role', 'Industry Type', 'Functional Area', 'Employment', 'Role Category', 'UG', 'PG', 'Doctorate', 'Key Skills']

        job = {}

        job['Job Title'] = data['title']
        job['Company'] = data['company']
        job['Experience'] = data['experience']
        job['Salary'] = data['salary'].lower()
        job['Location'] = data['location']
        job['Job Description'] = data['job_description']
        job['Link'] = job['Industry Type'] = job['Functional Area'] = job['Employment'] = job['Role Category'] = 'None'
        job['UG'] = data['ug']
        job['PG'] = data['pg']
        job['Doctorate'] = data['doctorate']
        job['Key Skills'] = ",".join(preprocess(data['IT_Skills'].split(','),[])[0])

        df = pd.DataFrame(columns=columns)
        df = df.append(job, ignore_index=True)
        df = addITSkills(df)
        output = recommend_resumes(df)
        matchedSkills = matched_skills(df, output)
        files = ["http://localhost:5000/getResume/Resume"+str(x+1)+".pdf" for x in list(output.index)]
        out = {}
        # with open('./Resumes/Resume1.pdf') as f:
        #     out['Resume'] = io.BytesIO(f.read())
        out['data'] = {"Job Title":original["title"],"Company":original['company'],"Location":original['location'],"Email":original['email'],'Role':original['role'],'Experience':original['experience'],"Salary":original['salary'],"UG":original['ug'],"PG":original['pg'],"Doctorate":original['doctorate'],"IT Skills":original['IT_Skills'],"Job Description":original['job_description']}
        out['Files'] = files
        out['Matched Skills'] = matchedSkills
        return out


if __name__ == "__main__":
  app.run(debug=True, use_reloader=True)


# In[ ]:




