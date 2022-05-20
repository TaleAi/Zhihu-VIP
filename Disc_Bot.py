from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


class Bot:
    url = 'https://discord.com/app'
    panel_xpath = '/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]'

    channel_xpath = './div[1]/nav[1]/div[2]/ul[1]'
    channel_name_xpath = './div[1]/a[1]/div[1]/div[2]/div[1]/div[1]/div[1]'

    textbox_xpath = './div[2]/div[2]/main[1]/form[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[last()]'

    def __init__(self, driver):
        self.driver = driver
        self.panel = driver.find_element(by=By.XPATH, value=self.panel_xpath)

    def getChannel(self, name):
        channel_list = self.panel.find_element(
            by=By.XPATH, value=self.channel_xpath).find_elements(by=By.TAG_NAME, value='li')
        for i in range(2, len(channel_list)):
            channel_name = channel_list[i].find_element(
                by=By.XPATH, value=self.channel_name_xpath).get_attribute('innerText')
            if (channel_name == name):
                return channel_list[i].find_element(by=By.XPATH, value='.//a')
        raise Exception('Channel name not found')

    def select(self, name):
        self.getChannel(name).click()

    def msg(self, text):
        textbox = self.panel.find_element(
            by=By.XPATH, value=self.textbox_xpath)
        textbox.send_keys(text)
        textbox.send_keys(Keys.RETURN)


driver = webdriver.Chrome(service=Service(
    executable_path="chromedriver"))
driver.get(Bot.url)