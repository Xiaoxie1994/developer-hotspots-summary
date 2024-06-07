import fetch, yaml, understand, time, hashlib
import markdown_strings as md

def generate_md5_hash(data):
    md5_hash = hashlib.md5()
    md5_hash.update(data.encode('utf-8'))
    return md5_hash.hexdigest()

# 读取配置文件
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 抓取热榜数据
result = None
fetch_type = config['fetch']['type']
fetch_config = config['fetch']['config']
if fetch_type == 'rss':
    result = fetch.fetch_list_by_rss(fetch_config)
elif fetch_type == 'topApi':
    result = fetch.fetch_list_by_api(fetch_config)
else:
    exit

# 解读热榜数据
date = time.strftime("%Y-%m-%d", time.localtime())
needSummary = config['fetch']['needSummary']
if needSummary:
    ai_type = config['understand']['type']
    ai_key = config['understand']['key']
    for value in result.values():
        for item in value:
            # 调用ai对文章内容总结
            summary = understand.summarize_content(ai_type, item['url'], ai_key)
            print(summary)
            item['summary'] = summary

# 生成结果md
if result:
    contents = []
    file_title = date + '热门文章'
    contents.append(md.header(file_title, 1))
    contents.append(md.blockquote('Power By: [developer-hotspots-summary](https://github.com/Xiaoxie1994/developer-hotspots-summary).    '))
    contents.append(md.blockquote(f"是否生成AI摘要: {needSummary}"))
    for key, value in result.items():
        contents.append(md.header(key, 2))
        table_title = ['文章']
        table_summary= ['摘要']
        for item in value:
            table_title.append(f"[{item['title'].replace("|", "")}]({item['url'].replace(" ", "")})")
            table_summary.append(item['summary'])
        contents.append(md.table([table_title, table_summary]))
    with open('./result/' + file_title + '.md', 'w', encoding="utf8") as file:
        file.write("\n".join(contents))
        