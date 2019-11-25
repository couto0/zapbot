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
import os
import randimage

headless = False
firefox_profile_dir = personal.firefox_profile_dir
msgbox_class = personal.msgbox_class
chat_title_class = personal.chat_title_class
chat_search_class = personal.chat_search_class
send_button_class = personal.send_button_class
send_button_image_class = personal.send_button_image_class
contact_name = personal.contact_name
msg_class = personal.msg_class

help_msg = ['Comandos disponíveis:',
            '*/help*: exibe essa mensagem',
            '*/mem*: mostra os lembretes',
            '*/mem _LEMBRETE_*: adiciona um lembrete',
            '*/role _NOME DO ROLE_*: configura o role atual',
            '*/confirmado*: mostra os confirmados no role',
            '*/confirmado _NOME_*: confirma o nome no role',
            '*/imagem*: envia uma imagem']

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

def send_img():
    msg_box = driver.find_element_by_class_name(msgbox_class)
    home_dir = os.path.dirname(os.path.realpath(__file__))
    memes_dir = os.path.join(home_dir, 'Memes')
    img_dir = os.path.join(memes_dir, randimage.generate())
    os.system('xclip -selection clipboard -t image/png -i {}'.format(img_dir))
    time.sleep(1)
    msg_box.send_keys('hmm', Keys.CONTROL, 'v')
    time.sleep(2)
    send_button_image = driver.find_element_by_class_name(send_button_image_class)
    send_button_image.click()

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

def memorize(fname, data):
    mem = read_json(fname + '.json')
    if data:
        mem.append(data)
        print('Armazenando:')
        print(mem)
        write_json(fname + '.json', mem)
        send_msg('ok!')
    else:
        if mem:
            for i in range(len(mem)):
                mem[i] = '- ' + mem[i]
            mem.insert(0, '*{}*'.format(fname.upper()))
            send_msg(mem)
        else:
            send_msg('Nada armazenado.')

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

searchbox.send_keys(contact_name)
time.sleep(2)
contact = driver.find_element_by_xpath('//span[@title = "{}"]'.format(contact_name))
contact.click()
time.sleep(2)

print('Iniciado!')
#send_msg('/help para ver os comandos disponíveis')
role = ''
last_msg = ''
#send_msg('*começou o ataque dos bot loko*')
#send_msg('/help para ajuda')
while 1:
    try:
        last_msg = read_last_message()
    except:
        send_msg('buguei')
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
            memorize('lembretes', data)
        if cmd == '/role':
            role = data
            send_msg('o role do momento é *_{}_*'.format(role.upper()))
        if cmd == '/confirmado':
            memorize(role, data)
        if cmd == '/imagem':
            send_img()

    if last_msg[-1] == '?':
        if len(last_msg)%2:
            send_msg('sim')
        else:
            send_msg('não')
    time.sleep(1)
