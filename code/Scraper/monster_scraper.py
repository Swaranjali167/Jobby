# import json
# import traceback
# import requests
# import helper


# def get_jobs(role, location, no_of_jobs_to_retrieve, all_skills):
#     url = "https://appsapi.monster.io/jobs-svx-service/v2/monster/search-jobs/samsearch/en-US?apikey=ulBrClvGP6BGnOopklreIIPentd101O2"
#     payload = "{\"jobQuery\":{\"query\":\"" + role + "\",\"locations\":[{\"country\":\"us\",\"address\":\"" + location + "\",\"radius\":{\"unit\":\"mi\",\"value\":20}}]},\"jobAdsRequest\":{\"position\":[1,2,3,4,5,6,7,8,9],\"placement\":{\"component\":\"JSR_SPLIT_VIEW\",\"appName\":\"monster\"}},\"fingerprintId\":\"de72842ced49bea0d5d7f4d75a74002c\",\"offset\":0,\"pageSize\":9,\"includeJobs\":[]}head"
#     headers = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json; charset=utf-8',
#         'Origin': 'https://www.monster.com',
#         'Content-Length': '338',
#         'Accept-Language': 'en-us',
#         'Host': 'appsapi.monster.io',
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
#         'Referer': 'https://www.monster.com/',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Connection': 'keep-alive',
#         'request-starttime': '1637812719632'
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)
#     jobs_response = {}
#     if response.status_code != 200:
#         print("Connection Failed!")
#         print("-------------------------------------")
#         #print("Monster API ResponseCode:" + str(response.status_code) + ", ErrorMessage: " + response.text)
#         #jobs_response['totalSize'] = 0
#     else:
#         jobs_response = json.loads(response.text)
#         jobs = []
#         job_details = {}
#         try:
#             for i in range(int(jobs_response['totalSize'])):
#                 job_data = jobs_response['jobResults'][i]["normalizedJobPosting"]
#                 if no_of_jobs_to_retrieve > 0:
#                     job = {}
#                     job["title"] = job_data['title']
#                     job["url"] = job_data['url']
#                     job_details[job["url"]] = [job["title"], ""]
#                     no_of_jobs_to_retrieve -= 1
#                     str3 = job_data['description']
#                     job["skills"] = helper.extract_skills(str3, all_skills)
#                 jobs.append(job)
#         except Exception:
#             traceback.print_exc()

#         return jobs


# role = "software engineer"
# location = "New York"
# no_of_jobs_to_retrieve = 5
# all_skills = ["python", "java", "javascript"]

# result = get_jobs(role, location, no_of_jobs_to_retrieve, all_skills)
# print(result)

import requests
from bs4 import BeautifulSoup

def get_jobs(role, location, no_of_jobs_to_retrieve, all_skills):
    url = f'https://www.monster.com/jobs/search/?q={role}&where={location}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        jobs = []

        for job_card in soup.find_all('li',class_='sc-blKGMR etPslv'):
            #'div', class_='sc-bSiGmx LCGfq'):
            #'section', attrs={'data-jobid': True}):
            
            print(job_card)
            job_title = job_card.find_all('li',class_='sc-blKGMR etPslv')
            print(job_title)
            # aria_label = job_card.get('aria-label')
            # print(aria_label)
            job_url = job_title.find('a')['href'] if job_title and job_title.find('a') else None

            if job_url:
                job = {
                    'title': job_title.text.strip() if job_title else '',
                    'url': job_url,
                }
                jobs.append(job)

                if no_of_jobs_to_retrieve > 0:
                    no_of_jobs_to_retrieve -= 1
                else:
                    break

        return jobs
    else:
        print(f"Connection Failed with status code {response.status_code}")
        return []

# Example usage
# role = "Software"
# location = "NewYork"
# no_of_jobs_to_retrieve = 5

# result = get_monster_jobs(role, location, no_of_jobs_to_retrieve)
# print(result)
