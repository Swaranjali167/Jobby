# from bs4 import BeautifulSoup
# import requests
# import re
# import helper
# import traceback


# def get_jobs(role, location, no_jobs, allskills):
#     URL = "http://www.indeed.com/jobs?q="
#     for string in role.split():
#         URL = URL + string + "+"
#     URL = URL + "&l=" + location

#     page = requests.get(URL)
#     if page.status_code != 200:
#         print(URL)
#         print("Connection Failed")
#     soup = BeautifulSoup(page.text, "html.parser")
#     # print(soup.encode("utf-8"))

#     results = soup.find_all('a', attrs={'class': re.compile('tapItem fs-unmask result job_.*')})
#     urls = []
#     for result in results:
#         # print(result['href'])
#         if(result['href'][0:8] == '/rc/clk?'):
#             urls.append("https://www.indeed.com/viewjob?" + result['href'][8:])
#         elif result['href'][0:8] == '/pagead/':
#             urls.append("https://www.indeed.com" + result['href'])
#         elif result['href'][0:8] == '/company':
#             urls.append("https://www.indeed.com" + result['href'])

#     jobtitles = soup.find_all('div', attrs={'class': 'heading4 color-text-primary singleLineTitle tapItem-gutter'})
#     for i in range(len(jobtitles)):
#         if(jobtitles[i] is None):
#             jobtitles[i] = jobtitles[i].find('span', attrs={'title': re.compile('.*')}).string

#     companynames = soup.find_all('span', attrs={'class': 'companyName'})

#     jobskills = []
#     for url in urls:
#         urlpage = requests.get(url)
#         bsresult = BeautifulSoup(urlpage.text, "html.parser")
#         descwrap = bsresult.find('div', attrs={'class': 'jobsearch-jobDescriptionText'})
#         jobskills.append(helper.extract_skills(str(descwrap), allskills))

#     jobs = []
#     try:
#         for i in range(len(urls)):
#             job = {}
#             job["title"] = jobtitles[i].string
#             if job['title'] is None:
#                 job['title'] = role
#             job["url"] = urls[i]
#             job["company"] = companynames[i].string
#             job["skills"] = jobskills[i]
#             jobs.append(job)
#     except Exception:
#         traceback.print_exc()
#     return jobs

# role = "software engineer"
# location = "New York"
# no_of_jobs_to_retrieve = 5
# all_skills = ["python", "java", "javascript"]

# result = get_jobs(role, location, no_of_jobs_to_retrieve, all_skills)
# print(result)

from bs4 import BeautifulSoup
import requests
import re
import helper
import traceback


def build_indeed_url(role, location):
    base_url = "https://www.indeed.com/jobs?q="
    role_params = "+".join(role.split())
    location_param = f"&l={location}"
    return f"{base_url}{role_params}{location_param}"


def extract_job_urls(soup):
    results = soup.find_all('a', class_=re.compile(r'tapItem fs-unmask result job_.*'))
    urls = []
    for result in results:
        href = result['href']
        if href.startswith('/rc/clk?'):
            urls.append(f"https://www.indeed.com/viewjob?{href[8:]}")
        elif href.startswith('/pagead/'):
            urls.append(f"https://www.indeed.com{href}")
        elif href.startswith('/company'):
            urls.append(f"https://www.indeed.com{href}")
    return urls


def extract_job_titles(soup):
    job_titles = soup.find_all('div', class_='heading4 color-text-primary singleLineTitle tapItem-gutter')
    return [title.get_text(strip=True) if title else None for title in job_titles]


def extract_company_names(soup):
    company_names = soup.find_all('span', class_='companyName')
    return [name.get_text(strip=True) for name in company_names]


def extract_job_skills(url, all_skills):
    url_page = requests.get(url)
    bs_result = BeautifulSoup(url_page.text, "html.parser")
    desc_wrap = bs_result.find('div', class_='jobsearch-jobDescriptionText')
    return helper.extract_skills(str(desc_wrap), all_skills)


def get_indeed_jobs(role, location, no_jobs, all_skills):
    try:
        url = build_indeed_url(role, location)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6"}

        page = requests.get(url,headers=headers)
        page.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(page.text, "html.parser")
        
        urls = extract_job_urls(soup)
        titles = extract_job_titles(soup)
        companies = extract_company_names(soup)
        skills = [extract_job_skills(url, all_skills) for url in urls]

        jobs = []
        for title, company, skill, url in zip(titles, companies, skills, urls):
            job = {
                "title": title or role,
                "company": company,
                "skills": skill,
                "url": url,
            }
            jobs.append(job)
            if len(jobs) >= no_jobs:
                break

        return jobs

    except requests.RequestException as e:
        print(f"Request Failed: {e}")
        return []


# Example usage
# role = "software engineer"
# location = "New York"
# no_of_jobs_to_retrieve = 5
# all_skills = ["python", "java", "javascript"]

# result = get_indeed_jobs(role, location, no_of_jobs_to_retrieve, all_skills)
# print(result)
