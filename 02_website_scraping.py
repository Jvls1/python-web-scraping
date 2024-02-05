import time
from bs4 import BeautifulSoup
import requests

def get_unfamiliar_skills():
  unfamiliar_skills = []
  while True:
    unfamiliar_skill = input('Put some skills that you are not familiar with (type "exit" to stop): ')
    if unfamiliar_skill.lower() == 'exit':
        break
    unfamiliar_skills.append(unfamiliar_skill)
    print(f'Filtering out {unfamiliar_skill}')
  print(f'Unfamiliar skills list: {unfamiliar_skills}')
  return unfamiliar_skills

def scrape_and_save_jobs(unfamiliar_skills):
  try:
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    list_size = len(jobs)
    print(f"The size of the list is: {list_size}")

    for index, job in enumerate(jobs):
      published_date = job.find('span', class_='sim-posted').span.text
      if 'few' not in published_date:
        continue
      
      skills = job.find('span', class_='srp-skills').text.replace(' ', '')
      unfamiliar_skill_found = any(unfamiliar_skill in skills for unfamiliar_skill in unfamiliar_skills)

      if unfamiliar_skill_found:
        continue

      company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '')
      more_info = job.header.h2.a['href']

      with open(f'posts/{index}.txt', 'w') as file:
        file.write(f'Company name: {company_name.strip()} \n')
        file.write(f'Required skills: {skills.strip()} \n')
        file.write(f'More info: {more_info}')

      print(f'File saved: {index}')

  except Exception as e:
    print(f"An error occurred: {e}")

if __name__ == '__main__':
  unfamiliar_skills = get_unfamiliar_skills()

  while True:
    scrape_and_save_jobs(unfamiliar_skills)
    time_wait = 10
    print(f'Waiting {time_wait} minutes...')
    time.sleep(time_wait * 60)
