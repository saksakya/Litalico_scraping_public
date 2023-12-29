from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

class Bs_chrome:
    """_summary_
    クロームを利用して解析用ソースデータ取得
    ※クロームを利用しないと、スクリプトが実行されない。
    """
    def __init__(self, base_url):
        self.base_url = base_url
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        
    def parser(self, sub_url):
        access_url = urljoin(self.base_url,sub_url)
        
        #ドライバを自動でインストールする
        service = ChromeService(ChromeDriverManager().install(), options=self.chrome_options)
        # ブラウザを起動する
        driver = webdriver.Chrome(service=service, options=self.chrome_options)
        #urlアクセス
        driver.get(access_url)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
        # HTMLを文字コードをUTF-8に変換してから取得
        html = driver.page_source.encode('utf-8')
        # BeautifulSoupで扱えるようにパース
        soup = BeautifulSoup(html, "html.parser")
        
        return soup
