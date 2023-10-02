from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
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


current_path = os.path.dirname(os.path.abspath(__file__))

def check_exists_by_xpath(browser, xpath=None, css=None):
    try:
        if xpath != None:
            browser.find_element(By.XPATH, xpath)
        elif css != None:
            browser.find_element(By.CSS_SELECTOR, css)
    except NoSuchElementException:
        return False
    return True

def delay():
    time.sleep(6)

def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

def validate_phone(phones):

    # for phone in phones:

    options = Options()
    # options.add_argument("--no-sandbox")
    # options.add_argument("--headless")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("start-maximized")
    # options.add_argument('disable-infobars')
    # ua = UserAgent()
    # userAgent = ua.random
    # print(userAgent)
    # options.add_argument(f'user-agent={userAgent}')
    options.add_extension(os.path.join(current_path,'buster.crx'))
    options.add_experimental_option("detach", True)


    browser = webdriver.Chrome(
        executable_path=os.path.join(current_path, "chromedriver"),
        chrome_options=options,
    )

    # set_viewport_size(browser, 1200, 800)

    browser.delete_all_cookies()
    browser.get(
        "https://lnnte-dncl.gc.ca/en/Consumer/Check-your-registration/#!/"
    )


    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "main-title"))
    )
    
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.ID, "phone")
            )
        )
        phone_elem = browser.find_element_by_id(
            "phone"
        )
        phone_elem.clear()
        phone_elem.send_keys(phone)
        
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='submit-container']/button[@class='btn-rounded ng-binding']")
            )
        )
        submit_elem = browser.find_element_by_xpath("//div[@class='submit-container']/button[@class='btn-rounded ng-binding']")
        submit_elem.click()
        time.sleep(1)

        # WebDriverWait(browser, 15).until(
        #     EC.presence_of_element_located((By.XPATH, "//div/div/iframe"))
        # )

        #switch to recaptcha frame
        frames=browser.find_elements_by_tag_name("iframe")
        browser.switch_to.frame(frames[0]);
        delay()
        browser.find_element_by_class_name("recaptcha-checkbox-border").click()

        # #switch to recaptcha audio control frame
        # browser.switch_to.default_content()
        # frames=browser.find_element_by_xpath("//html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
        # browser.switch_to.frame(frames[0])
        # delay()
        # #click on audio challenge
        # browser.find_element_by_id("recaptcha-audio-button").click()
        # #switch to recaptcha audio challenge frame
        # browser.switch_to.default_content()
        # frames= browser.find_elements_by_tag_name("iframe")
        # browser.switch_to.frame(frames[-1])
        # delay()
        # #click on the play button
        # browser.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()

        WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[src^='https://www.google.com/recaptcha/api2/anchor']")))
        delay()
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span#recaptcha-anchor"))).click()
        delay()
        # if check_exists_by_xpath(browser, css="recaptcha challenge expires in two minutes"):
        # print("recaptcha image")
        # browser.switch_to.default_content()
        # delay()
        # WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='recaptcha challenge expires in two minutes']")))
        # delay()
        # WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#recaptcha-audio-button"))).click()
        # delay()

        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@class='ng-pristine ng-invalid ng-invalid-recaptcha']/div[@class='ng-scope']/div[@class='submit-container']/button[@class='btn-rounded ng-binding']"))
        ).click()

        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='register-complete']/div[@class='rc-title ng-binding']"))
        )

        validate_status = browser.find_element_by_xpath("//div[@class='rc-cont']/div[@class='rc-left ng-binding']").text()

        print(validate_status)

        browser.close()

    except ElementNotInteractableException as err:
        print("Element Error: {}".format(err))
        pass
    except NoSuchElementException as err:
        print("NoSuchElement err: {}".format(err))
        browser.close()
        pass
    except TimeoutException as err:
        print("Loading took too much time! {}".format(err))
        validate_phone_err = pd.DataFrame([{phone}])
        validate_phone_err.to_csv(current_path + '/validate_phone_err.csv', mode="a", index=False, header=False)
        # browser.close()
        pass
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    phones = ['416-929-9577', '438-214-5140']
    validate_phone(phones)