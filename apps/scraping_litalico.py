
from time import sleep
from bs4 import BeautifulSoup
import requests
import csv
import datetime
import re

from chrome_soup import Bs_chrome

def exception_handling(content):
    try:
        result = content.string
    
    except:
        result = ''
        
    finally:
        return result

#DB接続
#db = ConnectDB('list','litalico')

#url
bsc = Bs_chrome('https://snabi.jp')

job_list = []

try:
    for page in range(37):
        if (page != 30):
            continue
        #パース
        soup = bsc.parser('/recruitments/prefecture-13?page='+str(page + 1))
        # print(soup)

        obj_url_list = soup.select('div.css-0 > a[href]')

        for i, ou in enumerate(obj_url_list):
            if i > 19:
                break

            sub_url = ou.get('href')
            #print(sub_url)
            
            id = re.sub(r"\D", "", sub_url)
            print(page+1,i, id)
            
            soup = bsc.parser(sub_url)
            company_name = exception_handling(soup.select_one('div.css-oc1vt3 > p'))
            job_description = exception_handling(soup.select_one('div.css-s2khqy > p'))
            income = exception_handling(soup.select_one('div.css-1ko99kf > p'))
            requirements = exception_handling(soup.select_one('div.css-vtn2l4 > div > p'))
            occupation1 = exception_handling(soup.select_one('p.chakra-text.css-0'))
            occupation2 = exception_handling(soup.select_one('p.chakra-text.css-1yni2gr'))
            industry = exception_handling(soup.select_one('div.css-19jcx03 > div > p'))
            pref = exception_handling(soup.select_one('p.chakra-text.css-1qm1lh'))
            address = exception_handling(soup.select_one('div.chakra-stack.css-1q2z04w > p:nth-child(3)'))
            commute = exception_handling(soup.select_one('div.chakra-stack.css-1q2z04w > p:nth-child(4)'))
            remarks = exception_handling(soup.select_one('div.css-19jcx03 > div > div:nth-child(1) > p'))
            e_stat = exception_handling(soup.select_one('div > div.chakra-stack.css-17930he > div:nth-child(9) > div.css-19jcx03 > div > p.chakra-text.css-0'))

            #print(id, company_name,job_description,income,requirements,occupation1,occupation2,industry,pref,address,commute ,remarks,e_stat)   
            job_list.append([id, company_name,job_description,income,requirements, occupation1,occupation2,industry,pref,address,commute ,remarks,e_stat])
            sleep(1)

finally:
    csv_header = ['ID','会社名','仕事内容','年収','対象','職種1','職種2','業種','都道府県','住所','最寄り駅','備考','雇用形態']
    csv_date= datetime.datetime.today().strftime("%Y%m%d%H%M%S")
    csv_file_name = "joblist" + csv_date + ".csv"
    with open(csv_file_name,"w",errors="ignore") as file:
        writer = csv.writer(file,lineterminator="\n")
        writer.writerow(csv_header)
        writer.writerows(job_list)