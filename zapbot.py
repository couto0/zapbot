from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import personalinfo
import time

class ZapBot:

    firefox_profile_dir = personalinfo.firefox_profile_dir
    whatsapp_searchbox_class = "_2zCfw"
    whatsapp_msgbox_class = "_3u328"
    whatsapp_msg_in_class = "FTBzM.message-in"
    whatsapp_msg_hour_class = "_3fnHB"
    whatsapp_button_class= "_3j8Pd"
    whatsapp_send_button_class = "_1g8sv.NOJWi"

    def __init__(self, headless=False):
        self.profile = FirefoxProfile(self.firefox_profile_dir)
        self.options = Options()
        self.options.add_argument('-headless')
        if headless:
            self.driver = Firefox(firefox_profile=self.profile, executable_path='geckodriver', options=self.options)
        else:
            self.driver = Firefox(firefox_profile=self.profile, executable_path='geckodriver')
        self.driver.get('https://web.whatsapp.com')


        page_not_loaded = True
        while page_not_loaded:
            try:
                self.searchbox = self.driver.find_element_by_class_name(self.whatsapp_searchbox_class)
                page_not_loaded = False
            except NoSuchElementException:
                time.sleep(0.5)

    def select_contact(self, contact_name):
        """selects the current conversation"""

        self.searchbox.send_keys(contact_name)
        self.contact = self.driver.find_element_by_xpath('//span[@title = "{}"]'.format(contact_name))
        self.contact.click()
        self.msgbox = self.driver.find_element_by_class_name(self.whatsapp_msgbox_class)

    def send_msg(self, msg):
        for m in msg.split('\n'):
            self.msgbox.send_keys(m, Keys.SHIFT, Keys.ENTER)
        self.msgbox.send_keys(Keys.ENTER)

    def read_last_msg(self):
        """reads the last message, and returns a tuple containing the text, and the hour of the message"""
        try:
            self.msgs_in = self.driver.find_elements_by_class_name(self.whatsapp_msg_in_class)
            last_msg = self.msgs_in[-1].find_element_by_css_selector('span.selectable-text').text
            hour = self.msgs_in[-1].find_element_by_css_selector('span.' + self.whatsapp_msg_hour_class).text
            return last_msg, hour
        except NoSuchElementException:
            return None

    def send_file(self, file_path):
        """attaches and sends a file. Can be a image, video, document or audio file."""

        self.driver.find_elements_by_class_name(self.whatsapp_button_class)[-2].click()
        send_image = self.driver.find_element_by_css_selector("input[type='file']").send_keys(file_path)
        file_not_loaded = True
        while file_not_loaded:
            try:
                self.driver.find_element_by_class_name(self.whatsapp_send_button_class).click()
                file_not_loaded = False
            except NoSuchElementException:
                time.sleep(0.5)
