from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta
from time import sleep
from os import system


class Bot:
    url = 'https://web.whatsapp.com'
    status_xpath = '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/header[1]/div[2]/div[2]/span[1]'

    status = ''

    def __init__(self, driver):
        self.driver = driver

    def getStatus(self):
        try:
            return self.driver.find_element(
                by=By.XPATH, value=self.status_xpath).get_attribute('innerText')
        except:
            self.driver.find_element(
                by=By.XPATH, value='/html/body').click()
            return self.status

    def log(self):
        file = open(
            'log.txt', 'a')
        now = (datetime.now()+timedelta(hours=7)).strftime('%H:%M:%S')
        if self.status == 'online':
            msg = '\nOnline at: ' + now
        else:
            msg = 'Offline at: ' + now
        file.write('\n'+msg)
        file.close()
        print(msg)
        return msg

    def alert(self, msg):
        system('/usr/local/bin/terminal-notifier -title "{}" -message "{}" -sound default'.format("Status Alert", msg))

    def run(self, alert=True):
        while True:
            status = self.getStatus()
            if status != self.status:
                self.status = status
                msg = self.log()
                if alert:
                    self.alert(msg)
            sleep(2)


driver = webdriver.Chrome(service=Service(
    executable_path="chromedriver"))
driver.get(Bot.url)