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
from twocaptcha import TwoCaptcha, ApiException


API = input('Вставьте ключ rucaptcha: ')
time_out = input('Введите задержку для голосований(в секундах) между аккаунтами: ')
#API = '85a9a133c454bea489b63692901579b6'

class Auth():
    def __init__(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

        self.driver = webdriver.Chrome(options=chrome_options,
                                       executable_path=os.getcwd() + './chromedriver')



    def captcha_response(self, captcha_api_key):
        api_key = os.getenv('APIKEY_2CAPTCHA', f'{captcha_api_key}')
        solver = TwoCaptcha(api_key)

        result = solver.normal('current_captcha.png')


        return result['code']

    def crop_default(self):
        self.driver.save_screenshot("fullPageScreenshot.png")
        left = 720
        top = 260
        right = 900
        bottom = 300
        fullImg = Image.open("fullPageScreenshot.png")
        cropImg = fullImg.crop((left, top, right, bottom))
        cropImg.save("current_captcha.png")


    def crop_failed_captcha(self):
        self.driver.save_screenshot("fullPageScreenshot.png")
        left = 425
        top = 620
        right = 550
        bottom = 650
        fullImg = Image.open("fullPageScreenshot.png")
        cropImg = fullImg.crop((left, top, right, bottom))
        cropImg.save("current_captcha.png")


    def load_accounts(self):
        logins_list = []
        with open('registered_accs.txt', 'r') as f:
            for i in f:
                logins_list.append(i.replace('\n',''))

        return logins_list

    def auth(self):
        url = "https://ebudget.primorsky.ru/Login/Form"
        #self.crop_default()
        accounts = self.load_accounts()
        for i in accounts:
            self.driver.get(url)
            self.driver.find_element_by_xpath("//input[contains(@name,'login')]").send_keys(i.split(':')[0])
            self.driver.find_element_by_xpath("//input[contains(@type,'password')]").send_keys(i.split(':')[1])


            while True:
                try:
                    self.crop_default()
                    captcha_solve_data = self.captcha_response(API)
                except ApiException:
                    continue

                self.driver.find_element_by_xpath("//input[contains(@name,'captcha')]").send_keys(captcha_solve_data)
                self.driver.find_element_by_xpath("//input[contains(@value,'Вход')]").click()
                time.sleep(3)
                try:
                    WebDriverWait(self.driver, 10).until(EC.alert_is_present())
                    alert = self.driver.switch_to.alert
                    alert.accept()
                    time.sleep(3)
                    self.crop_default()
                    try:
                        cap_field = self.driver.find_element_by_xpath("//input[contains(@name,'captcha')]")
                        for k in range(1, 13):
                            cap_field.send_keys(Keys.BACK_SPACE)

                    except (NoSuchElementException, UnexpectedAlertPresentException):
                        pass
                    continue
                except TimeoutException:
                    if 'Инструкция для голосования' in self.driver.page_source or 'Выйти' in self.driver.page_source:
                        print('Авторизовались успешно')
                        break

            self.driver.get('https://ebudget.primorsky.ru/Pib/Project/747-0004')

            try:
                time.sleep(3)
                if 'На странице произошла ошибка. Вы можете попробовать сделать следующие действия:' in self.driver.page_source:
                    time.sleep(5)
                    self.driver.get('https://ebudget.primorsky.ru/Pib/Project/747-0004')
            except NoSuchElementException:
                continue
            self.driver.find_element_by_xpath("//span[contains(.,'Поддержать')]").click()
            print('Проголосовали =)')
            # Пишем логины проголосоващах  аккаунтов в файл, для отчёта
            log_file = open('voted_accs.txt', 'a')
            log_file.write(f"{i.split(':')[0]}:{i.split(':')[1]}" + '\n')
            log_file.close()
            time.sleep(int(time_out))

        #  как закончились аккаунты - закрываем браузер нахуй и забываем о проекте хи-хи, ха-ха
        self.driver.close()

vt = Auth()
vt.auth()