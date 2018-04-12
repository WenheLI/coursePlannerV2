from time import sleep

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

locations = ["NYU Shanghai"]

ops = webdriver.ChromeOptions().add_argument(
    '--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
driver = webdriver.Chrome("./chromedriver", chrome_options=ops)

driver.get("http://albert.nyu.edu/albert_index.html")
buttons = driver.find_elements_by_class_name("buttonLink")
buttons[1].click()

tables = driver.find_elements_by_class_name("PSGROUPBOXWBO")

tables = tables[1:len(tables) - 7]  # subtract 8 noun course table

for i in range(len(tables)):
    t = driver.find_elements_by_class_name("PSGROUPBOXWBO")[1:len(tables) - 7]
    t = t[i]
    institution = t.find_element_by_tag_name("div")
    category = t.find_elements_by_tag_name("a")
    category.pop(0)
    for index in range(len(category)):
        sleep(2)
        t = driver.find_elements_by_class_name("PSGROUPBOXWBO")[1:len(tables) - 7]
        t = t[i]

        category_copy = t.find_elements_by_tag_name("a")
        category_copy.pop(0)

        c = category_copy[index]
        c.click()
        sleep(5)
        courses = driver.find_elements_by_xpath("//div[starts-with(@id, 'win0divNYU_CLS_SBDTLVW_CRSE_ID')]")

        for index_course in range(len(courses)):
            courses_copy = driver.find_elements_by_xpath("//div[starts-with(@id, 'win0divNYU_CLS_SBDTLVW_CRSE_ID')]")
            course = courses_copy[index_course]
            print("title", course.find_element_by_tag_name('b').text)
            print("desc", course.find_element_by_tag_name('p').text)

            detail = course.find_element_by_class_name("PSGROUPBOXWBO")
            print("detail", detail.text)

            expend = course.find_elements_by_tag_name('img')
            if len(expend) > 0:
                driver.execute_script("arguments[0].scrollIntoView(true);", expend[0])
                expend[0].click()

                sleep(2)

                courses_copy = driver.find_elements_by_xpath(
                    "//div[starts-with(@id, 'win0divNYU_CLS_SBDTLVW_CRSE_ID')]")
                course = courses_copy[index_course]

                term_info = course.find_element_by_xpath("//div[starts-with(@id, 'win0divNYU_CLS_DERIVED_TERM$')]")
                print(term_info.text)

            else:
                print("No Expend")
        try:
            back = driver.find_element_by_id("NYU_CLS_DERIVED_BACK")  # wait button
            sleep(8)
        except:
            sleep(8)
            back = driver.find_element_by_id("NYU_CLS_DERIVED_BACK")  # wait button
        back.click()
        sleep(2)
    sleep(2)


driver.quit()
