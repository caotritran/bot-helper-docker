import argparse
from unittest import result
from jenkinsapi.jenkins import Jenkins
import re, sys, os

_result = []
host = sys.argv[1]
api_token = os.environ.get('JENKINS_API_TOKEN')

def jenkins_vhost(_result):

    jenkins_url = 'http://jenkins.sweb.vn'
    username = 'admin'

    jenkins = Jenkins(jenkins_url, username=username, password=api_token)

    job_name = 'sweb/Create_vhost'
    job = jenkins.get_job(job_name)

    builds = job.get_build_dict()

    with open("jenkins_results.txt", "w") as f:
        for build_number in sorted(builds.keys(), reverse=True):
            build = job.get_build(build_number)
            if build.get_status() == 'SUCCESS':
                f.write(str(build.get_status) + '\n')
        f.close()

    with open("jenkins_results.txt", "r") as f:
        for line in f:
            text = line.strip()
            match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b\s-\s(.+)$', text)
            if match is None:
                continue
            domain = match.group(1)[:-2]
            ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)[0]
            if ips is None:
                continue
            #print(domain, ips)
            try:
                if ips == host:
                    _result.append(domain)
                    #_result += domain + '\n'
                    #print(domain + " - " + ips)
                else:
                    continue
            except:
                continue
        f.close()
    return _result

def jenkins_allinone(_result):
    jenkins_url = 'http://jenkins.sweb.vn'
    username = 'admin'

    jenkins = Jenkins(jenkins_url, username=username, password=api_token)

    job_name = 'sweb/One_Click_In_All'
    job = jenkins.get_job(job_name)

    builds = job.get_build_dict()

    with open("jenkins_results_2.txt", "w") as f:
        for build_number in sorted(builds.keys(), reverse=True):
            build = job.get_build(build_number)
            if build.get_status() == 'SUCCESS':
                f.write(str(build.get_status) + '\n')
        f.close()

    with open("jenkins_results_2.txt", "r") as f:
        for line in f:
            text = line.strip()
            parts = text.split("- ")

            ips = parts[1].strip()
            domain = parts[-2].strip()
            if ips is None:
                continue
            if domain is None:
                continue
            #print(domain, ips)
            try:
                if ips == host:
                    _result.append(domain)
                    #print(domain + " - " + ips)
                else:
                    continue
            except:
                continue
        f.close()
    return _result

if __name__ == "__main__":
    latest_result = []
    latest_result = jenkins_vhost(latest_result)
    latest_result = jenkins_allinone(latest_result)
    unique_latest_result = list(set(latest_result))
    for domain in unique_latest_result:
        print(domain)
    os.remove("jenkins_results.txt")
    os.remove("jenkins_results_2.txt")
    