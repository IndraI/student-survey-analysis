from bs4 import BeautifulSoup
import __future__

import requests

import os
from selenium import webdriver


def download_files(files, prefix_="", cookies=""):
    headers = {}
    for url, name in files.items():
        print(url)
        print(name)
        file = open(name + ".pdf", 'wb')
        response = requests.get(prefix_ + url, headers=headers, cookies=cookies)
        file.write(response.content)
        print(name + ": Completed")
        file.close()


driver = webdriver.Chrome()

year = "1516"
## Agrupats per Ensenyament
driver.get("https://www.ub.edu/avdoc/visado/visa_documents.jsp?codiEnse=G1077&curs=" + year)
prefix = "https://www.ub.edu/avdoc/visado/"
input("After login, press return")

# enquestes = BeautifulSoup(driver.page_source,'html.parser')
# urls = {}
# for link in enquestes.find_all('a'):
#     href = link.get('href')
#     if href is not None and "visa_visiona.jsp?uidFitxer=" in href:
#
#         try:
#             name_file = urls[href] +"_" + link.string
#         except KeyError:
#             name_file = link.string
#         urls[href] = name_file
#
# cookies_list = driver.get_cookies()
# cookies_dict = {}
# for cookie in cookies_list:
#     cookies_dict[cookie['name']] = cookie['value']
# download_files(urls,prefix,cookies_dict)


## Professors
driver.get("https://www.ub.edu/avdoc/visado/professor.jsp")
professors_html = BeautifulSoup(driver.page_source,'html.parser')
professors = {}
for link in professors_html.find_all('a'):
    href = link.get('href')
    if href is not None and "visa_documents.jsp?codiProf=" in href:
        try:
            name_file = professors[href] +"_" + link.string
        except KeyError:
            name_file = link.string.replace(",","")
        professors[href] = name_file

for url, professor in professors.items():
    driver.get(prefix+url)
    assignatures_html = BeautifulSoup(driver.page_source,'html.parser')
    assignatures= {}
    for link in assignatures_html.find_all('a'):
        href = link.get('href')
        if href is not None and "visa_visiona.jsp?uidFitxer=" in href:
            try:
                name_file = assignatures[href] +"_" + link.string
            except KeyError:
                name_file = professor+"_"+link.string
            assignatures[href] = name_file
    cookies_list = driver.get_cookies()
    cookies_dict = {}
    for cookie in cookies_list:
        cookies_dict[cookie['name']] = cookie['value']
    download_files(assignatures,prefix,cookies_dict)


## Assignatures
# driver.get("https://www.ub.edu/avdoc/visado/assignatura.jsp")
# assignatures_html = BeautifulSoup(driver.page_source, 'html.parser')
# assignatures = {}
# for link in assignatures_html.find_all('a'):
#     href = link.get('href')
#     if href is not None and "visa_documents.jsp?codiAssig=" in href:
#         try:
#             name_file = assignatures[href] + "_" + link.string
#         except KeyError:
#             name_file = link.string.replace(",", "")
#         assignatures[href] = name_file
#
# for url, assignatura in assignatures.items():
#     driver.get(prefix + url)
#     grups_html = BeautifulSoup(driver.page_source, 'html.parser')
#     grups = {}
#     for link in grups_html.find_all('a'):
#         href = link.get('href')
#         if href is not None and "visa_visiona.jsp?uidFitxer=" in href:
#             try:
#                 name_file = grups[href] + "_" + link.string
#             except KeyError:
#                 name_file = link.string
#             grups[href] = name_file
#     cookies_list = driver.get_cookies()
#     cookies_dict = {}
#     for cookie in cookies_list:
#         cookies_dict[cookie['name']] = cookie['value']
#     download_files(grups, prefix, cookies_dict)
