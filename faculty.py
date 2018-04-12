from selenium import webdriver
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import async_timeout
import json
import uvloop


class FacultyParser:
    """
    A class to store and parse information of a faculty
    """
    def __init__(self, preferred_name, raw):
        self.preferred_name = preferred_name
        self.raw = raw
        self.profile_picture = "N/A"
        self.official_title = "N/A"
        self.email_address = "N/A"
        self.room_number = "N/A"
        self.office_phone = "N/A"
        self.bio = "N/A"
        self.parse()
        self.save_raw()
        self.save_json()

    def __str__(self):
        return self.preferred_name

    def parse(self):
        """
        What we want:

            Profile picture:
                div.
                class="views-field views-field-field-profile-picture"
                    img.src

            Official title:
                div,
                class="field field-name-field-official-title field-type-text field-label-hidden"

            Email:
                div,
                class="field field-name-field-email-address field-type-text field-label-inline clearfix"

            Room number:
                div,
                class="field field-name-field-room-number field-type-text field-label-inline clearfix"

            Tel:
                div,
                class="field field-name-field-office-phone field-type-text field-label-inline clearfix"

            Bio:
                div,
                class="panel-pane pane-faculty-member-bio"
        """
        parser = BeautifulSoup(self.raw)

        # find profile picture
        profile_picture = parser.find_all("div", class_="views-field views-field-field-profile-picture")
        if profile_picture:
            profile_picture = profile_picture[0].find_all("img")
            if profile_picture:
                self.profile_picture = profile_picture[0].get("src")
        # find official title
        official_title = parser.find_all(
            "div", class_="field field-name-field-official-title field-type-text field-label-hidden")
        if official_title:
            official_title = official_title[0].text.strip()

            self.official_title = official_title
        # find email address
        email_address = parser.find_all(
            "div", class_="field field-name-field-email-address field-type-text field-label-inline clearfix")
        if email_address:
            email_address = email_address[0].text.strip().split()[1]
            self.email_address = email_address
        # find room number
        room_number = parser.find_all(
            "div", class_="field field-name-field-room-number field-type-text field-label-inline clearfix")
        if room_number:
            room_number = room_number[0].text.strip().split()[1]
            self.room_number = room_number
        # find office phone number
        office_phone = parser.find_all(
            "div", class_="field field-name-field-office-phone field-type-text field-label-inline clearfix")
        if office_phone:
            office_phone = office_phone[0].text.strip().split('\n')[2]
            self.office_phone = office_phone
        # find Bio
        bio = parser.find_all(
            "div", class_="panel-pane pane-faculty-member-bio")
        if bio:
            bio = bio[0]
            self.bio = bio.__str__()

    def save_json(self):
        info = self.__dict__
        del info['raw']
        with open("./falcutyJson/" + self.preferred_name + ".json", "w", encoding="utf-8") as f:
            print(self.preferred_name)
            f.write(json.dumps(info))

    def save_raw(self):
        with open("./falcutyRawPage/" + self.preferred_name + ".html", "w", encoding="utf-8") as f:
            f.write(self.raw)


if __name__ == "__main__":
    """
    Main logic of the crawler
    """
    # set up webdriver
    options = webdriver.ChromeOptions().add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64)'
        ' AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/51.0.2704.103 Safari/537.36')
    driver = webdriver.Chrome("bin/chromedriver", chrome_options=options)

    base_url = "https://shanghai.nyu.edu/academics/faculty/directory"
    total_pages = 9

    # A list to store urls
    url_todo = []

    for page_number in range(total_pages):
        # in each page, do the following
        page_url = base_url + "?page=" + str(page_number)
        driver.get(page_url)
        # get a name with url to his profile page
        faculty_list = driver.find_elements_by_xpath(
            "//div[@class='faculty-grid-directory list-active']//div[@class='views-field views-field-title']//a")
        for faculty in faculty_list:
            new_faculty = (faculty.text, faculty.get_attribute('href'))
            url_todo.append(new_faculty)
    driver.quit()
    print(url_todo.__len__())

    # following lines crawl all the faculty pages asynchronously
    async def get_page(session_func, url_func):
        # important: if the parsing time is expected to be long, please set a longer timeout
        with async_timeout.timeout(100):
            async with session_func.get(url[1]) as resp:
                FacultyParser(url_func[0], await resp.text())


    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    session = aiohttp.ClientSession(loop=loop)

    tasks = []
    for url in url_todo:
        tasks.append(get_page(session, url))

    loop.run_until_complete(asyncio.gather(*tasks))

    loop.close()
    session.close()
