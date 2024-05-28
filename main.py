import fetch, yaml, json, ai, time
import markdown_strings as md

# 读取配置文件
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 抓取热榜数据
result = {}
baseurl = config['hotList']['url']
key = config['hotList']['key']
hotTypes = config['hotList']['types']
aiUrl = config['ai']['url']
aiKey = config['ai']['key']
aiRole = config['ai']['role']
for type in hotTypes:
    url = baseurl + type['code']
    hotListResult = fetch.fetch_hot_list_content(url, key)
    if hotListResult:
        print(hotListResult)
        needSummary = type['needSummary']
        result[type['name']] = []
        # 每个榜单保留配置num篇文章
        for item in hotListResult['data']['items'][:type['num']]:
            title = item['title']
            contentUrl = item['url']
            summary = item['description']
            if needSummary:
                # 获取文章内容
                content = fetch.fetch_article_content(contentUrl)
                if content:
                    # 调用ai对文章内容总结，注意控制调用频率
                    summary = ai.summarize_content(aiKey, aiUrl, aiRole, content)
                    print(summary)
                    time.sleep(1)
                else:
                    print(f"【LOG】获取文章{title}内容时发生错误。")
            result[type['name']].append({
                'title': title,
                'url': contentUrl,
                'summary': summary
            })
    else:
        print(f"【LOG】请求热榜{type['name']}失败或解析 JSON 数据时发生错误。")
        continue

print(result)
# 生成结果md
if result:
    contents = []
    fileTitle = time.strftime("%Y-%m-%d", time.localtime()) + '热门文章'
    contents.append(md.header(fileTitle, 1))
    contents.append(md.blockquote('Power By: [developer-hotspots-summary](https://github.com/Xiaoxie1994/developer-hotspots-summary).'))
    for key, value in result.items():
        contents.append(md.header(key, 2))
        tableTitle = ['文章']
        tableSummary= ['摘要']
        for item in value:
            tableTitle.append(f"[{item['title']}]({item['url'].replace(" ", "")})")
            tableSummary.append(item['summary'])
        contents.append(md.table([tableTitle, tableSummary]))
    with open('./result/' + fileTitle + '.md', 'w', encoding="utf8") as file:
        file.write("\n".join(contents))
        