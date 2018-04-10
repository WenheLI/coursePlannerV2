from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

locations = ["NYU Shanghai"]

ops = webdriver.ChromeOptions().add_argument(
    '--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
driver = webdriver.Chrome(chrome_options=ops)

driver.get("http://albert.nyu.edu/albert_index.html")
buttons = driver.find_elements_by_class_name("buttonLink")

buttons[1].click()

courses = driver.find_elements_by_xpath("//a[starts-with(@id, 'LINK') and @class='PSHYPERLINK']")
selector = Select(driver.find_element_by_id("NYU_CLS_WRK2_DESCR254$33$"))

# for s in range(len(selector.options)):
selector.select_by_index(1)
sleep(1)
selector.select_by_index(2)
print(courses.__len__())

driver.quit()


