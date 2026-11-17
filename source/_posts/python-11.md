---
title: Django 与 DRF
date: 2026-11-11 09:00:00
tags:
  - Django
  - DRF
categories:
  - Django
---

> 我的学习笔记,边学边记,持续修订。

## 📖 HTTP协议与Web框架本质


### 1. HTTP协议特点(基于TCP、无状态、长连接)

**HTTP 是**基于 TCP 的应用层协议**,本身**无状态**;HTTP/1.1 默认通过 keep-alive 复用 TCP 连接,但每次请求的内容仍然相互独立。**

- HTTP 工作在**应用层**,底层依赖 **TCP** 提供可靠传输(默认端口 80,HTTPS 默认 443)
- **无状态**:协议本身不记住上一次请求是谁发的,每次请求相互独立;登录状态是靠 cookie/session 机制额外补充的
- **短连接**:HTTP/1.0 每次请求都新建一条 TCP 连接,用完就断,频繁握手开销大
- **keep-alive(长连接)**:HTTP/1.1 默认开启,一条 TCP 连接可以连续承载多次 HTTP 请求/响应
- 无状态说的是"不保存上下文",长/短连接说的是"TCP 连接怎么复用",两个维度不要混为一谈

### 2. 请求报文与响应报文格式

**请求报文 = **请求行 + 请求头 + 空行 + 请求体**;响应报文 = **状态行 + 响应头 + 空行 + 响应体**,头和体之间必须用空行分隔。**

- 请求行:`GET /index/ HTTP/1.1`,依次是**请求方法、请求路径、协议版本**,用空格分隔
- 请求头:`key: value` 形式,常见有 Host、User-Agent、Content-Type、Cookie、Referer
- **空行**(`\r\n`)表示请求头结束:没有这个空行,服务器无法确定从哪里开始读请求体
- GET 请求通常**没有请求体**,参数拼在 URL 后;POST 请求的数据放在请求体中
- 响应报文:状态行(`HTTP/1.1 200 OK`)+ 响应头(Content-Type 等)+ 空行 + 响应体(HTML/JSON 等实际内容)

### 3. GET 与 POST 的区别、幂等性

**GET 参数在 **URL 查询字符串**里且**幂等**,POST 参数在**请求体**里、一般会改变服务器数据;所谓安全只是"相对"的。**

- POST:数据放在请求体中,不显示在地址栏,大小一般只受服务器配置限制
- **幂等**:同一请求执行一次和执行多次,对服务器数据的影响相同;GET 是幂等的,POST 不幂等(重复提交可能重复建数据)
- **安全是相对的**:POST 只是不显示在地址栏,明文传输下抓包照样能看到,真正的安全靠 HTTPS
- 协议并不禁止 GET 带请求体或 POST 用 URL 传参,但**规范用法**是:取数据用 GET,提交数据用 POST

### 4. 常见状态码与 URL 组成

**200 成功、**301 永久重定向 / 302 临时重定向**、304 缓存、403/404 客户端错误、500 服务器错误;URL = 协议://域名:端口/路径?参数。**

- `200` 请求成功;`304` 资源未修改,浏览器使用本地缓存(属于 3xx,但语义是缓存而不是跳转)
- `301` **永久**重定向,搜索引擎会把收录地址换成新地址;`302` **临时**重定向,原地址以后还会用
- `403` 服务器拒绝执行(权限不够);`404` 找不到资源;`500` 服务器内部代码出错
- URL 组成:`协议://域名:端口/路径?查询参数`,如 `https://www.oldboy.com:8000/courses/?page=2`
- 端口不写时用默认值:http 是 80、https 是 443;多个查询参数用 `&` 连接

### 5. 手写 Web 框架与 wsgiref

**Web 框架的本质四步:**接收请求 → 路由匹配 → 执行视图函数 → 返回响应字符串**;wsgiref 只是把 socket 收发和报文解析封装好了。**

- 最原始做法:socket 监听端口,收到请求后按 `\r\n\r\n` 切分报文,解析出请求路径
- 用字典 `{路径: 函数}` 当**路由表**,比一长串 if-elif 清爽,这就是所有框架路由的雏形
- **wsgiref** 是 Python 内置的符合 WSGI 规范的简易服务器:帮你解析 HTTP 报文成 environ 字典,你只写路由和函数
- 返回响应必须按格式拼:状态行 + 响应头 + 空行 + 响应体,少写空行浏览器就解析不了
- uWSGI、gunicorn 等生产服务器做的也是同一层事:把 HTTP 解析成程序能用的结构,框架只管业务

```python
from wsgiref.simple_server import make_server

def index(environ):
    return "hello index"

def login(environ):
    return "hello login"

routes = {"/index/": index, "/login/": login}   # 路由表

def app(environ, start_response):
    path = environ["PATH_INFO"]                 # 请求路径
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return routes[path]().encode("utf-8")       # 执行函数,返回响应

make_server("127.0.0.1", 8000, app).serve_forever()
```

*wsgiref 版最小 Web 框架*

### 6. MVC/MTV 对应关系与动态页面本质

**Django 采用 **MTV**:Model 管、Template 展示、View 写业务;动态页面的本质就是**字符串替换(模板渲染)**。**

- MVC:Model 负责数据、View 负责展示、Controller 负责调度逻辑
- Django 的 MTV:**M**odel(ORM 操作数据库)、**T**emplate(模板,**对应 MVC 的 View**)、**V**iew(视图函数,**对应 MVC 的 Controller**),外加 urls.py 做路由分发
- 动态页面本质:把 HTML 当模板,**用真实数据替换占位符**后再返回,这个替换动作就叫模板渲染
- 手写框架用 `tpl.replace("{name}", name)`,Django 用模板引擎 `{{ name }}`,原理完全一致
- 静态页面内容永远不变;动态页面同一 URL,不同数据(不同登录人、不同页码)返回不同内容

### 7. 常见请求头与响应头

**请求头是"浏览器的自我介绍":**User-Agent 身份、Referer 来源页、Cookie、Accept 接受类型**;响应头是"服务器的交代":**Content-Type 内容格式、Content-Length 长度、Location 重定向、Set-Cookie 下发 cookie**。**

- `User-Agent`:浏览器与操作系统信息,反爬的第一道关卡(爬虫要伪装 UA)
- `Referer`:请求从哪个页面跳过来的,**防盗链就是校验它**——图片站只允许 Referer 是自己(或白名单)域名的请求
- `Accept` 客户端能接受的内容类型;`Accept-Language` 语言偏好;`Connection: keep-alive` 保持连接;`Cookie` 自动携带浏览器存的 cookie
- `Content-Type`:**告诉对方实体的格式与编码**,如 `text/html; charset=utf-8`、`application/json`、`multipart/form-data`,设置错误会导致乱码或解析失败
- `Content-Length` 响应体字节数;`Location` 配合 301/302 指明跳转地址;`Set-Cookie` 让浏览器种下 cookie
- Django 里用 `request.META` 读请求头:键名转大写、加 `HTTP_` 前缀,如 `HTTP_USER_AGENT`、`HTTP_REFERER`(Content-Type/Content-Length 例外,不加前缀)

```python
def meta_view(request):
    print(request.META.get("HTTP_USER_AGENT"))   # User-Agent
    print(request.META.get("HTTP_REFERER"))      # Referer,直接打开可能没有
    print(request.META.get("CONTENT_TYPE"))      # 请求体格式
    print(request.META.get("REMOTE_ADDR"))       # 客户端 IP
```

*Django 中读取请求头*

### 8. Python 三大主流 Web 框架对比

****Django 大而全**(ORM/模板/admin 全自带)、**Flask 小而精**(核心只管路由视图,其余装扩展)、**Tornado 异步非阻塞**(自带异步服务器,抗高并发长连接)。**

- Django:"重武器",自带 ORM、模板引擎、admin 后台、auth、缓存、中间件等全套组件,开发效率高,适合**大型网站**;学习成本也最高
- Flask:"轻骑兵",核心只提供路由和请求响应,**模板(Jinja2)、ORM(SQLAlchemy)、表单等都按需装第三方扩展**,灵活自由,适合小项目和 API 服务
- Tornado:不仅是个框架还是**异步非阻塞**服务器,单线程事件循环处理高并发,擅长 **WebSocket、长连接、实时推送**类业务
- Django 与 Flask 默认同步处理请求;Tornado 的异步写法(回调/协程)代码风格与两者差异较大
- 选型没有绝对优劣:业务复杂、要后台管理选 Django;轻量灵活选 Flask;高并发实时场景考虑 Tornado

### 9. 代码封装:从单文件脚本到多文件结构

**单文件脚本写完路由和视图后难以维护,按**职责拆分**:路由表放 urls、视图函数放 views、页面模板放 templates 目录,主文件只负责启动服务——这就是 Django 项目结构 urls.py / views.py / templates 的由来。**

- 单文件的痛点:路由、视图、HTML 字符串挤在一起,改一个页面要在几百行里来回找,多人协作互相冲突
- 第一步拆分:**路由字典**单独成文件,把「路径 → 函数」的映射集中管理
- 第二步拆分:**视图函数**单独成文件,只写业务逻辑;返回页面时改为**读取模板文件**再替换占位符,改页面不再动 Python 代码
- 第三步归拢:文件路径拼接、响应体封装这类公共代码提成通用函数,它们最终被框架收编为内置功能
- Django 的目录结构(templates、urls.py、views.py、settings.py)正是这次拆分的标准化结果,理解了拆分过程,项目结构就不用死记

### 10. 简易 Web 请求流程图(手写框架版)

**一次请求的完整链路:**浏览器发请求 → wsgi 服务收报文解析 → 取路径查路由表 → 执行视图(查数据、渲染模板)→ 返回响应字符串 → 浏览器渲染展示**;这是 Django 请求生命周期的基础版。**

- 起点:浏览器按 HTTP 报文格式发出请求,wsgiref 完成 socket 收发与**报文解析**,整理成 environ 结构
- 匹配:框架入口从 environ 取 **PATH_INFO**(请求路径),拿路径到**路由字典**里查找对应视图函数
- 执行:视图按需操作——读取/查询数据 → 读模板文件**替换占位符**生成完整 HTML(动态页面)
- 返回:按「状态行 + 响应头 + 空行 + 响应体」组装后写回 socket,浏览器解析渲染
- 把这张图记熟,后面学 Django 版请求生命周期时,只是在中途插入了中间件和更完整的路由/模板/ORM 组件

## 📖 Django 基础


### 1. 项目创建、目录结构与常用配置

**`django-admin startproject 项目名` 建项目,`python manage.py runserver` 启动开发服务器;新写的 app 必须在 settings 的 **INSTALLED_APPS** 中注册。**

- 创建项目:`django-admin startproject mysite`;创建 app:`python manage.py startapp app01`
- 核心文件:`manage.py` 命令入口、`settings.py` 配置、`urls.py` 总路由、`wsgi.py` 部署入口
- settings 三大常用配置:**INSTALLED_APPS**(注册 app,不注册则模型/模板不生效)、**TEMPLATES**(模板目录)、**DATABASES**(数据库)
- 静态文件:`STATIC_URL = "/static/"` 只是 URL **前缀(别名)**,`STATICFILES_DIRS` 里放**真实存放目录**,两者配合才能找到文件
- admin 后台:`python manage.py createsuperuser` 建管理员,模型类注册到 admin.py 后即可在后台可视化增删改查数据

### 2. 路由系统(include、分组、反向解析)

**urls.py 把 URL 映射到视图;`include` 做**路由分发**;`<int:id>` 是**有名分组**,路由配 `name` 后可用 `reverse` **反向解析**出 URL。**

- 最简路由:`path("index/", views.index)` —— 访问 /index/ 执行 views.index 函数
- **include 路由分发**:总路由 `path("app01/", include("app01.urls"))` 把前缀分给各 app,项目解耦合
- 有名分组:`path("book/<int:id>/", views.detail)`,匹配值以**关键字参数 id** 传给视图;`re_path` 中 `(?P<id>\d+)` 同理
- 无名分组(`re_path` 的 `(\d+)`)以**位置参数**传给视图,可读性差,推荐有名分组
- **反向解析**:路由加 `name="detail"`,代码里 `reverse("detail", kwargs={"id": 7})`,模板里 `{% url "detail" 7 %}`,改路由规则不用改业务代码
- include 分发后的路由想区分不同 app 的同名 name,要配合 `namespace`(app_name)使用,反向解析写成 `"app01:detail"`

### 3. 视图三件套与 request 对象

**视图函数必须接收 `request` 并返回响应:**HttpResponse** 返回字符串、**render** 渲染模板、**redirect** 重定向;请求信息全部从 request 上取。**

- `HttpResponse("内容")`:直接返回一段字符串;`render(request, "xx.html", {"k": v})`:查数据+渲染模板返回完整页面
- `redirect("/login/")`:返回重定向响应(默认 **302**),让浏览器再发一次请求跳到新地址
- `request.method` 请求方式("GET"/"POST");`request.path` 不含参数的路径;`request.body` 原始请求体(字节)
- `request.GET` 取 URL 查询参数、`request.POST` 取表单提交的数据,都是 **QueryDict**,同键多值用 `getlist`
- 三个响应类都在 `django.shortcuts` 里(`HttpResponse` 严格说在 `django.http`),常一起 import

```python
from django.shortcuts import HttpResponse, render, redirect

def book_list(request):
    books = Book.objects.all()                 # ORM 查数据
    return render(request, "list.html", {"book_list": books})

def add_book(request):
    title = request.POST.get("title")          # 取表单数据
    Book.objects.create(title=title)
    return redirect("/books/")                 # 处理完跳回列表页
```

*视图三件套典型用法*

### 4. 模板语法(变量、标签、过滤器、继承)

**`{{ 变量 }}` 输出值,`{% 标签 %}` 写逻辑(for/if);过滤器改显示格式,`extends + block` 实现模板继承,`{% static %}` 引静态文件。**

- 变量:`{{ name }}`、`{{ user.name }}`(点语法万能:字典取键、对象属性、列表索引都能点出来)
- 标签:`{% for book in book_list %}...{% endfor %}`、`{% if 条件 %}...{% else %}...{% endif %}`
- 过滤器:`{{ pub_date|date:"Y-m-d" }}`、`{{ name|default:"匿名" }}`、`{{ lst|length }}`,可以连续 `|` 链式使用
- 继承:base.html 用 `{% block content %}{% endblock %}` 挖坑,子页面开头 `{% extends "base.html" %}` 再用同名 block 填坑
- `{% include "nav.html" %}` 把公共小组件嵌进来;静态文件先 `{% load static %}`,再 `{% static "css/a.css" %}`

### 5. Django 请求生命周期

**一次请求:**中间件 process_request → 路由匹配 → 视图(ORM/模板)→ 中间件 process_response → 返回浏览器**,中间件是进出都要路过的关卡。**

- 浏览器发请求 → wsgi socket 服务器接收并解析成结构化数据 → 交给 Django
- 中间件先干活:process_request 按**注册顺序从上到下**执行,可做登录校验、黑名单拦截(返回 HttpResponse 会短路)
- 路由(urls.py)匹配到视图函数 → 视图操作 **ORM** 拿数据 → **render 把模板渲染成字符串**
- 返回途中:中间件 process_response 按**从下到上**再走一遍 → 组装 HTTP 响应 → 回到浏览器
- 模板渲染和数据库操作都发生在**视图阶段**;中间件决定请求"放不放行"、响应"改不改"

### 6. ORM 基础(字段、迁移、CRUD、双下划线)

**模型类对应表、属性对应字段;改模型后 **makemigrations 生成迁移文件、migrate 执行入库**;查询靠 `filter/all/get`,双下划线做条件与跨表,`F`/`Q` 组合逻辑。**

- 常用字段:`CharField(max_length=32)`(字符串**必须**给 max_length)、`IntegerField`、`DateField`/`DateTimeField`、`ForeignKey`(一对多外键)
- 建表两步:`python manage.py makemigrations`(生成迁移文件)→ `python manage.py migrate`(真正写进数据库)
- 增:`Book.objects.create(title="xx")`;删:`obj.delete()`;改:`Book.objects.filter(id=1).update(price=99)`
- `all()`/`filter()` 返回 **QuerySet**(filter 查不到是空 QuerySet,不报错);`get()` 要求有且只有一条:0 条抛 DoesNotExist,多条抛 MultipleObjectsReturned
- 双下划线条件:`price__gt=100`、`title__contains="py"`、`id__in=[1, 2]`;跨表:对象用 `book.publisher.name`,条件用 `publisher__name="清华社"`
- `values("title")` 得到**字典列表**,`values_list("title")` 得到**元组列表**;`F` 引用字段自身参与运算(自增),`Q` 组合 与/或/非;多对多 `ManyToManyField` 会自动创建第三张表

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.IntegerField(default=0)

# 迁移两步后即可增删改查
Book.objects.create(title="Python入门", price=89)   # 增
Book.objects.filter(price__gt=50).update(price=59)  # 改
Book.objects.filter(id=1).delete()                  # 删
qs = Book.objects.filter(title__contains="Python")  # 模糊查询
```

*模型定义与增删改查*

### 7. JsonResponse 与文件上传

**`JsonResponse` 自动序列化字典并返回 **Content-Type: application/json**;文件上传前端表单必须 **enctype="multipart/form-data"**,后端从 **request.FILES** 取文件,用 chunks() 分块写入。**

- `JsonResponse({"code": 0, "msg": "ok"})`:内部自动 json.dumps,响应头 Content-Type 是 **application/json**,比手写 HttpResponse(json.dumps(...)) 方便
- JsonResponse 默认只允许传 **字典**,想传列表要加 `safe=False`,否则报 TypeError
- 前端:form 的 method 必须 post、**enctype="multipart/form-data"**,少了这个属性文件到不了 request.FILES
- 后端:`file_obj = request.FILES.get("file")`,它有 `.name`(文件名)和 `.chunks()`(分块迭代二进制),也可以直接 `.read()` 一次性读完
- 保存:`with open(file_obj.name, "wb") as f: for chunk in file_obj.chunks(): f.write(chunk)`;文件名建议拼时间戳/uuid 防止重名覆盖

```python
import os
import uuid

def upload(request):
    if request.method == "POST":
        file_obj = request.FILES.get("file")     # 取上传的文件
        name = str(uuid.uuid4()) + os.path.splitext(file_obj.name)[1]
        path = os.path.join("media", name)
        with open(path, "wb") as f:
            for chunk in file_obj.chunks():      # 分块写入,避免大文件撑爆内存
                f.write(chunk)
        return HttpResponse("上传成功")
```

*文件上传视图*

### 8. ORM 必知必会查询方法

**除 all/filter/get/create/update/delete 外必会:**count 计数、order_by 排序(加 - 倒序)、exclude 条件取反、first/last 取单个对象、exists 判断存在、distinct 去重**。**

- `all()/filter()` 返回 **QuerySet 且惰性**:不遍历、不打印就不真正查库;`count()` 直接返回条数
- `order_by("price")` 升序,`order_by("-price")` **降序**;可传多个字段依次排序;`reverse()` 反转已有排序(需配合 order_by)
- `exclude(price__gt=100)`:**条件取反**,查出价格不大于 100 的记录,等价于 filter(price__lte=100)
- `first()/last()` 返回**单个模型对象**(不是 QuerySet),查空表返回 None 不报错;`exists()` 返回 True/False 判断有没有数据,比取全量再判断高效
- `distinct()` 去重:直接调用按整行去重,配合 `values("title")` 就是按 title 字段去重

### 9. 聚合、分组、F 与 Q 查询

****aggregate 整表聚合返回一个字典,annotate 分组统计返回 QuerySet**;`F` 取字段自身的值参与运算,`Q` 用 `|` `&` `~` 组合条件,突破 filter 参数只能 and 的限制。**

- 聚合:`Book.objects.aggregate(Sum("price"))` → `{"price__sum": 120}`,可起别名 `aggregate(total=Sum("price"))`;需先 `from django.db.models import Sum, Avg, Max, Min, Count`
- 分组:`Book.objects.values("publisher__name").annotate(cnt=Count("id"))` 按出版社分组统计书目,**返回 QuerySet,每组一条**,结果含分组字段和统计字段
- F:引用**字段自己**的值参与运算,如 `Book.objects.update(stock=F("stock") - 1)` 库存自减,在 SQL 层完成、并发安全;也可 `filter(sales__gt=F("stock"))` 比较两个字段
- Q:`filter(Q(price__lt=50) | Q(sales__gt=100))` 实现"或";`filter(~Q(id=1))` 取"非";Q 与普通参数混用时,普通参数会 and 到每个 Q 上
- 记忆点:**aggregate 出字典、annotate 出 QuerySet**;filter 多个参数默认 and,Q 负责或/非

```python
from django.db.models import Sum, Count, Avg, F, Q

Book.objects.aggregate(Avg("price"))            # {'price__avg': 88.5}
Book.objects.values("publisher__name").annotate(cnt=Count("id"))
Book.objects.filter(Q(price__lt=50) | Q(sales__gt=100))   # 或
Book.objects.update(sales=F("sales") + 1)                 # 字段自增
```

### 10. choices 参数与多对多的三种创建方式

**字段加 **choices=[(存储值, 显示值)]**,模板里 `get_字段_display()` 取显示值;多对多第三张表三种建法:**全自动 ManyToManyField(推荐)、纯手动自己建表、半自动 through 指定中间表**。**

- choices:`gender = models.CharField(max_length=8, choices=(("male", "男"), ("female", "女")))`,数据库里存 male,页面显示"男"
- 取显示值:对象上 `obj.get_gender_display()`(模板里直接写 `{{ obj.get_gender_display }}`);适合性别、状态、星期等**取值固定**的字段,下拉框数据也能直接用它生成
- 全自动:模型里写 `ManyToManyField(to="Author")`,Django **自动创建第三张表**,支持 `.add()/.remove()/.set()/.clear()` 便捷操作,缺点是第三张表**加不了自定义字段**
- 纯手动:自己建一个含两个 ForeignKey 的中间模型,字段随意加,但**没有 ManyToManyField 的便捷方法和正反向跨表语法**,查询都要手写
- 半自动:`ManyToManyField(to="Author", through="Book2Author")` 指定自己建的中间表:既能正反向跨表查询,中间表也能加字段,但 **add/remove/set/clear 失效**,需手动维护中间表

```python
class Book(models.Model):
    title = models.CharField(max_length=32)
    status = models.CharField(
        max_length=8,
        choices=(("1", "连载中"), ("2", "已完结")),
        default="1",
    )
    authors = models.ManyToManyField(to="Author")   # 全自动第三张表

book.get_status_display()   # '连载中'
book.authors.add(author)    # add/remove/set/clear 只有全自动才有
```

### 11. 伪静态概念与实现

**伪静态把**动态 URL 伪装成静态页面的样子**(如 /article/3.html),路由照常匹配、视图照常查库渲染;目的是迎合搜索引擎 **SEO**、提高收录友好度,页面本质仍是动态生成的。**

- 背景:动态页面 URL 常带 ?id=3 这类查询参数,早期搜索引擎对带参数的 URL 收录不友好,于是把 URL 包装成 .html 结尾
- 实现:路由直接写成 `re_path(r'article/(\d+)\.html', views.detail)`,访问时看起来像打开一个静态文件,实际仍执行视图、查数据库、动态渲染
- 识别:URL 长得像 .html 静态文件,内容却随数据变化(换个 id 内容就变),基本可判定为伪静态;真静态文件内容不会自己变
- 定位:**SEO 只是加分项**,现代搜索引擎已能正常收录动态参数 URL,伪静态更多是历史习惯,别指望它提升真实排名
- 代价与取舍:URL 变长、无实际功能收益;面试常问「什么是伪静态、为什么要用」,答出『动态伪装成静态,为了 SEO』即可

### 12. 自定义过滤器、标签与 inclusion_tag

**模板功能不够用时自己造:app 下建 **templatetags 包**(内含 `__init__.py`),新文件里 `register = template.Library()`,再用 **@register.filter** 定义过滤器、**@register.simple_tag** 定义标签、**@register.inclusion_tag** 定义「带模板的复用组件」;模板里先 `{% load 文件名 %}` 再使用。**

- 准备三步:在**已注册的 app** 下新建 `templatetags` 目录(目录名固定)→ 放一个空的 `__init__.py` 使其成为包 → 新建如 `my_tags.py`,顶部写 `from django import template` 和 `register = template.Library()`
- 自定义过滤器:`@register.filter` 装饰函数(**最多两个参数**),模板里 `{{ value|my_filter:参数 }}` 使用,适合对单个值做简单变换
- 自定义简单标签:`@register.simple_tag` 装饰函数,**参数不限**,模板里 `{% my_tag 参数1 参数2 %}` 调用,适合需要多个入参的场景
- inclusion_tag:`@register.inclusion_tag('xxx.html')` 装饰函数,函数返回的**字典**会作为上下文去渲染指定模板,适合分页条、侧边栏这类**多处复用的 HTML 片段**——写一次,传不同参数到处用
- 使用前必须在模板里 `{% load my_tags %}`(写文件名,不是 app 名);改动自定义代码后记得**重启开发服务器**才生效

### 13. Django 中开启事务

**把多条 ORM 写操作绑成一个整体:**要么全部成功、要么全部回滚**。常用 `from django.db import transaction` 配合 `with transaction.atomic():` 代码块,块内任何异常都会回滚,适合转账、下单扣库存这类多步写操作。**

- 事务四大特性(ACID):**原子性**(多条操作不可拆分)、**一致性**(事务前后数据完整)、**隔离性**(事务之间互不干扰)、**持久性**(提交后永久保存)
- 用法一 with 块:`with transaction.atomic():` 缩进范围内的所有 ORM 写操作同生共死,任何一条抛异常,块内已执行的全部回滚,推荐这种细粒度写法
- 用法二装饰器:`@transaction.atomic` 加在视图函数上,整个函数体是一个事务,粒度较粗,函数里无关的查询也会被卷进来
- 典型场景:A 给 B 转账,`A.balance -= 100` 和 `B.balance += 100` 两条 update 必须捆绑——任何一条失败都整体回滚,绝不能出现钱扣了没到账
- 注意:Django 默认**自动提交**(每条 SQL 立即生效);开启事务后块内代码共享一个连接,块外代码不受事务保护;用 savepoint 可以在块内嵌套局部回滚

### 14. 数据库查询优化(only/defer 与关联查询)

**核心思路:**少查、按需查、一次查**。`only`/`defer` 控制取哪些列,`select_related`/`prefetch_related` 把跨表查询合并,避免循环里反复查库的 **N+1 问题**;QuerySet 惰性,不迭代不查库。**

- QuerySet 是**惰性**的:filter/values 只生成 SQL 不执行,迭代、len()、list()、if qs: 时才真正查库——利用惰性可以先把条件拼好再一次性查询
- **N+1 问题**:循环里逐个访问对象的外键属性,每访问一次发一条 SQL,100 条数据就是 101 条查询,页面直接变慢
- `select_related('外键名')`:基于 **JOIN 一次连表取回**数据,适合**一对多/一对一的正向**关联,之后循环里跨表访问不再额外查库
- `prefetch_related('子表名')`:分两次查询后在 **Python 层做关联**,适合**多对多、反向**查询这类 JOIN 不划算的场景
- `only('id', 'title')` 只取指定列(访问没取的列会再发一条 SQL)、`defer('price')` 排除指定列;列表页用 `values`/`values_list` 直接拿字典/元组,不实例化模型对象,更轻量

## 📖 Django 进阶与 DRF


### 1. cookie 与 session

**cookie 存**浏览器**端、随请求自动携带;session 存**服务端**,靠 cookie 里的 **sessionid** 找回数据,相对更安全。**

- cookie:服务器通过 `resp.set_cookie("k", "v")` 写到浏览器,之后浏览器每次请求同域名**自动携带**
- 取值:`request.COOKIES.get("k")`;可用 `max_age` 设过期时间,不设默认关浏览器就失效
- session:`request.session["user"] = obj` 直接操作,数据默认存在服务端 **django_session 表**,浏览器 cookie 里只存一个 sessionid
- session **依赖 cookie**:浏览器禁用 cookie,默认的 session 机制就失效了
- 对比:cookie 容量小(约 4KB)、在客户端可见可改,**不能放敏感数据**;session 在服务端相对安全,但占服务器存储/内存

### 2. 中间件(五个方法与执行顺序)

**中间件是请求的必经关卡:`process_request` **从上到下**、`process_response` **从下到上**;继承 MiddlewareMixin 实现方法,注册位置决定顺序。**

- 自定义:继承 `MiddlewareMixin`,可实现的五个方法:process_request、process_view、process_response、process_exception、process_template_response
- process_request:请求进来先走,**按 MIDDLEWARE 注册顺序从上到下**;返回 HttpResponse 会**短路**,视图不再执行
- process_response:响应回去之前走,**按注册顺序从下到上**,内部必须 `return response`,否则报错
- process_view 在路由匹配后、视图执行前触发;process_exception 在视图抛异常时触发,可统一兜底
- 注册:把 `"app01.middleware.MyMiddleware"` 加进 settings 的 **MIDDLEWARE** 列表,**写的位置决定执行顺序**

```python
from django.utils.deprecation import MiddlewareMixin

class LogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("请求来了", request.path)

    def process_response(self, request, response):
        print("响应走了")
        return response   # 必须返回 response
```

*最简自定义中间件*

### 3. CSRF 跨站请求伪造

**CSRF = 冒用用户已登录身份发请求;Django 靠 **csrftoken** 防御:表单加 `{% csrf_token %}`,ajax 在请求头带 **X-CSRFToken**,个别视图可用 `csrf_exempt` 豁免。**

- 原理:用户登录了 A 网站,又去访问恶意 B 网站,B 偷偷向 A 发请求,浏览器**自动带上 A 的 cookie**,请求就被当成了用户本人
- Django 防御思路:除了 cookie 还要校验一个攻击者拿不到的 **csrf token**,校验通过才放行(默认开启 CsrfViewMiddleware)
- 表单提交:form 里写 `{% csrf_token %}`,自动生成隐藏的 token 输入框
- ajax 提交:先从 cookie 取出 csrftoken,再放进请求头 **X-CSRFToken** 一起发过去
- 个别接口确实不需要校验(如第三方回调):用 `from django.views.decorators.csrf import csrf_exempt` 装饰该视图,但会降低安全性,慎用

### 4. CBV/FBV 与 ajax

**FBV 是函数视图,CBV 是类视图(`as_view()` 入口、按请求方法分发到 get/post);CBV 加装饰器要用 **method_decorator**;ajax 局部刷新、success 回调处理结果。**

- FBV:`def index(request): ...` 简单直观;CBV:`class Login(View):` 里写 `def get(self, request)`、`def post(self, request)`
- urls 里 CBV 写 `Login.as_view()`;as_view 内部把请求方式转成小写,去类里找同名方法执行
- CBV 加装饰器:`@method_decorator(装饰器, name="get")` 加在**类**上指定方法,或用 @method_decorator 直接加在**方法**上
- $.ajax 常用参数:`url` 请求地址、`type` 请求方式、`data` 参数、`success` 成功回调、`error` 失败回调
- ajax 的价值:**不刷新整个页面**就能与服务器交互,回调里拿到返回数据局部更新页面(前后端分离的基础)

### 5. auth 模块、分页与批量插入

**auth 全家桶:`authenticate` 验密码、`login/logout` 管登录态、`login_required` 限制登录;扩展用户表继承 **AbstractUser**;批量插入用 `bulk_create` 又快又省。**

- `user = auth.authenticate(username=..., password=...)`:验证成功返回用户对象,**失败返回 None**
- `auth.login(request, user)` 把登录态写进 session,之后 `request.user` 就是当前用户;`auth.logout(request)` 退出登录
- `@login_required` 装饰的视图,未登录访问会被重定向到 `settings.LOGIN_URL` 配置的登录页
- 扩展用户:`class UserInfo(AbstractUser)` 加 phone 等字段,settings 配 `AUTH_USER_MODEL = "app01.UserInfo"`,**必须在第一次 migrate 之前定好**
- 分页:简单场景用切片 `[start:end]`,规范做法用 `django.core.paginator` 的 **Paginator** 分页器
- 批量插入:`Book.objects.bulk_create([Book(title=t) for t in titles])`,一条 SQL 插多条,比循环 create 快得多

### 6. DRF 核心(序列化器、视图集、三大组件、JWT)

**DRF(django-rest-framework)做前后端分离接口:**Serializer 负责序列化与校验**,**ModelViewSet + DefaultRouter 自动生成路由**,认证/权限/频率三大组件层层把关。**

- 序列化器:继承 `serializers.ModelSerializer`,用 `fields` 指定字段;`serializer.is_valid()` 校验数据,`serializer.errors` 看错误详情
- 校验钩子:局部钩子 `validate_字段名(self, value)`、全局钩子 `validate(self, attrs)`,不合法就 `raise serializers.ValidationError`
- **APIView** 继承 Django 的 View:请求包装成 DRF 的 **Request**(统一用 `request.data` 取参数),返回 **Response** 自动渲染 JSON
- 视图类演进:APIView 手写逻辑 → GenericAPIView + Mixins 封装查询集 → **ModelViewSet** 一套搞定增删改查五个接口;配合 **DefaultRouter** 自动注册路由
- 三大组件:**Authentication 认证**(你是谁)→ **Permission 权限**(能不能访问)→ **Throttle 频率**(一分钟最多几次),可全局配置也可视图内局部覆盖
- JWT(json web token):登录后签发 token 给前端,之后放在请求头携带认证;与 session 不同,**服务端不存状态**,天然适合分布式和 App/小程序多端

### 7. form 组件(校验、渲染、错误信息、钩子)

**form 组件三大功能:**校验**(`is_valid()` 通过后从 `cleaned_data` 取干净数据)、**渲染标签**(as_p 或 for 循环自动生成 input)、**展示错误**(`errors`;局部钩子 clean_字段、全局钩子 clean 里 raise ValidationError)。**

- 定义:继承 `forms.Form`,字段如 `name = forms.CharField(min_length=2, max_length=8)`,常用参数 required、widget、error_messages(定制中文提示)
- 校验:`form = MyForm(request.POST)`;`form.is_valid()` 全部通过才 True;通过的字段在 `form.cleaned_data`(字典),**没通过校验的字段不进 cleaned_data**
- 渲染:方式一自己手写 input 结构最灵活;方式二 `{{ form.as_p }}` 一键全渲染;方式三 `{% for field in form %}{{ field.label }}{{ field }}{% endfor %}` 逐个渲染
- 错误信息:`{{ form.name.errors.0 }}` 取该字段第一条错误;`error_messages={"required": "不能为空"}` 可以给每种校验失败定制提示文案
- 钩子:**局部钩子 `def clean_name(self)`** 校验单个字段,不合法 `raise forms.ValidationError("提示")`,合法要 `return value`;**全局钩子 `def clean(self)`** 校验字段组合(如两次密码一致),错误用 `self.add_error()` 添加

```python
from django import forms

class RegForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=8)
    pwd = forms.CharField(min_length=6)
    re_pwd = forms.CharField(min_length=6)

    def clean_name(self):                      # 局部钩子:单个字段
        value = self.cleaned_data.get("name")
        if "admin" in value:
            raise forms.ValidationError("名字不合法")
        return value

    def clean(self):                           # 全局钩子:字段组合
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd != re_pwd:
            self.add_error("re_pwd", "两次密码不一致")
        return self.cleaned_data
```

*form 组件:校验 + 双钩子*

### 8. 前后端传输数据的编码格式与 ajax 发送 JSON/文件

**POST 请求体三种编码:**urlencoded(默认,request.POST 可解析)、formdata(文件,进 request.FILES)、json(原样躺在 request.body,request.POST 为空)**;ajax 发 json 用 contentType+JSON.stringify,发文件用 FormData+两个 false。**

- urlencoded:表单默认格式,请求体形如 `name=alex&pwd=123`,Django **自动解析进 request.POST**;GET 的参数永远在 request.GET
- formdata:`enctype="multipart/form-data"` 时使用,普通键值对进 request.POST,**文件对象进 request.FILES**
- json:请求头 `Content-Type: application/json`,Django 默认**不解析**,request.POST 是空 QueryDict,要自己 `json.loads(request.body)`
- ajax 发 json:`$.ajax({ contentType: "application/json", data: JSON.stringify(obj) })`——必须 stringify,否则 jQuery 会按 urlencoded 编码
- ajax 发文件:`var fd = new FormData(); fd.append("file", fileInput[0].files[0]);` 并设置 **`processData: false, contentType: false`**(让浏览器自己处理格式和边界)

```js
// 发送 json
$.ajax({
    url: "/api/",
    type: "post",
    contentType: "application/json",
    data: JSON.stringify({name: "alex", age: 18}),
    success: function (res) { console.log(res); }
});

// 发送文件
var fd = new FormData();
fd.append("file", $("#f1")[0].files[0]);
$.ajax({
    url: "/upload/",
    type: "post",
    data: fd,
    processData: false,   // 不让 jQuery 处理 data
    contentType: false,   // 不手动指定,交给浏览器
    success: function (res) { console.log(res); }
});
```

*ajax 发 json 与文件的标准姿势*

### 9. DRF 过滤、排序与分页组件

**DRF 列表接口三大修饰:**过滤**(按条件筛选)、**排序**(OrderingFilter,参数 ordering)、**分页**(PageNumberPagination,参数 page);支持 settings 全局配置,或视图里 filter_backends / pagination_class 局部覆盖。**

- 排序:视图设 `filter_backends = [OrderingFilter]`、`ordering_fields = ["price", "id"]`,前端 `?ordering=-price`(负号表示倒序)
- 过滤:装 django-filter 后用 DjangoFilterBackend,`filterset_fields = ["category"]`(旧版叫 filter_fields),前端 `?category=python`;内置 SearchFilter 做模糊搜索,前端 `?search=关键词`
- 分页:settings 里 `DEFAULT_PAGINATION_CLASS = "rest_framework.pagination.PageNumberPagination"` + `PAGE_SIZE = 5`,前端 `?page=2` 翻页
- 自定义分页器:继承 PageNumberPagination,重写 `page_size`、`page_size_query_param`(支持 ?size=20 临时改每页条数)等属性,视图里 `pagination_class = MyPager` 局部生效
- 分页响应自动带 `count`(总条数)、`next`、`previous`(上下页链接)和 `results`(数据),前端翻页直接用;三个组件都是"全局兜底、局部覆盖"的配置思路

```python
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination

class MyPager(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"      # ?size=20 临时改每页条数

class BookView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["price", "id"]
    search_fields = ["title"]
    pagination_class = MyPager
```

### 10. Django 缓存机制

**缓存把算过的结果存起来下次直接用:按**粒度**分**全站缓存(两条中间件)、视图缓存(@cache_page)、局部缓存({% cache %} 标签)**,按**存储位置**分内存/文件/Redis/Memcached,在 settings 的 CACHES 里配置。**

- 为什么缓存:页面内容不常变化时,把渲染结果存起来,下次请求直接返回,**省掉数据库查询和模板渲染**的开销
- 全站缓存:MIDDLEWARE 里加两条中间件——`UpdateCacheMiddleware` 放**最上面**、`FetchFromCacheMiddleware` 放**最下面**,全站页面走缓存
- 视图缓存:`from django.views.decorators.cache import cache_page`,视图上加 `@cache_page(60)`,该视图 60 秒内的请求直接返回缓存结果
- 局部缓存:模板里先 `{% load cache %}`,再用 `{% cache 60 sidebar %}...{% endcache %}`,只缓存页面某个片段
- 存储位置:settings 的 CACHES 配置 BACKEND——默认 LocMemCache(本地内存),还有 FileBasedCache(文件)、Memcached、Redis 等,生产环境常用 Redis/Memcached(重启不丢、可分布式共享)
- 注意:数据更新后要**主动清缓存**(或设置较短过期时间),否则用户会一直看到旧数据

```python
from django.views.decorators.cache import cache_page

@cache_page(60)          # 该视图缓存 60 秒
def book_list(request):
    books = Book.objects.all()
    return render(request, "list.html", {"book_list": books})

# settings.py —— 默认本地内存,生产环境可换成 Redis/Memcached
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
```

### 11. Django 自带的序列化组件

**不装 DRF 也能把 QuerySet 转 JSON:`from django.core import serializers`,一句 `serializers.serialize('json', queryset)` 返回 JSON 字符串;但它**格式固定、字段不可定制**,只适合简单场景,复杂需求还是用 DRF 序列化器。**

- 用法:`res = serializers.serialize('json', Book.objects.all())` 直接得到 JSON 字符串,再 `HttpResponse(res, content_type='application/json')` 返回
- 输出结构固定:每条记录被包成 `model`(表名)、`pk`(主键)、`fields`(字段字典)三层,字段无法重命名、无法追加自定义内容
- 它解决的问题:免去「for 循环把对象转字典再 json.dumps」的重复劳动,datetime 等类型也由它处理
- 局限:只能**单向序列化输出**,没有反序列化、没有数据校验、没有字段取舍(source/SerializerMethodField)这些 DRF 能力
- 选型:临时调试、内部简单接口可以用;正式前后端分离项目一律上 DRF 的 ModelSerializer/Serializer

### 12. 基于 django 中间件学习编程思想

**中间件的设计藏着一套通用扩展模式:**配置文件里写「包.模块.类」字符串 → 框架启动时 import_module 反射导入 → 按约定调用固定方法**。框架预留扩展点,使用者只改配置不动源码,这是所有插件式设计的原型。**

- 字符串导入类:Django 启动时逐条读 MIDDLEWARE 列表,用 `importlib.import_module('xx.yy')` 导入模块,再用 `getattr` 取出类并实例化——这是必须掌握的固定套路
- 约定大于配置:框架不管你的类叫什么,只要实现了 process_request / process_response 等方法,就会在对应时机被调用,方法名就是接口约定
- 顺序即逻辑:MIDDLEWARE 列表的书写顺序决定执行顺序,框架只负责循环遍历,把控制权完全交给配置者
- 同款思想遍地都是:DRF 的认证/权限/频率类、缓存 BACKEND、数据库 ENGINE,全部是「配置字符串 + 反射导入 + 约定方法」
- 自己写可扩展代码时照抄三件套:**定义约定 → 提供默认实现 → 允许配置替换**,就能把「改功能」变成「改配置」

### 13. web 开发模式、api 接口与 RESTful 规范

**两种开发模式:**前后端混合**(模板渲染整页)与**前后端分离**(后端只出接口、前端独立部署);接口 = **url + 请求参数 + 响应数据**;RESTful 十条规范约定接口怎么写;**postman** 是不写页面就能模拟发请求的调试工具。**

- 前后端混合:后端用模板渲染出完整 HTML,SEO 友好、部署简单,但前后端耦合在同一项目里,分工效率低
- 前后端分离:后端只返回 JSON,前端(vue/react)独立开发部署,一套接口同时服务 PC / 小程序 / App,是当前主流
- 接口三要素:url(通常带版本,如 /api/v1/books/)、请求方式与参数、响应数据(带状态码和错误提示);postman 里选 method、填 url、填 body 就能直接发请求调试,不必先写前端页面
- RESTful 核心条目:**用名词不用动词**(资源 /books/,动作交给请求方式:GET 查、POST 增、PUT/PATCH 改、DELETE 删)、**版本号**放 url 或请求头、**善用状态码**(200 成功、201 已创建、400 参数错、401 未认证、403 无权限、404 不存在、500 服务器错)、**过滤/分页参数**放查询字符串(?page=1&size=10)、响应里**带错误信息**
- 规范是约定不是强制:团队统一即可;DRF 的 CBV 体系(ModelViewSet + 路由)就是按这套规范设计的落地实现

### 14. DRF 异常处理与自定义 Response 封装

**统一响应格式是团队规范的落点:自定义 Response 类(继承 rest_framework 的 Response)自动带上 **code / msg / data** 三件套;再自定义 **EXCEPTION_HANDLER**,把 APIException、Http404 等异常统一转成同样结构,视图里只管 raise 和 return。**

- 为什么封装:每个视图手写 Response({'code': 0, 'msg': 'ok', 'data': ...}) 重复且易漏,封装成类后一处定义、处处调用
- 自定义 Response:继承 DRF 的 Response,在 `__init__` 里固定塞入 code/msg,常用**类方法**批量生成成功/失败响应;视图里 `return MyResponse(data=qs, msg='查询成功')` 一行搞定
- 异常处理:settings 的 REST_FRAMEWORK 里配 `EXCEPTION_HANDLER = 'api.exceptions.my_exception_handler'`;函数内先判断 `isinstance(exc, APIException)`、`Http404`、`PermissionDenied`,分别转成对应状态码和提示
- 兜底策略:处理不了的异常统一返回「服务器未知错误」并**记录日志**,绝不把异常堆栈直接抛给前端
- 收益:前端只认一种响应结构——按 code 判断成败、msg 做提示、data 取数据,联调成本大幅下降;注意视图内 return 的仍然要经过渲染,Response 封装与异常处理共同构成「响应出口统一」

## 📖 课后作业（DRF接口）


### 1. 作业清单与完成顺序

**DRF 阶段四次作业：**Day82 视图作业**(ModelViewSet+路由) → **Day83 认证作业**(自定义认证类) → **Day84 频率作业**(IP限流) → **Day87 jwt作业**(签发与过期校验)。**

- Day82：books 五大接口 + 自动路由注册
- Day83：登录成功签发 token，自定义认证类校验请求头
- Day84：匿名用户按 IP 限流 3/m
- Day87：多方式登录签发 jwt，过期时间可配置

---
