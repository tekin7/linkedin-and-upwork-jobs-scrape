from selenium import webdriver
from time import sleep
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
import json
import datetime
import re
import threading

job_urls = []
class linkedn:
    def __init__(self):
        self.browserProfile = webdriver.FirefoxProfile()
        self.options = FirefoxOptions()
        self.browserProfile.set_preference("intl.accept_languages", "en-us")
        self.options.add_argument("--headless")
        self.browserProfile.set_preference("general.useragent.override","Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
        self.browser = webdriver.Firefox(options=
        self.options,firefox_profile=self.browserProfile, executable_path=GeckoDriverManager().install())
        
        
    def job_list(self):
        self.browser.get("https://www.linkedin.com/jobs/search/?f_F=wrt&f_T=49%2C206%2C3649%2C273%2C101%2C1277%2C2872&f_TPR=r2592000&geoId=92000000&keywords=writer&location=Worldwide&sortBy=DD")
        print("\n Linkedin Job posting searching... \n") 
        while len(self.job_urls) < 6000:
            action = webdriver.ActionChains(self.browser)
            for i in range(1,7):
                action.send_keys(Keys.SPACE).perform()
                try:
                    self.browser.find_element_by_xpath("//button[@class='infinite-scroller__show-more-button infinite-scroller__show-more-button--visible']").click()                   
                except:
                    action.send_keys(Keys.SPACE).perform()
            job_counts = self.browser.find_element_by_xpath("//span[@class='results-context-header__job-count']").text.replace(",","").replace(".","").strip("+")
            print(len(self.job_urls), "Job postings founded")
            job_hrefs = self.browser.find_elements_by_xpath("//a[@class='result-card__full-card-link']")
            for href in job_hrefs:
                link = href.get_attribute("href")
                self.job_urls.append(link)
        print("\n",len(self.job_urls)," Job postings found! \n")   

    def job_scrape(self):
        data = {}
        data['linkedin'] =[]
        i = 1
        for url in self.job_urls:
            self.browser.get(url)
            print("\n Linkedin Job posting ("+str(i)+")\n")
            try:
                self.browser.find_element_by_xpath("//button[@class='show-more-less-html__button show-more-less-html__button--more']").click()
            except:
                self.browser.get(url)
            job_title = self.browser.find_element_by_xpath("//h1[@class='topcard__title']").text.strip()
            job_company_name = self.browser.find_element_by_xpath("//span[@class='topcard__flavor']").text.strip()
            job_location = self.browser.find_element_by_xpath("//span[@class='topcard__flavor topcard__flavor--bullet']").text.strip()
            try:
                j_date = self.browser.find_element_by_xpath("//span[@class='topcard__flavor--metadata posted-time-ago__text']").text.strip()
                job_date = self.covert_date(j_date)
            except:
                j_date = self.browser.find_element_by_xpath("//span[@class='topcard__flavor--metadata posted-time-ago__text posted-time-ago__text--new']").text.strip()
                job_date = self.covert_date(j_date)
            try:
                job_description = self.browser.find_element_by_xpath("//div[@class='show-more-less-html__markup']").text.strip()
            except:
                job_description=self.browser.find_element_by_xpath("//div[@class='show-more-less-html__markup show-more-less-html__markup--clamp-after-5']").text.strip()
            data['linkedin'].append({
                "job_title":job_title,
                "job_company name":job_company_name,
                "job_location":job_location,
                "job_date":job_date,
                "job_description": job_description,
                "url":self.browser.current_url
            })
            i +=1
            
        with open('linkedin_jobs.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile) 
            print("\n Linkedin Job posting list completed! \n")
    def covert_date(self, j_date):
        converted_date = ""
        if j_date.find("minutes") != -1 or j_date.find("minute") != -1:
            date_int = int(re.search(r'\d+', j_date).group()) 
            k = datetime.datetime.now()- datetime.timedelta(minutes = date_int)
            converted_date= k.strftime("%Y-%m-%d")
        elif j_date.find("hours") != -1 or j_date.find("hour") != -1:
            date_int = int(re.search(r'\d+', j_date).group()) 
            k = datetime.datetime.now()- datetime.timedelta(hours = date_int)
            converted_date= k.strftime("%Y-%m-%d")
        elif j_date.find("day") != -1 or j_date.find("days") != -1:
            date_int = int(re.search(r'\d+', j_date).group()) 
            k = datetime.datetime.now()- datetime.timedelta(days = date_int)
            converted_date= k.strftime("%Y-%m-%d")
        elif j_date.find("week") != -1 or j_date.find("weeks") != -1:
            date_int = int(re.search(r'\d+', j_date).group()) 
            k = datetime.datetime.now()- datetime.timedelta(weeks = date_int)
            converted_date= k.strftime("%Y-%m-%d")
        elif j_date.find("month") != -1 or j_date.find("months") != -1:
            date_int = int(re.search(r'\d+', j_date).group()) 
            k = datetime.datetime.now()- datetime.timedelta(days = date_int*30)
            converted_date= k.strftime("%Y-%m-%d")
        return converted_date



linkedin = linkedn()
linkedin.job_list()
linkedin.job_scrap()
