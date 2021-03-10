# -*- coding: utf-8 -*-
import time
import os
import sys


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *



class Voter():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options,
                                       executable_path=os.getcwd() + './chromedriver')

    def load_data(self):
        logins_list = []
        fio_list = []
        email_list = []
        password_list = []

        lg = open('logins.txt', 'r', encoding = 'utf-8')
        for l in lg:
            logins_list.append(l.replace('\n',''))

        fi = open('fio.txt', 'r', encoding = 'utf-8')
        for f in fi:
            fio_list.append(f.replace('\n', ''))

        em = open('emails.txt', 'r', encoding = 'utf-8')
        for e in em:
            email_list.append(e.replace('\n', ''))

        pw = open('emails.txt', 'r', encoding = 'utf-8')
        for p in pw:
            password_list.append(p.replace('\n', ''))

        print('logins', len(logins_list))
        print('fio', len(fio_list))
        print('emails', len(email_list))
        print('passwords', len(password_list))



if __name__ == '__main__':
    vt = Voter()
    vt.load_data()
