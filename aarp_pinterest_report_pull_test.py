from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
import os.path
import time
import os
import fnmatch, glob
from datetime import datetime, timedelta
import datetime
import pandas as pd
from bs4 import BeatifulSoup
from mitmproxy import ctx

chrome_options = Options()
# chrome_options.add_argument("--headless")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

chrome_options.add_argument(f'user-agent={user_agent}')
       
prefs = {'download.default_directory': '/Users/victorolade/Box/Domo - AARP/AARP - Pinterest', "download.prompt_for_download": False }
chrome_options.add_experimental_option('prefs', prefs)

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(options=chrome_options,executable_path='/Users/victorolade/old Desktop/Selenium Automation/chromedriver')

#add missing support for chrome "send_command"  to selenium webdriver
driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': "/Users/victorolade/Box/Domo - AARP/AARP - Pinterest"}}
command_result = driver.execute("send_command", params)

user = "" #Define username 
pwd = "" #Define password

# STEP 1. Go to the Pinterest Ads home page
driver.get("https://ads.pinterest.com/login")

# Marker for when Step 1 is complete
print("Step 1 is complete")

# STEP 2. Login
elem = driver.find_element_by_id("email")
elem.send_keys(user)
elem = driver.find_element_by_id("password")
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)

# Marker for when Step 2 is complete
print("Step 2 is complete")

apath = "//*[@id=\"HeaderContent\"]/div/div/div/div/div/div/div[3]/div/div/div/div/div/a/div/div/div[1]/div"  #Path for Ads Menu
rpath = "//*[@id=\"HeaderContent\"]/div/div/div/div/div/div/div[3]/div/div[2]/ul/li[4]/a" #Path for reporting option in Ads Menu
adsTab = "/html/body/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div[2]/div/div/ \
div/div[1]/div/div/button[3]/div" #click on ads tab
exportMenu = "/html/body/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div/div[3]/div/div[1] \
/div/div[1]/div/div/div[2]/div/div[1]/div/div/div" #click export menu
customReport  = "/html/body/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div/div[3]/ \
div/div[1]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/div/div/div[1]/div/div/ul/li[4]/div/div/div" # click custom report
awareness = "/html/body/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div/div/div[2] \
/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[2]/label/div/div[2]/div" #select awareness
engagement = "/html/body/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div/div/div[2] \
/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[3]/label/div/div[2]/div" #select engagement
video = "/html/body/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/ \
div[2]/div/div[2]/div[1]/div[1]/div[2]/div[4]/label/div/div[2]/div" #select video
promo_clicks = "/html/body/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div/div/div[2] \
/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[5]/label/div/div[2]/div" #select promoted clicks
promo_installs = "/html/body/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div/div/div[2]\
/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[6]/label/div/div[2]/div" #select promoted installs
shopping = "/html/body/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/ \
div[2]/div/div[2]/div[1]/div[1]/div[2]/div[7]/label/div/div[2]/div" #select shopping
last30 = "/html/body/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/ \
div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[4]/label/div/div[2]/div" #select last 30 days
ag_dev_per_day = "/html/body/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div/div/div[2]\
/div/div[2]/div/div[2]/div[1]/div[2]/div[6]/label/div/div[2]/div" #select ad group performance per device per day
exportButton = "/html/body/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/ \
div[3]/div/div/div/span/button" #click export button

wait = WebDriverWait(driver, 90)

paths = [apath,rpath,adsTab,exportMenu,customReport,awareness,engagement,video,promo_clicks,promo_installs,shopping,last30,ag_dev_per_day,exportButton]
no_wait = [awareness,engagement,video,promo_clicks,promo_installs,shopping,last30,ag_dev_per_day]

count = 3

def export_report(path_array):
    global path,variable,count
    for path in path_array:
        printSteps = "Step" + ' ' + str(count) + ' ' + 'is complete'
        variable = wait.until(EC.element_to_be_clickable((By.XPATH, path)))
        if path in no_wait:
            variable.click()
        else:
            time.sleep(10)
            variable.click()            
        print(printSteps)
        count+=1

#Change report name

path = os.chdir('/Users/victorolade/Box/Domo - AARP/AARP - Pinterest')

def rename_report():
    global filenames, bn, file, max_date, max_dt, min_date, min_dt,new_name
    filenames = glob.glob("../AARP - Pinterest/ad_group_targeting_day*.csv")
    for file in filenames:
        bn = os.path.basename(file)
        df = pd.read_csv(bn)
        max_date = max(df['Date'])
        max_dt = datetime.datetime.strptime(max_date,'%Y-%m-%d')
        max_date = max_dt.strftime('%m%d%y')
        
        min_date = min(df['Date'])
        min_dt = datetime.datetime.strptime(min_date,'%Y-%m-%d')
        min_date = min_dt.strftime('%m%d%y')
    
        new_name = 'aarp_pinterest' + '_' + min_date + '_' + max_date + '.csv'
        os.rename(bn, new_name)

        print('Final Step Complete! YAY!!!!!')

#Run the following functions
        
export_report(paths)

time.sleep(10)

driver.close()

rename_report()


