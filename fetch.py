import requests, feedparser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# 使用聚合api获取热门文章列表
def fetch_list_by_api(config):
    result = {}
    baseurl = config['url']
    key = config['key']
    hotTypes = config['types']
    for type in hotTypes:
        url = baseurl + type['url']
        hotListResult = fetch_hot_list_content(url, key)
        if hotListResult:
            print(hotListResult)
            result[type['name']] = []
            # 每个榜单保留配置num篇文章
            num = type['num'] if 'num' in type else len(hotListResult['data']['items'])
            for item in hotListResult['data']['items'][:num]:
                result[type['name']].append({
                    'title': item['title'],
                    'url': item['url'],
                    'summary': item['description']
                })
        else:
            print(f"【LOG】请求热榜{type['name']}失败或解析 JSON 数据时发生错误。")
            continue
    return result

# 使用RSS获取热门文章列表
def fetch_list_by_rss(config):
    result = {}
    hotTypes = config['types']
    for type in hotTypes:
        hotListResult = parse_rss_feed(type)
        if hotListResult:
            print(hotListResult)
            result[type['name']] = hotListResult
        else:
            print(f"【LOG】请求热榜{type['name']}失败或解析 RSS 数据时发生错误。")
            continue
    return result

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
        text = soup.get_text()
        cleaned_lines = [line.strip() for line in text.splitlines() if line.strip()]
        return '\n'.join(cleaned_lines)
    except Exception as e:
        print(f"【LOG】获取文章内容异常: {e}")
    return None

def parse_rss_feed(type):
    rss_url = type['url']
    print(f"parse_rss_feed: {rss_url}")
    try:
        # 解析 RSS 源
        feed = feedparser.parse(rss_url)

        # 创建一个列表存储结果
        result = []
        # 遍历每个条目，提取标题和链接，并添加到结果列表中
        num = type['num'] if 'num' in type else len(feed.entries)
        for entry in feed.entries[:num]:
            item = {
                'title': entry.title,
                'url': entry.link,
                'summary': entry.description if len(entry.description) <= 200 else None
            }
            result.append(item)

        return result
    except Exception as e:
        print(f"【LOG】获取热门list异常: {e}")
    return None