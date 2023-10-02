from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import ( 
    Select,
    WebDriverWait
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
)
import os
import time
import random
import pandas as pd
from fake_useragent import UserAgent
import pyautogui
import sys
import random as rd
from random import randint

class reCaptcha:
    def __init__(self):
        self.options = Options()
        self.driver = Chrome()
        self.ua = UserAgent()
    def gencoordinates(self):
        list_tmp = []
        x = rd.randint(0,1440)
        y = rd.randint(0,900)
        list_tmp.append(x)
        list_tmp.append(y)
        return list_tmp

    def check_exists_by_xpath(browser, xpath=None, css=None):
        try:
            if xpath != None:
                browser.find_element(By.XPATH, xpath)
            elif css != None:
                browser.find_element(By.CSS_SELECTOR, css)
        except NoSuchElementException:
            return False
        return True

    def control_cursor(self):
        try:
            for i in range(rd.randint(2,5)):
                x = self.gencoordinates()[0]
                y = self.gencoordinates()[1]
                time = rd.uniform(1.0,2.0)
                pyautogui.moveTo(x,y,time)

            x1 = rd.randint(150,250)
            y1 = rd.randint(760,810)
            pyautogui.moveTo(x1,y1,time)
            pyautogui.click(clicks = 1,x = x1,y = y1)
            self.delay()
            pyautogui.moveTo(320,860,1)
            pyautogui.click(clicks = 1,x = 320,y = 860)
            self.delay()
        # try:
        #     while True:
        #         x, y = pyautogui.position()
        #         positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        #         print(positionStr, end='')
        #         print('\b' * len(positionStr),end='', flush=True)
        # except KeyboardInterrupt:
        #     print('\n')
        except Exception as exception:
            print(exception)

    def delay(self):
        time.sleep(5)

    def set_viewport_size(driver, width, height):
        window_size = driver.execute_script("""
            return [window.outerWidth - window.innerWidth + arguments[0],
            window.outerHeight - window.innerHeight + arguments[1]];
            """, width, height)
        driver.set_window_size(*window_size)

    def validate_phone(self,phones):
        for phone in self.phones:
            # options = Options()
            self.options.add_extension("/Users/dinhvan/Downloads/buster.crx")
            self.options.add_argument("--no-sandbox")
            # self.options.add_argument("--headless=chrome")
            # options.add_argument('window-size=1440x900')
            # options.add_argument('--disable-dev-shm-usage')
            # options.add_argument("--disable-dev-shm-usage")   
            self.options.add_argument("--kiosk")
            # options.add_argument('disable-infobars')
            # ua = UserAgent()
            userAgent = self.ua.random
            self.options.add_argument(f'user-agent={userAgent}')
            # options.add_experimental_option("detach", True)

            self.driver = webdriver.Chrome(options=self.options,executable_path=r'/Users/dinhvan/Downloads/chromedriver 2')
            self.driver.delete_all_cookies()
            self.driver.get("https://lnnte-dncl.gc.ca/en/Consumer/Check-your-registration/#!/")

            WebDriverWait(self.driver,30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "main-title")))
            
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located(
                        (By.ID, "phone")))
                phone_elem = self.driver.find_element(By.ID,"phone")
                phone_elem.clear()
                phone_elem.send_keys(phone)
                
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='submit-container']/button[@class='btn-rounded ng-binding']")))

                submit_elem = self.driver.find_element(By.XPATH,"//div[@class='submit-container']/button[@class='btn-rounded ng-binding']")
                submit_elem.click()
                time.sleep(1)


                #? switch to recaptcha frame
                frames = self.driver.find_elements(By.TAG_NAME,"iframe")
                self.driver.switch_to.frame(frames[0]);
                self.delay()
                # coordinate = driver.find_element(By.CLASS_NAME,"recaptcha-checkbox-border")
                # location = coordinate.location
                self.control_cursor()
                # print(location)
                # print(coordinate.size)
                # driver.find_element(By.CLASS_NAME,"recaptcha-checkbox-border").click()
                self.delay()
                self.driver.close()

            except Exception as exception:
                print('Error: '+ str(exception))
                self.driver.close()
                continue

if __name__ == '__main__':
    re = reCaptcha()
    phones = ['416-929-9577', '438-214-5140']
    re.validate_phone(phones)
