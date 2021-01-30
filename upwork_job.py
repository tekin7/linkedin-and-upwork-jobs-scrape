from selenium import webdriver
from time import sleep
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
import json
import datetime
import re

class upwork:
    def __init__(self):
        self.browserProfile = webdriver.FirefoxProfile()
        self.options = FirefoxOptions()
        # self.options.add_argument("--headless")
        self.browserProfile.set_preference("general.useragent.override","Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
        self.browser = webdriver.Firefox(options=
        self.options,firefox_profile=self.browserProfile, executable_path=GeckoDriverManager().install())
        self.job_urls = []
        self.base_url = "https://www.upwork.com"
        self.page = 1

    def jobs(self):
        data = {}
        data['upwork'] =[]
        print("\n Job posting searching... \n") 
        while self.page <= 1:
            self.browser.get("https://www.upwork.com/search/jobs/?category2_uid=531770282580668423&page="+str(self.page)+"&sort=recency")
            links = self.browser.find_elements_by_xpath("//a[@class='job-title-link break visited']")
            for link in links:
                self.job_urls.append(link.get_attribute("href"))
            self.page +=1
            sleep(2)
        print("\n",len(self.job_urls)," Job postings found! \n")
        i = 1
        for job_url in self.job_urls:
            self.browser.get(job_url)
            self.job_salary = ""
            print("\n Job posting ("+str(i)+")\n")
            try:
                job_title = self.browser.find_element_by_xpath("//h2[@class='m-0']").text.strip()
         
                j_date = self.browser.find_element_by_id("posted-on").text.strip()
                job_date = self.covert_date(j_date)
                job_description = self.browser.find_element_by_xpath("//div[@class='break mb-0']").text.strip()
                try:
                    job_location = self.browser.find_element_by_xpath("//span[@class='vertical-align-middle']").text.strip()
                except:
                    job_location = self.browser.find_element_by_xpath("//span[@class='text-muted d-none d-md-inline vertical-align-middle']").text.strip()
                try:
                    salary_type = self.browser.find_element_by_xpath("//small[@class='text-muted']").text.strip()
                except:
                    pass
                if salary_type == "Fixed-price":
                    self.job_salary = self.browser.find_element_by_xpath("/html/body/div/div/div/div/div[2]/div/div/div/div[2]/div/div[1]/section[3]/ul/li[1]/div/strong").text.strip()+" Fixed-price"
                elif salary_type == "Hourly":
                    self.job_salary = self.browser.find_element_by_xpath("/html/body/div/div/div/div/div[2]/div/div/div/div[2]/div/div[1]/section[3]/ul/li[4]/div/strong").text.strip() + " Hourly"
            except:
                pass
            data['upwork'].append({
                "job_title":job_title,
                "job_salary":self.job_salary,
                "job_location":job_location,
                "job_date":job_date,
                "job_description": job_description,
                "url":self.browser.current_url
            })
            i += 1
        with open('dataup.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile) 
            print("\n Job posting list completed! \n")
    def covert_date(self, j_date):
        converted_date = ""
        if j_date.find("minutes") != -1 or j_date.find("minute") != -1:
            date_int = int(re.search(r'\d+', j_date).group()) 
            k = datetime.datetime.now()- datetime.timedelta(minutes = date_int)
            converted_date= k.strftime("%Y-%m-%d %H:%M:%S")
        elif j_date.find("hours") != -1 or j_date.find("hour") != -1:
            date_int = int(re.search(r'\d+', j_date).group()) 
            k = datetime.datetime.now()- datetime.timedelta(hours = date_int)
            converted_date= k.strftime("%Y-%m-%d %H:%M:%S")
        elif j_date.find("day") != -1 or j_date.find("days") != -1:
            date_int = int(re.search(r'\d+', j_date).group()) 
            k = datetime.datetime.now()- datetime.timedelta(days = date_int)
            converted_date= k.strftime("%Y-%m-%d %H:%M:%S")
        elif j_date.find("week") != -1 or j_date.find("weeks") != -1:
            date_int = int(re.search(r'\d+', j_date).group()) 
            k = datetime.datetime.now()- datetime.timedelta(weeks = date_int)
            converted_date= k.strftime("%Y-%m-%d %H:%M:%S")
        elif j_date.find("month") != -1 or j_date.find("months") != -1:
            date_int = int(re.search(r'\d+', j_date).group()) 
            k = datetime.datetime.now()- datetime.timedelta(days = date_int*30)
            converted_date= k.strftime("%Y-%m-%d %H:%M:%S")
        return converted_date
up = upwork()
up.jobs()