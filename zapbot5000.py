#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import personal
import time


headless = False
firefox_profile_dir = personal.firefox_profile_dir
msgbox_class = personal.msgbox_class
chat_title_class = personal.chat_title_class
chat_search_class = personal.chat_search_class
send_button_class = personal.send_button_class
msg_class = personal.msg_class

help_msg = ['Comandos disponíveis:',
            'help: exibe essa mensagem',
            'mem: adiciona um lembrete',
            'remind: mostra os lembretes']

def send_msg(msg):
    msg_box = driver.find_element_by_class_name(msgbox_class)
    if type(msg) == list:
        for m in msg:
            msg_box.send_keys(m, Keys.SHIFT, Keys.ENTER)
    else:
        msg_box.send_keys(msg)
    send_button = driver.find_element_by_class_name(send_button_class)
    send_button.click()

def read_last_message():
    messages = driver.find_elements_by_class_name(msg_class)
    last = len(messages) - 1
    msg_text = messages[last].find_element_by_css_selector('span.selectable-text').text
    return msg_text

profile = FirefoxProfile(firefox_profile_dir)
options = Options()
options.add_argument('-headless')
if headless:
    driver = Firefox(firefox_profile=profile, executable_path='geckodriver', options=options)
else:
    driver = Firefox(firefox_profile=profile, executable_path='geckodriver')
print('iniciando')
driver.get('https://web.whatsapp.com')

time.sleep(3)
pageLoaded = False
while not pageLoaded:
    try:
        searchbox = driver.find_element_by_class_name(chat_search_class)
        pageLoaded = True
    except NoSuchElementException:
        print('page loading...')
        time.sleep(3)

side_panel = driver.find_element_by_id('side')

contact_name='zapbot5000'
searchbox.send_keys(contact_name)
time.sleep(2)
contact = driver.find_element_by_xpath('//span[@title = "{}"]'.format(contact_name))
contact.click()
time.sleep(5)

send_msg('iniciando...')
while 1:
    last_msg = read_last_message()
    if last_msg == 'help':
        send_msg(help_msg)
    if last_msg[-1] == '?':
        if len(last_msg)%2:
            send_msg('sim')
        else:
            send_msg('não')
    time.sleep(3)
