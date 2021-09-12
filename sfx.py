#%%

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

import requests
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

import re
from math import ceil

from typing import List

#%%

def html_to_ids(html_text: str) -> List[str]:
    ids = []
    split_html = html_text.split('<li>')
    split_html.pop(0)
    for sent in split_html:
         ids.append(sent.partition('data-listing-id=\"')[2].partition("\"")[0])
    return ids

def get_app_ids(selpath: str) -> List[str]:
    """
    Default sleep to enable the browser to execute JS, and the SalesForce Server to Respond

    selpath example:
    C:\selpath\chromedriver.exe
    """

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(selpath, options=options)


    # URL of website
    url = "https://appexchange.salesforce.com/appxStore?type=App"
    
    # Opening the website
    driver.get(url)
    
    sleep(10.0)

    print("sleeping for 10 seconds to allow page to load")


    app_count = driver.find_element_by_id("total-items-store")
    app_count = int(app_count.get_attribute('innerHTML'))

    # For DEMO! Each 28 apps takes up to 423.2s
    # app_count = 28

    count = 28
    while count <= app_count:
        try:
            button = driver.find_element_by_id("appx-load-more-button-id")
            # clicking on the button
            button.click()
            sleep(10.0)
            print('click successful')
            count += 28
        except Exception as ex:
            print(ex)


    dt = driver.find_element_by_id("appx-table-results")
    app_html = dt.get_attribute('innerHTML')
    
    return html_to_ids(app_html)

def get_Name() -> str:
    try:
        re = app_soup.find_all('h1', attrs={'class':'appx-page-header-2_title'})
        return re[0].string.strip()
    except:
        re = ""
        return re

def get_Pricing() -> str:
    try:
        re = app_soup.find_all('span', attrs={'id':'appxListingDetailPageId:AppxLayout:planList:0:planCharges'})
        return re[0].string.strip()
    except:
        re = app_soup.find('span', attrs={'id':'appxListingDetailPageId:AppxLayout:j_id805'})
        return list(re)[0].string.strip()

def get_Categories() -> str:
    try:
        re = app_soup.find_all('a', attrs={'id':'appxListingDetailPageId:AppxLayout:listingCategories:0:firstCat'})
        return re[0].string.strip()
    except:
        re = ""
        return re

def get_Ratings() -> str:
    try:
        re = app_soup.find_all('span', attrs={'id':'appxListingDetailPageId:AppxLayout:j_id840:j_id841:j_id848'})
        return re[0].string.strip()
    except:
        re = ""
        return re

def get_Latest_Release() -> str:
    try:
        re = app_soup.find_all('span', attrs={'id':'appxListingDetailPageId:AppxLayout:j_id857'})
        return list(re[0].children)[3].string.strip()
    except:
        re = ""
        return re

def get_Tool_Intro_Information() -> str:
    re = ""
    try:
        tool_info = app_soup.find_all('div', attrs={'class':'appx-detail-section-description appx-multi-line-to-fix'})
        re = re + list(tool_info[0].children)[1].string + '\n' + list(tool_info[0].children)[3].string
        return re
    except:
        return re

def get_Highlights() -> str:
    re = ""
    try:
        highlights = app_sub_soup.find("ul", {"id": "AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:ftListInventory"})
        for child in highlights.children:
            s = list(list(child.children)[3].children)
            re = re + s[0].string
            if highlights.index(child) == len(highlights)-1:
                continue
            else:
                re = re + '\n\n'
        return re
    except:
        return re

def get_Description() -> str:
    try:
        re = app_sub_soup.find_all('div', attrs={'class':'appx-extended-detail-description appx-multi-line-to-fix'})
        return re[0].string.strip()
    except:
        re = ""
        return re

def get_Requirements() -> str:
    re = ""
    try:
        headReq = app_sub_soup.find_all('div', attrs={'class':'appx-extended-detail-subsection-label'})
        re = re + list(headReq)[0].string + '\n'
        req = app_sub_soup.find_all('div', attrs={'class':'appx-extended-detail-subsection-description'})
        for i in range(1,len(list(list(req[0].children))), 2):
            if (i == len(list(list(req[0].children))) - 2):
                re = re + (list(list(req[0].children))[i].string.strip())
            else:
                re = re + (list(list(req[0].children))[i].string.strip()) + " "
        re = re + '\n'
        headOtherSys = app_sub_soup.find_all('div', attrs={'class':'appx-extended-detail-subsection-label'})
        re = re + list(headOtherSys)[1].string + '\n'
        req = app_sub_soup.find_all('div', attrs={'class':'appx-extended-detail-subsection-description appx-multi-line-to-fix'})
        re = re + list(req)[0].string.strip()
        return re
    except:
        return re

def get_Support() -> str:
    ret = ""
    try:
        support_list = [["Phone","AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id129"], ["Email","AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id131"], ["Knowledge","AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id137"]]
        for st in support_list:
            support = app_sub_soup.find('div',id=st[1])
            if support is None:
                continue
            else:
                if(st[0] == "Phone"):
                    ret = support.contents[0] + "\n"
                if(st[0] == "Email"):
                    ret = ret + "Ëmail" + '\n' + re.findall(r'"(?:(?:(?!(?<!\\)").)*)"',str(support.contents))[0][1:-1].split(':')[1] + '\n'
                if(st[0] == "Knowledge"):
                    ret = ret + "Knowledge Base" + '\n' + re.findall(r'"(?:(?:(?!(?<!\\)").)*)"',str(support.contents))[0][1:-1] + '\n'
        return ret.strip()
    except:
        return ret.strip()

def get_Additional_Information() -> str:
    try:
        re = "Package Name" + '\n' 
        packageName = app_sub_soup.find_all('div', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id146'})
        re = re + packageName[0].string.strip()
        
        re = re + '\n' + "Version" + '\n'
        versionName = app_sub_soup.find_all('div', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id149'})
        re = re + versionName[0].string.strip()
        
        re = re + '\n' + "Listed On" + '\n'
        listedOn = app_sub_soup.find('div', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id152'})
        re = re + list(listedOn.children)[3].string.strip()
        
        re = re + '\n' + "Latest Release" + '\n'
        latestRelease = app_sub_soup.find('div', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id154'})
        re = re + list(latestRelease.children)[3].string.strip()
        
        re = re + '\n' + "Languages" + '\n'
        lang = app_sub_soup.find_all('a', attrs={'data-event':'listing-languages'})    
        for i in range(len(list(lang))):
            re = re + list(lang)[i].string.strip()
        
        return re
    except:
        re = ""
        return re

def get_About_Company() -> str:
    try:
        re = app_sub_soup.find_all('p', attrs={'class':'appx-extended-detail-company-description'})
        return re[0].string.strip()
    except:
        re = ""
        return re

def get_Website() -> str:
    try:
        re = app_sub_soup.find_all('a', attrs={'data-event':'listing-publisher-website'})
        return re[0].string.strip()
    except:
        re = ""
        return re

def get_Email() -> str:
    try:
        re = app_sub_soup.find_all('a', attrs={'data-event':'listing-publisher-email'})
        return re[0].string.strip()
    except:
        re = ""
        return re

def get_Address() -> str:
    try:
        re = app_sub_soup.find_all('div', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id350'})
        return re[0].string.strip()
    except:
        re = ""
        return re
#%%

if __name__ == "__main__":
    apps_ids_list = get_app_ids(r'C:\Github\Salesforce-Appexchange\chromedriver.exe')
    
    # creating pandas and setting all attributes needed
    df = pd.DataFrame(columns=['Name','Pricing','Categories',
                               'Ratings','Latest Release',
                               'Tool Intro Information','Highlights','Description','Requirements',
                               'Support','Additional Information','About Company','Website','Email','Address'])
    
    for appID in apps_ids_list:
        global app_soup    
        global app_sub_soup
    
        # APP ID page request
        app_url = f'https://appexchange.salesforce.com/appxListingDetail?listingId={appID}'
        app_get_url = requests.get(app_url)
        app_get_text = app_get_url.text
        app_soup = BeautifulSoup(app_get_text, "html.parser")
        
        # APP ID sub page request
        app_sub_url = f'https://appexchange.salesforce.com/AppxListingDetailOverviewTab?listingId={appID}'
        app_sub_get_url = requests.get(app_sub_url)
        app_sub_get_text = app_sub_get_url.text
        app_sub_soup = BeautifulSoup(app_sub_get_text, "html.parser")
        
        row = []
        row.append(get_Name())
        row.append(get_Pricing())
        row.append(get_Categories())
        row.append(get_Ratings())
        row.append(get_Latest_Release())
        row.append(get_Tool_Intro_Information())
        row.append(get_Highlights())
        row.append(get_Description())
        row.append(get_Requirements())
        row.append(get_Support())
        row.append(get_Additional_Information())
        row.append(get_About_Company())
        row.append(get_Website())
        row.append(get_Email())
        row.append(get_Address())
        row = np.array(row).reshape(1,-1)
        df = df.append(pd.DataFrame(row, columns=df.columns), ignore_index=True)
        
    df = df.replace('', np.nan)
    df.to_csv('Demo_SF.csv', index=False, encoding='utf-8')
#%%