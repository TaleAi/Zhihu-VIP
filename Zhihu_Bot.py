from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from markdownify import markdownify


class Bot:
    url = 'https://www.zhihu.com/'
    dir = './'

    def __init__(self, browser):
        self.driver = browser

    def write_contents(self, file, frame):
        sections = frame.find_elements(by=By.XPATH, value='./*')
        for section in sections:
            if section.get_attribute('tag') == 'figure':
                section = section.find_element(by=By.XPATH, value='./img')
            file.write('\n%s' % markdownify(
                section.get_attribute('outerHTML')))

    def get_info(self):
        # Expand Description
        self.driver.find_element(
            by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/span[2]').click()
        # Title
        self.file.write('### %s' % self.driver.find_element(
            by=By.XPATH, value='//*[@id="app"]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/span[2]').get_attribute('innerText'))
        # Author
        self.file.write('\n\n###### 作者：%s' % self.driver.find_element(
            by=By.XPATH, value='//*[@id="app"]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]').get_attribute('innerText'))
        # Genre
        self.file.write('\n\n###### 分类：%s' % self.driver.find_element(
            by=By.XPATH, value='//*[@id="app"]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]').get_attribute('innerText'))
        # Status
        self.file.write('\n\n###### 状态：%s' % self.driver.find_element(
            by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[1]').get_attribute('innerText'))
        # Description
        self.file.write('\n\n\n#### 简介')
        self.write_contents(self.file, self.driver.find_element(
            by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/div/div[2]/div[1]/div[1]/div'))
        print('Info done')

    def get_chapter(self, cnt):
        # Title
        self.file.write('\n\n\n#### %d.%s' % (cnt, self.driver.find_element(
            by=By.XPATH, value='//*[@id="app"]/div/h1').get_attribute('innerText')))
        # Contents
        self.write_contents(self.file, self.driver.find_element(
            by=By.ID, value='manuscript'))
        print('Chapter %d done' % cnt)

    def scroll_and_click(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", element)
        element.click()

    def run(self):
        self.file = open(self.dir + 'test.md', 'w')
        cnt = 0
        try:
            old = self.driver.find_element(by=By.TAG_NAME, value='html')
            self.get_info()
            # Go to chapter 1
            self.scroll_and_click(self.driver.find_element(
                by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div[1]'))
            WebDriverWait(self.driver, 10).until(EC.staleness_of(old))
            while True:
                old = self.driver.find_element(by=By.TAG_NAME, value='html')
                cnt += 1
                self.get_chapter(cnt)
                # Go to next chapter
                try:
                    self.scroll_and_click(self.driver.find_element(
                        by=By.XPATH, value='//*[@id="webNextSection"]/div[1]/span'))
                except:
                    break
                WebDriverWait(self.driver, 10).until(EC.staleness_of(old))
        finally:
            print('Finished %d chapters' % cnt)
            self.file.close()


browser = webdriver.Chrome(service=Service(
    executable_path="chromedriver"))
browser.get(Bot.url)
