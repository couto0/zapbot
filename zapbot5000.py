#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import personal
import time
import json


headless = True
firefox_profile_dir = personal.firefox_profile_dir
msgbox_class = personal.msgbox_class
chat_title_class = personal.chat_title_class
chat_search_class = personal.chat_search_class
send_button_class = personal.send_button_class
msg_class = personal.msg_class

help_msg = ['Comandos disponíveis:',
            '*/help*: exibe essa mensagem',
            '*/mem*: mostra os lembretes',
            '*/mem _LEMBRETE_*: adiciona um lembrete']

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

def read_json(fname):
    try:
        with open(fname, 'r') as f:
            jsondata = json.load(f)
            return jsondata
    except FileNotFoundError:
        with open(fname, 'w') as f:
            json.dump([], f)
    return []

def write_json(fname, jsondata):
    with open(fname, 'w') as f:
        json.dump(jsondata, f)

def memorize(data):
    mem = read_json('mem.json')
    if data:
        mem.append(data)
        print('Armazenando:')
        print(mem)
        write_json('mem.json', mem)
        send_msg('Lembrete armazenado!')
    else:
        if mem:
            for i in range(len(mem)):
                mem[i] = '- ' + mem[i]
            mem.insert(0, '*LEMBRETES:*')
            send_msg(mem)
        else:
            send_msg('Nenhum lembrete armazenado.')

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
time.sleep(2)

print('Iniciado!')
send_msg('Iniciado!')
while 1:
    last_msg = read_last_message()
    print(last_msg)
    if last_msg[0] == '/':
        message = last_msg.split(' ', 1)
        cmd = message[0].lower()
        data = ''
        if len(message) > 1:
            data = message[1]
        if cmd == '/help':
            send_msg(help_msg)
        if cmd == '/mem':
            memorize(data)

    time.sleep(3)
