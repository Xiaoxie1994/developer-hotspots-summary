from openai import OpenAI

def summarize_content(key, url, role, content):
    print(f"summarize_content: {url}")
    try:
        client = OpenAI(
            api_key = key,
            base_url = url,
        )
        completion = client.chat.completions.create(
            model = "moonshot-v1-8k",
            messages = [
                {"role": "system", "content": role},
                {"role": "user", "content": "请协助我对博客内容进行总结，150字以内，内容为：" + content}
            ],
            temperature = 0.3
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"【LOG】使用ai总结文章异常: {e}")
    return None