from openai import OpenAI
import fetch, time, requests, json

def summarize_content(type, url, key):
    if type == 'kimi':
        return summarize_content_kimi(url, key)
    elif type == 'cozi':
        return summarize_content_cozi_bot(url, key)
    # 可以扩展更多的ai类型
    # elif type == 'gimini': 
    # elif type == 'openAi':     
    else:
        return None

# 调用kimi api生成摘要
def summarize_content_kimi(url, key):
    try:
        # kimi api暂不支持搜索 需要调用内容抓取
        content = fetch.fetch_article_content(url)
        if content == None : return
        # 调用kimi api生成摘要
        client = OpenAI(
            api_key = key,
            base_url = 'https://api.moonshot.cn/v1',
        )
        completion = client.chat.completions.create(
            # 如果传入的文本太大可以调整模型
            model = "moonshot-v1-32k",
            messages = [
                {"role": "system", "content": "你是Kimi，你擅长对软件开发技术博客进行内容总结。你会为用户提供安全，有帮助，准确的回答。"},
                {"role": "user", "content": "请协助我对博客内容进行总结，150字以内，博客内容为：" + content}
            ],
            temperature = 0.3
        )
        result = completion.choices[0].message.content
        time.sleep(20)  # 注意控制调用频率，免费版为每分钟3次
        return result
    except Exception as e:
        print(f"【LOG】使用ai总结文章异常: {e}")
    return None

# 调用cozi bot api生成摘要
def summarize_content_cozi_bot(url, key):
    try:
        headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': 'api.coze.cn',
            'Connection': 'keep-alive'
        }
        data = {
            "bot_id": "7380233020667789351",
            "user": "肖恩",
            "query": f"{url}",
            "stream": False
        }
        response = requests.post('https://api.coze.cn/open_api/v2/chat', headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_data = response.json()
        print(response_data)
        messages = response_data.get('messages', [])
        for message in messages:
            if message.get('type') == 'answer':
                return message.get('content')
    except Exception as e:
        print(f"【LOG】使用ai总结文章异常: {e}")
    return None   