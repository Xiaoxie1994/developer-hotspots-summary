import fetch, csv, understand

# 抓取热榜数据并暂存
def fetch_top_hot_list(fetch_type, fetch_config):
    # 抓取数据
    result = None
    if fetch_type == 'rss':
        result = fetch.fetch_list_by_rss(fetch_config)
    elif fetch_type == 'topApi':
        result = fetch.fetch_list_by_api(fetch_config)

    if None == result : return
    # 将数据暂存到本地
    filename = "./tmp/output.csv"
    header = ["类型", "标题", "地址"]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 写入表头
        writer.writerow(header)
        # 遍历数据列表，将每个字典写入文件
        for key, values in result.items():
            for value in values:
                writer.writerow([key, value["title"], value["url"]])
    return result

# 解读热榜数据
def understan_urls(ai_type, ai_key):
    # 读取本地暂存数据
    filename = "./tmp/output.csv"
    result = {}
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        # 读取表头
        header = next(reader)
        # 读取数据
        for row in reader:
            key = row[0]
            title = row[1]
            url = row[2]
            # 如果字典中没有这个键，初始化一个空列表
            if key not in result:
                result[key] = []
            # 将读取到的数据添加到列表中
            result[key].append({
                "title": title,
                "url": url
            })

    # 调用ai对文章内容总结
    for value in result.values():
        for item in value:
            # 调用ai对文章内容总结
            summary = understand.summarize_content(ai_type, item['url'], ai_key)
            print(summary)
            item['summary'] = summary
    return result