# gs-cite-fellow

本项目用来寻找所有引用过某位学者文章的Fellow。

项目流程为

[1] 在该学者 Google Scholar 主页中爬取该学者发表过的所有文章，以及每篇文章的 Google Scholar 引用聚合界面。
[2] 在每篇文章的 Google Scholar 引用聚合界面中，爬取每篇引用文章的标题。
[3] 清洗爬取文章的标题。
[4] 在 DBLP 中并行爬取每篇引用文章对应的作者名。
[5] 合并 DBLP 中并行爬取结果。
[6] 爬取或直接获得 Fellow 列表。
[7] 清洗 Fellow 列表。
[8] 比对每篇引用文章的作者名和 Fellow 列表，输出最后结果。

## 安装环境

```
pip install -r requirements.txt
```

## 代码配置

在 config.json 中添加 scholar_id, 学者的 Google Scholar Id，可以在学者的Google Scholar主页的网址中找到。
在 config.json 中添加 driver_path, 谷歌浏览器驱动地址，谷歌浏览器驱动需和谷歌浏览器版本一致，在网上下载。
## 代码运行

``` bash
# 01  
python 01_article.py

# 02 start_article id 为爬取文章开始编号。期间需要手动验证码
pythn 02_citation.py {{start_article id}}

# 03 
pythn 03_clear.py 

# 04 parallel_count 为总并行数量，建议为8，parallel_id为并行id
pythn 04_author.py {{parallel_id}} {{parallel_count}}
# 若并行数量为8，则需要启动8个，分别为 python 04_author.py {{0..7}} 8

# 05 parallel_count 为总并行数量，与04一致
python 05_merge.py {{parallel_count}}

# 08 
python 08_compare_fellow.py

```
