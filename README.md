# developer-hotspots-summary
> 自动汇总并解读热榜内容。通过抓取技术热榜列表数据，并将相关文章内容发送给大模型生成摘要。

## 背景
- 不知道从哪里去获取技术热点信息？
- 工作繁忙没时间了解新知识和技术趋势？
- 近期热点事件老是错过？
- 硬核文章太难或内容太长，没时间深入学习？

## 方案设计 
![方案设计](./picture/image.png)

## 依赖三方API
- [Tophubdata](https://www.tophubdata.com/): 提供热门榜单数据，现成数据不用自己写爬虫（有一定费用开销）；
- [Coze API](https://www.coze.cn/open): 字节跳动推出的一站式AI Bot开发平台，项目中使用的bot（[网页内容理解](https://www.coze.cn/store/bot/7380236432360751123)）支持搜索能力，你也可以在[Coze](https://www.coze.cn/)上定制化自己的bot（目前免费！！！）；
- [Moonshot AI](https://platform.moonshot.cn/): 大模型KIMI的API，不支持搜索能力（有一定费用开销）。

## 使用方式
- 将config-template.yaml重命名为config.yaml，按照诉求修改配置值（添加开放api的key值, 并按照自己需求调整热榜类型）
``` yaml
# 设置执行流开关（可以选择是否执行抓取、摘要生成和最终md生成）
# 执行流程为fetch -> understand -> md
flow:
  fetch: true
  understand: true
  md: true
# 抓取配置
fetch:
  # 抓取类型目前支持 topApi/rss
  type: rss
  config: 
    types:
      - name: 肖恩的杂货店
        url: https://www.shawnxie.top/feed.xml
        num: 5
      - name: 掘金本周最热
        url: https://rsshub.rssforever.com/juejin/trending/all/weekly
        num: 5
# 内容解读配置
understand:
  # 大模型类型，目前支持 kimi、coze
  type: coze
  # 在 https://www.coze.cn/open 申请key
  key: 填写你自己的密钥
  # type: kimi
  # # 在 https://platform.moonshot.cn/console/api-keys 申请key
  # key: 填写你自己的密钥
```
- 运行main.py程序
```
python3 main.py
```
- 在/result文件下获取生成后文档    

## 周刊
目前基于此项目创建了技术周刊，相关内容：
- 个人博客: [肖恩技术周刊](https://www.shawnxie.top/categories/tf-weekly)
- Github: [shawn-weekly](https://github.com/Xiaoxie1994/shawn-weekly)
- 公众号: 肖恩聊技术

<img src="./picture/image-1.png" alt="公众号二维码" width="400">

License
---

This code is distributed under the MIT license. See `LICENSE` in this directory.