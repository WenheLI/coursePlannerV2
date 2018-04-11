from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

locations = ["NYU Shanghai"]

# set up webdriver
options = webdriver.ChromeOptions().add_argument(
    '--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64)'
    ' AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/51.0.2704.103 Safari/537.36')
driver = webdriver.Chrome("bin/chromedriver", chrome_options=options)

base_url = "http://albert.nyu.edu/albert_index.html"
driver.get(base_url)

# click into public course search
buttons = driver.find_elements_by_class_name("buttonLink")
buttons[1].click()

# using xpath to get all subjects
subjects = driver.find_elements_by_xpath("//a[starts-with(@id, 'LINK') and @class='PSHYPERLINK']")
selector = Select(driver.find_element_by_id("NYU_CLS_WRK2_DESCR254$33$"))

# for s in range(len(selector.options)):
selector.select_by_index(2)

selector = Select(driver.find_element_by_id("NYU_CLS_WRK2_DESCR254$33$"))
selector.select_by_index(3)

#sleep(10)

print(subjects.__len__())

driver.quit()

