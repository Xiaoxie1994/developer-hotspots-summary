from openai import OpenAI

def summarize_content(key, url, role, content):
    print(f"summarize_content: {url}")
    try:
        client = OpenAI(
            api_key = key,
            base_url = url,
        )
        completion = client.chat.completions.create(
            # 如果传入的文本太大可以调整模型
            model = "moonshot-v1-32k",
            messages = [
                {"role": "system", "content": role},
                {"role": "user", "content": "请协助我对博客内容进行总结，100字以内，博客内容为：" + content}
            ],
            temperature = 0.3
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"【LOG】使用ai总结文章异常: {e}")
    return None