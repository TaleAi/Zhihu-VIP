from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from markdownify import markdownify
from datetime import date
from uuid import uuid4
from os import mkdir


class Bot:
    url = 'https://www.zhihu.com/'
    timeout = 10

    # Write contents by paragraph within a div
    def write_contents(self, file, frame):
        sections = frame.find_elements(by=By.XPATH, value='./*')
        for section in sections:
            if section.get_attribute('tag') == 'figure':
                # Extract image
                section = section.find_element(by=By.XPATH, value='./img')
            file.write('\n%s' % markdownify(
                section.get_attribute('outerHTML')))

    # Craft info page
    def get_info(self):
        file = open(self.dir + 'info.md', 'w')
        try:
            # Expand Description
            driver.find_element(
                by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/span[2]').click()
            # Title
            file.write('# %s' % driver.find_element(
                by=By.XPATH, value='//*[@id="app"]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/span[2]').get_attribute('innerText'))
            # Author
            file.write('\n\n### 作者：%s' % driver.find_element(
                by=By.XPATH, value='//*[@id="app"]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]').get_attribute('innerText'))
            # Genre
            file.write('\n\n### 分类：%s' % driver.find_element(
                by=By.XPATH, value='//*[@id="app"]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]').get_attribute('innerText'))
            # Status
            file.write('\n\n### 状态：%s' % driver.find_element(
                by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[1]').get_attribute('innerText'))
            # Date
            file.write('\n\n### 存档日期：%s' % date.today().strftime("%Y-%m-%d"))
            # URL
            file.write('\n\n### 原始地址：%s' % driver.current_url)
            # Description
            file.write('\n\n\n## 简介')
            self.write_contents(file, driver.find_element(
                by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/div/div[2]/div[1]/div[1]/div'))
            # Table of contents (to be appended)
            file.write('\n\n\n## 目录')
            print('Info done')
        finally:
            file.close()

    # Append to table of contents in info page
    def append_toc(self, title, filename):
        file = open(self.dir + 'info.md', 'a')
        try:
            file.write('\n- [%s](%s)' % (title, filename))
        finally:
            file.close()

    # Create chapter document
    def get_chapter(self, cnt):
        # Title
        title = '%d.%s' % (cnt, driver.find_element(
            by=By.XPATH, value='//*[@id="app"]/div/h1').get_attribute('innerText'))
        file = None
        # In case title is an invalid filename
        filename = '%s.md' % title
        try:
            file = open(self.dir + filename, 'w')
        except:
            filename = '%d.md' % cnt
            file = open(self.dir + filename, 'w')
        finally:
            self.append_toc(title, filename)
        try:
            # Write title
            file.write('## %s' % title)
            # Write contents
            self.write_contents(file, driver.find_element(
                by=By.ID, value='manuscript'))
            print('Chapter %d finished' % cnt)
        finally:
            file.close()

    # Scroll to an element and click
    def scroll_and_click(self, element):
        driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()

    # Secondary function
    def get_book(self):
        # Set book directory
        self.dir = './contents/%s/' % driver.find_element(
            by=By.XPATH, value='//*[@id="app"]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/span[2]').get_attribute('innerText')
        try:
            mkdir(self.dir)
        except:
            self.dir = './contents/%s/' % uuid4().hex
            mkdir(self.dir)
        # Craft info page
        old = driver.find_element(by=By.TAG_NAME, value='html')
        self.get_info()
        # Create content documents
        cnt = 0
        try:
            # Go to chapter 1
            self.scroll_and_click(driver.find_element(
                by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div[1]'))
            WebDriverWait(driver, self.timeout).until(EC.staleness_of(old))
            # Loop until inner try fails (no more chapters)
            while True:
                old = driver.find_element(by=By.TAG_NAME, value='html')
                self.get_chapter(cnt+1)
                cnt += 1
                # Go to next chapter
                try:
                    self.scroll_and_click(driver.find_element(
                        by=By.XPATH, value='//*[@id="webNextSection"]/div[1]/span'))
                except:
                    break
                WebDriverWait(driver, self.timeout).until(EC.staleness_of(old))
        finally:
            print('Finished %d chapters\n' % cnt)

    # Main function
    def run(self, start=0, finish=0):
        list = driver.find_element(
            by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div[1]/div')
        for i in range(start, finish):
            print('Getting book %d...' % i+1)
            item = list.find_elements(by=By.TAG_NAME, value='a')[i]
            # Scroll to update infinite list
            driver.execute_script("arguments[0].scrollIntoView();", item)
            # Open and switch to new tab
            driver.execute_script("window.open('%s');" %
                                  item.get_attribute('href'))
            driver.switch_to.window(driver.window_handles[-1])
            # Get book
            self.get_book()
            # Close tab and switch back
            driver.close()
            driver.switch_to.window(driver.window_handles[0])


driver = webdriver.Chrome(service=Service(
    executable_path="chromedriver"))
driver.get(Bot.url)
