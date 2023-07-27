from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import re


def make_driver(headless=True):  # 크롬 드라이버를 만듬 False: 드라이버 창을 띄움 True: 드라이버가 백그라운드로 돌아감
    chromedriver_autoinstaller.install(True)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_argument('allow-insecure-localhost')
    # options.add_argument('no-sandbox')
    # options.add_argument('ignore-certificate-errors')
    if headless:
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.get('https://sldict.korean.go.kr/front/main/opinionSend.do?r_type=1')

    return driver


class video:
    def __init__(self, driver):  # 드라이버 인자를 받음
        self.driver = driver

    def finder(self, val, check_count=-1):  # val로 받은 단어를 검색하여 검색한 모든 결과를 2차원 리스트로 반환[[단어, url],[단어, url]]
        """
        :param val:
        :param check_count:
        :return:
        """
        self.driver.find_element(By.CLASS_NAME, 'n_input').clear()
        self.driver.find_element(By.CLASS_NAME, 'n_input').send_keys(val)
        self.driver.find_element(By.CLASS_NAME, 'n_btn_search').click()

        self.driver.execute_script("javascript:fnSearchSignCteList();")
        html = self.driver.page_source
        self.driver.back()
        self.driver.execute_script("javascript:fnSearchSignSpeList();")
        html += self.driver.page_source
        return_list = []
        soup = BeautifulSoup(html, 'html.parser')
        for cnt, li in enumerate(soup.find("div", "wrap_list").find_all('li')):
            if cnt & 1:
                continue
            else:
                video_url = li.find('img', alt="수어사전 동영상")['src'].replace('215X161.jpg', '700X466.webm')
                title = li.find_all('a')[1].text
                title = re.sub(r"[^ㄱ-ㅣ가-힣\s,]", "", title).strip()
                return_list.append([title, video_url])

        return return_list

    def getlength(self, url):  # 동영상의 길이를 얻음
        self.driver.get(url)
        sec = None
        while sec == None:
            sec = self.driver.execute_script("return document.getElementsByName('media')[0].duration")
        return sec
