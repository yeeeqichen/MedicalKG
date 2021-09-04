# 医疗领域知识图谱构建实战 
![](https://img.shields.io/badge/Python-3.7-brightgreen) ![](https://img.shields.io/badge/py2neo-4.3.0-brightgreen) ![](https://img.shields.io/badge/pymongo-3.12.0-brightgreen) ![](https://img.shields.io/badge/MongoDB-5.0.2%20Community-brightgreen) ![](https://img.shields.io/badge/neo4j-3.5.28-brightgreen) ![](https://img.shields.io/badge/Scrapy-2.5.0-brightgreen) ![](https://img.shields.io/badge/scrapy--splash-0.7.2-brightgreen)
## 项目简介 
此项目基于Scrapy爬虫框架，爬取百度百科中医疗相关数据，使用MongoDB存储解析得到的结构化数据，最后使用neo4j构建知识图谱并进行可视化展示

抛砖引玉，目前项目还处于打磨阶段，后续可以进一步拓宽和深化爬虫的能力，构建更大更完善的知识图谱
## 准备工作 
#### 一、启动MongoDB服务

[MongoDB安装](https://www.mongodb.com/try/download/community)

安装完毕MongoDB后，进入MongoDB安装目录
```shell
cd <你的MongoDB安装目录>
```
随后执行以下命令启动MongoDB服务，其中--dbpath参数指定了数据库存放位置
```shell
./bin/mongod --dbpath data/
```
可以通过以下python脚本测试MongoDB服务是否正确启动：
```python
from pymongo import MongoClient
client = MongoClient('localhost')
print(client)
```
期望得到以下输出：
```angular2html
MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True)
```
#### 二、启动neo4j服务
neo4j需要匹配相应版本的java才能使用，经测试在本项目中可以使用[neo4j Community 3.5](https://neo4j.com/download-center/#community) 和 [Java SE 11](https://www.oracle.com/java/technologies/javase-downloads.html#JDK11) 的组合

可以通过以下方法查看本机的Java版本：
```shell
java --version
```
安装neo4j后，进入neo4j安装目录：
```shell
cd <你的neo4j安装目录>
```
执行以下命令启动neo4j服务：
```shell
./bin/neo4j console
```
测试以及配置neo4j数据库，在浏览器中访问：
```angular2html
localhost:7474
```
若neo4j服务正常启动，则可以进入neo4j的可视化页面，初始用户名与密码均为neo4j，初次登录后会要求**重新设置密码后才可使用**

### 三、启动splash服务

splash能够帮助我们爬取使用JavaScript脚本动态渲染的html页面，百度百科页面大量采用动态渲染机制，因此需要splash帮助我们成功爬取到有用信息

splash依赖于docker部署，[docker安装](http://get.daocloud.io/#install-docker-for-mac-windows), [docker教程](https://blog.csdn.net/qq_39611230/article/details/108641842)

安装完docker后，执行以下命令拉取splash镜像:
```shell
docker pull scrapinghub/splash
```
使用以下docker命令启动splash服务：
```shell
docker run -p 8050:8050 scrapinghub/splash
```
也可以通过docker的可视化界面（如果安装了）来启动splash，点击任务栏中的小鲸鱼即可呼出docker图形界面
## 启动知识图谱构建
启动百度百科爬虫，可以通过调整BaikeMedical.py文件中的start_urls来增加爬取的内容：
```shell
cd MedicalKG
python3 run.py
```
爬取百度百科页面目标区域：
![](https://github.com/yeeeqichen/Pictures/blob/master/%E7%99%BE%E7%A7%91target.png?raw=true)
在MongoDB中查看爬取得到的数据：
![](https://github.com/yeeeqichen/Pictures/blob/master/MongoDB.png?raw=true)
完成数据的爬取操作后，执行脚本进行知识图谱的构建:
```shell
python3 create_KG.py \
  --mongo_url <MongoDB服务访问地址,默认为localhost> \
  --neo4j_url <neo4j服务访问地址,默认为bolt://localhost:7687> \
  --neo4j_name <neo4j数据库用户名> \
  --neo4j_password <neo4j数据库访问密码>
```
可通过访问 localhost:7474来查看知识图谱构建情况：
![](https://github.com/yeeeqichen/Pictures/blob/master/%E7%96%BE%E7%97%85%E4%B8%8E%E4%BC%A0%E6%9F%93%E6%80%A7%E5%8F%8A%E4%BC%A0%E6%92%AD%E9%80%94%E5%BE%84.png?raw=true)
![](https://github.com/yeeeqichen/Pictures/blob/master/%E7%96%BE%E7%97%85%E4%B8%8E%E5%8F%91%E7%97%85%E9%83%A8%E4%BD%8D.png?raw=true)
![](https://github.com/yeeeqichen/Pictures/blob/master/%E7%96%BE%E7%97%85%E4%B8%8E%E7%9B%B8%E5%85%B3%E7%A7%91%E5%AE%A4.png?raw=true)



