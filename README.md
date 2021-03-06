# 数据治理、数据标准相关的小工具


随着技术的不断进步，一些大公司、金融行业，很多业务操作都线上化，因而产生的数据就会越来越多，但各业务系统的数据库都是各自为政，数据标准，表字段的命名，元数据都不一样，导致后端的数据加工、数据清洗、数据加工环节比较麻烦，而且由此生产的数据质量问题日益严重。很多公司都发起了数据治理项目，目的是了为统一数据标准，提升数据质量，发挥数据价值。

本人在工作的过程中发现很多系统在建表时都没有一个标准，一个证件类型都有好几套码值，一个身份证号码都有十几种命名方式，导致数据分析、数据加工时多了很多转换和沟通环节。为了解决这个数据库建表不统一的问题，特依据标准词库（自建）来自动生成建表语句，只要大家都使用这个工具，中文字段名一样，那么字段命名，码值都会自动统一。一句话就是标准化建表工具。

由于工作比较繁忙，不保证后续会有更新，如果发现新的问题，后续也许会加入新的功能。如果能帮助需要的人，我就很欣慰了。

### 目前已具有的功能

1. 查询、添加、修改数据标准：包含数据项的中文描述，英文代码，英文全称，码值说明。
2. 生成符合数据标准的建语句：根据提供的中文字段名，依据数据标准生成建表语句。

### 界面展示：

![界面](datastandard.gif)

### 采用的技术栈

都是一些非常好用、高效、流行的库或框架，初学者可以练练手，改成任意你想实现的功能。

1. 后端：Django, Django rest framework，jieba
2. 前段: Vue,  Element-ui, axios 

### 部署步骤

```shell
git clone https://github.com/somenzz/DataStandard.git

cd DataStandard

pip install -r requirements.txt

python manage.py runserver 0.0.0.0:8000

```

然后打开浏览器，在地址栏上输入 ：http://127.0.0.1:8000/std/ 即可看到界面。

**在添加或修改数据标准时需要登陆难**，初始用户名 admin 密码 admin8888，你也可以通过以下命令自行添加用户：

```python
python manage.py createsuperuser
```

### 可以完善的地方

1. 数据标准可以扩展更多属性，如长度，字段类型等，输入一个中文字段名，可以自动选择字段类型，长度，码值等。
2. 添加更多的词条，完善到可以不使用 jieba 分词去组合查询。

### 联系我

微信号: somenzz

关注微信公众号：Python七号

