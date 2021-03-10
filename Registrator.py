# -*- coding: utf-8 -*-
import time
import os
import sys
import urllib
import urllib.request


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import requests
from PIL import Image
from twocaptcha import TwoCaptcha


API = input('Вставьте ключ rucaptcha: ')

#API = '85a9a133c454bea489b63692901579b6'

class Register():
    def __init__(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(options=chrome_options,
                                       executable_path=os.getcwd() + './chromedriver')

    def captcha_response(self, captcha_api_key):
        print('посылаем капчу на разгаду')
        api_key = os.getenv('APIKEY_2CAPTCHA', f'{captcha_api_key}')
        solver = TwoCaptcha(api_key)
        result = solver.normal('current_captcha.png')
        return result['code']

    def crop_default(self):
        self.driver.save_screenshot("fullPageScreenshot.png")
        left = 425
        top = 560
        right = 550
        bottom = 600
        fullImg = Image.open("fullPageScreenshot.png")
        width, height = fullImg.size
        print(width, height)
        cropImg = fullImg.crop((left, top, right, bottom))
        cropImg.save("current_captcha.png")


    def crop_failed_captcha(self):
        self.driver.save_screenshot("fullPageScreenshot.png")
        left = 425
        top = 550
        right = 550
        bottom = 650
        fullImg = Image.open("fullPageScreenshot.png")
        cropImg = fullImg.crop((left, top, right, bottom))
        cropImg.save("current_captcha.png")


    def load_data(self):
        logins_list = []
        fio_list = []
        email_list = []
        password_list = []

        big_data_list = []

        lg = open('logins.txt', 'r', encoding='utf-8')
        for l in lg:
            logins_list.append(l.replace('\n', ''))

        fi = open('fio.txt', 'r', encoding='utf-8')
        for f in fi:
            fio_list.append(f.replace('\n', ''))

        em = open('emails.txt', 'r', encoding='utf-8')
        for e in em:
            email_list.append(e.replace('\n', ''))

        pw = open('passwords.txt', 'r', encoding='utf-8')
        for p in pw:
            password_list.append(p.replace('\n', ''))

        for l, f, e, p in zip(logins_list, fio_list, email_list, password_list):
            big_data_list.append([l, f, e, p])


        return big_data_list


    def do_register(self):
        data_list = self.load_data()
        url = 'https://ebudget.primorsky.ru/Login/RegisterUser?retUrl=%2fMenu%2fPage%2f1446'

        for i in data_list:
            print('current_data',i)
            self.driver.get(url)
            self.driver.find_element_by_id("Name").send_keys(i[0]) # login
            self.driver.find_element_by_id("FullName").send_keys(i[1])  # FIO
            self.driver.find_element_by_id("Email").send_keys(i[2])  # email
            self.driver.find_element_by_id("Password").send_keys(i[3])  # password 1
            self.driver.find_element_by_id("CheckPassword").send_keys(i[3])  # password 2

            # вырезаем фото капчи
            self.crop_default()

            while True:
                captcha_solve_data = self.captcha_response(API)
                self.driver.find_element_by_xpath("//input[contains(@id,'captcha')]").send_keys(captcha_solve_data)
                time.sleep(1)
                self.driver.find_element_by_id("link_submit").click()
                time.sleep(1)

                if 'Введённый код не соответствует изображению. Сгенерирован новый код' in self.driver.page_source:
                    self.crop_failed_captcha()
                    self.driver.find_element_by_id("Password").send_keys(i[3])  # password 1
                    self.driver.find_element_by_id("CheckPassword").send_keys(i[3])  # password 2

                    time.sleep(5)
                    cap_field = self.driver.find_element_by_xpath("//input[contains(@id,'captcha')]")
                    for k in range(1,15):
                        cap_field.send_keys(Keys.BACK_SPACE)
                    continue
                elif 'Ваша учетная запись успешно добавлена.' in self.driver.page_source:

                    # Пишем зареганнйы аккаунт в файл, для отчёта
                    log_file = open('registered_accs.txt', 'a')
                    log_file.write(f'{i[0]}:{i[3]}' + '\n')
                    log_file.close()
                    break # зарегистрировались
        self.driver.close()

vt = Register()
vt.do_register()