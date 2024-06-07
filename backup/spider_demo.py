from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

url = 'https://juejin.cn/hot/articles/6809637769959178254'

 # 设置浏览器选项
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式，不显示浏览器窗口
options.add_argument('--disable-gpu')

# 启动浏览器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)

# 等待页面加载完成（根据页面复杂度设置适当的等待时间）
time.sleep(5)

# 获取页面HTML
html = driver.page_source

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html, 'html.parser')

# 查找所有文章项
article_items = soup.find_all('a', class_='article-item-link')

# 存储文章数据
articles = []

for item in article_items:
    link = item['href']
    title = item.find('div', class_='article-title').text.strip()
    articles.append({'title': title, 'link': 'https://juejin.cn' + link})

# 输出文章数据
for article in articles:
    print(f"Title: {article['title']}, Link: {article['link']}")

# 关闭浏览器
driver.quit()