import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def fetch_hot_list_content(url, key):
    print(f"【LOG】fetch_hot_list_content: {url}")
    try:
        headers = {
            'Authorization': key
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"【LOG】获取热门list异常: {e}")
    return None

def fetch_article_content(url):
    print(f"【LOG】fetch_article_content: {url}")
    try:
        # 设置浏览器选项
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 无头模式，不显示浏览器窗口
        options.add_argument('--disable-gpu')

        # 启动浏览器
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # 获取页面内容
        page_content = driver.page_source
        driver.quit()

        # 解析页面内容
        soup = BeautifulSoup(page_content, 'html.parser')
        return soup.get_text()
    except Exception as e:
        print(f"【LOG】获取文章内容异常: {e}")
    return None