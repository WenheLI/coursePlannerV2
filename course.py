from time import sleep
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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

res = dict(length=0, data=[])
try:
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
                res['length'] += 1
                courses_copy = driver.find_elements_by_xpath("//div[starts-with(@id, 'win0divNYU_CLS_SBDTLVW_CRSE_ID')]")
                course = courses_copy[index_course]
                title = course.find_elements_by_tag_name('b')
                data = dict(title="", desc="", detail="", expend=[])
                if title:
                    data['title'] = "title", title[0].text

                description = course.find_elements_by_tag_name('p')
                if description:
                    data['desc'] = ("desc", description[0].text)

                detail = course.find_elements_by_class_name("PSGROUPBOXWBO")
                if detail:
                    data['detail'] = ("detail", detail[0].text)

                expend = course.find_elements_by_tag_name('img')
                if expend:
                    driver.execute_script("arguments[0].scrollIntoView(true);", expend[0])

                    expend[0].click()
                    sleep(5)

                    courses_copy = driver.find_elements_by_xpath(
                        "//div[starts-with(@id, 'win0divNYU_CLS_SBDTLVW_CRSE_ID')]")
                    course = courses_copy[index_course]
                    term_info = course.find_element_by_xpath("//div[starts-with(@id, 'win0divNYU_CLS_DERIVED_TERM$')]")
                    print(term_info.text)

                    terms = term_info.find_elements_by_tag_name("table")

                    for t in terms:
                        if len(t.text) > 0:
                            data['expend'].append(t.text)
                res['data'].append(data)
            try:
                back = driver.find_element_by_id("NYU_CLS_DERIVED_BACK")  # wait button
                sleep(3)
            except:
                sleep(3)
                back = driver.find_element_by_id("NYU_CLS_DERIVED_BACK")  # wait button
            back.click()
            sleep(2)
        sleep(2)
finally:
    source = json.dumps(res)
    with open("source.json", 'w') as f:
        f.write(source)
    driver.quit()
