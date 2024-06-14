import yaml, time, flow
import markdown_strings as md

# 读取配置文件
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

result = None
# 抓取热榜数据
need_fetch = config['flow']['fetch']
if need_fetch:
    fetch_type = config['fetch']['type']
    fetch_config = config['fetch']['config']
    result = flow.fetch_top_hot_list(fetch_type, fetch_config)

# 解读热榜数据
need_understand = config['flow']['understand']
if need_understand:
    ai_type = config['understand']['type']
    ai_key = config['understand']['key']
    result = flow.understan_urls(ai_type, ai_key)

# 生成结果md
need_md = config['flow']['md']
if result is not None and need_md is True:
    contents = []
    file_title = time.strftime("%Y-%m-%d", time.localtime()) + '生成热门文章'
    contents.append(md.header(file_title, 1))
    contents.append(md.blockquote('Power By: [developer-hotspots-summary](https://github.com/Xiaoxie1994/developer-hotspots-summary).    '))
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
        