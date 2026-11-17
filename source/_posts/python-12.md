---
title: 项目实战
date: 2026-11-12 09:00:00
tags:
  - Django
  - 实战
categories:
  - 项目实战
---

> 我的学习笔记,边学边记,持续修订。

## 📖 选课系统项目(面向对象综合)


### 1. 项目概览与角色设计

**选课系统是**面向对象思想的综合练习**:管理员/学生/老师三种角色,围绕 学校→班级→课程 的层级组织数据。**

- 三种角色功能:管理员(创建学校/课程/老师)、学生(注册/选课/查看分数)、老师(选择教授课程/查看学生/修改分数)
- 核心类:School(学校)、Classes(班级)、Course(课程)、Teacher(老师)、Student(学生)、Admin(管理员)
- 关系:学校与班级**一对多**、班级与课程关联、老师与课程**多对多**、学生选课程后产生分数记录
- 这个阶段还没有数据库,数据持久化用 **json/pickle 文件**保存对象状态

### 2. 登录认证装饰器

**每种角色登录后,后续功能都要先校验身份——用**认证装饰器**统一包裹,避免每个功能里重复写判断。**

- 装饰器内校验当前登录状态(全局字典/文件里是否保存了已登录角色),未登录则强制先登录
- 用 `functools.wraps` 保留被装饰函数的元信息
- 登录成功后把当前用户写入**全局状态字典**,后续功能从状态里取当前用户
- 这是装饰器「不修改原函数代码增加功能」的典型实战应用

```python
from functools import wraps

def auth(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        print("校验登录")
        return fn(*args, **kwargs)
    return inner

@auth
def view():
    return "首页"

print(view())
```

### 3. 反射调度功能

**菜单选择用 if/elif 会越写越长,课程教的是**用反射 getattr 按字符串调度功能**,这是该项目最重要的编程思想。**

- 把功能函数名和菜单文字对应,用户输入后用 `getattr(模块或对象, "函数名")` 拿到函数直接调用
- 配合 hasattr 先判断功能是否存在,避免 AttributeError
- 新增功能只需写函数+注册菜单,**不用改调度逻辑**
- Django 的 CBV 底层也是同样的反射思想,在这里练熟后面看源码就不吃力

```python
class Sys:
    def login(self):
        return "登录页"

obj = Sys()
print(getattr(obj, "login")())   # 按字符串调度方法
```

### 4. 数据持久化与目录规范

**对象数据用 **json/pickle 存到 db 目录**,项目按 软件开发目录规范 组织:src/db/conf/log 各司其职。**

- json 可读性好但只能存基础类型;pickle 能存对象但要小心反序列化安全
- 保存:dump 对象字典;读取:load 后重建对象(或存字典直接用)
- 目录规范:bin 启动、src 核心逻辑、db 数据文件、log 日志、conf 配置、README
- 从根目录运行时用 `os.path` 处理数据文件路径,避免相对路径错乱

```python
import json
data = {"student": ["alex"]}
with open("db.json", "w") as f:
    json.dump(data, f)
with open("db.json") as f:
    d = json.load(f)
print(len(d["student"]))
```

### 5. 三大角色业务流程:注册、选课与成绩

**三条业务主线落地:学生 注册→选学校→选课程(自动生成分数记录)→查看分数;老师 查看教授课程→选择课程→查看课程下学生→修改分数;登录做成**合并登录**,一个入口区分三种角色。**

- 学生主线:注册后先**选择学校**,再从学校的班级里选课程,选课时自动创建一条该生该课的分数记录(初始 0 分),之后随时可查看分数
- 老师主线:先查看自己可选择(教授)的课程列表,选定课程后就能查看课程下的学生并**修改他们的分数**
- 合并登录:一个登录入口按输入的用户名/密码先找到对应角色(管理员/学生/老师),校验通过后按角色进入各自的功能视图
- 选课关系用面向对象表达:学生对象持有课程列表、课程对象记录老师与选课学生,保存时把这张「对象关系网」序列化进 db 目录的文件

```python
class Student:
    def __init__(self, name):
        self.name = name
        self.courses = []

    def choose(self, course):
        if course in self.courses:
            return False          # 重复选课
        self.courses.append(course)
        course.scores[self.name] = 0   # 选课即生成 0 分记录
        return True

class Course:
    def __init__(self, name):
        self.name = name
        self.scores = {}

py = Course("Python")
alex = Student("alex")
print(alex.choose(py), py.scores)
```

## 📖 BBS博客项目(Django综合)


### 1. 项目概览与技术栈

**BBS 是 Django 知识点的**大汇合**:forms 校验、auth 认证、ORM 多表、模板继承、ajax、中间件全部用上。**

- 技术栈:Django + MySQL + Bootstrap + jQuery + ajax + Pillow(验证码) + kindeditor(富文本)
- 开发流程:需求分析 → **表设计**(最关键) → 注册登录 → 个人站点 → 文章详情 → 点赞评论 → 后台管理
- 用户表基于 `AbstractUser` 扩展,settings 里配置 `AUTH_USER_MODEL = "app01.UserInfo"`
- 博客表 Blog 与用户**一对一**,个人站点皮肤/标题存在 Blog 表里

### 2. 数据库表设计(项目最核心一步)

**8 张表把三种关系用全:**一对一**(User-Blog)、**一对多**(Category-Article)、**多对多**(Article-Tag,通过第三张表 Article2Tag)。**

- UserInfo(用户)、Blog(站点)、Category(分类)、Tag(标签)、Article(文章)、Article2Tag(文章标签第三张表)
- ArticleUpDown(点赞点踩:用户+文章+is_up,用户和文章**联合唯一**防重复操作)
- Comment(评论):关联文章和用户,**parent 字段自关联 ForeignKey("self", null=True)** 实现根评论/子评论
- 设计口诀:先确定实体,再找实体间关系,多对多想清楚要不要自定义第三张表(要存额外字段就必须自定义)

### 3. 注册与登录

**注册用 **forms 组件校验** + ajax 提交 + **Pillow 生成图片验证码**;登录用 auth 模块,一个接口同时支持用户名/邮箱/手机号登录。**

- forms 钩子函数做局部/全局校验(如两次密码一致、用户名重复)
- 验证码:一次性随机字符串画到图片上,存 session,提交时与用户输入比对(不区分大小写)
- 头像实时预览:input file 的 change 事件 + FileReader 读图
- 多方式登录:Q 查询把 username/email/phone 三个条件 or 起来,再交给 auth.authenticate

### 4. 个人站点与侧边栏

**每个用户一个个人站点页面,**侧边栏三种筛选**(分类/标签/日期归档)用 inclusion_tag 组件化,一条 ORM 查询带出文章+筛选。**

- 路由支持用户名动态匹配;侧边栏做成 inclusion_tag,三个页面复用
- 日期归档用 `annotate(month=TruncMonth("create_time")).values("month").annotate(c=Count("pk"))` 按月分组计数
- 筛选本质是给文章查询加不同 filter 条件(分类 id / 标签 id / 年月)

### 5. 文章详情、点赞点踩与评论

**点赞点踩和评论都走 **ajax + 事务**;子评论要记录 parent 评论;点赞用联合唯一防止重复。**

- 点赞:先判断是否给自己的文章点赞、是否重复点赞,再**事务包裹**(文章计数+1 与插入点赞记录要么都成功要么都失败)
- 评论提交后 ajax 局部刷新;子评论渲染时带上 @父评论用户
- 文章正文里开事务前先生成简介(截取前 N 个字符),防止标签截断

```python
from django.db import transaction

with transaction.atomic():
    article.up_num += 1
    article.save()
    ArticleUpDown.objects.create(user_id=uid, article_id=aid, is_up=True)
```

### 6. 后台管理与富文本安全

**后台用 kindeditor 写文章,富文本内容**必须做 XSS 清洗**再入库,简介截取前也要先处理标签。**

- XSS 攻击:恶意用户在文章里提交 <script>,别人浏览就执行——**永远不要直接信任用户输入的 HTML**
- 清洗方案:BeautifulSoup 解析,只保留白名单标签(如 p/img/a),其余转义或删除
- 文章简介 = 清洗后正文的前若干字符,避免页面样式错乱
- 媒体文件配置 MEDIA_ROOT/MEDIA_URL,头像等上传文件统一管理

### 7. 导航条、Django admin 与 media 配置

**登录成功后**导航条按 auth 状态渲染**两种样子;Django admin 注册模型即可可视化管理数据;media 配置让头像等上传文件能通过 URL 直接访问,顺带了解图片防盗链思路。**

- 导航条基于 request.user 分支:未登录显示 登录/注册;已登录显示 用户名、修改密码、退出;退出调 auth.logout 清 session 后跳首页
- admin 后台:createsuperuser 建超管 → admin.site.register 注册模型(可配 ModelAdmin 定制列表列/搜索/过滤) → /admin 可视化增删改查
- media 三步:settings 配 MEDIA_ROOT(上传根目录)与 MEDIA_URL → urls 里 static() 把 /media/ 映射到目录 → 模板用 {{ MEDIA_URL }}{{ blog.user.avatar }} 拼路径展示头像
- 图片防盗链:服务端校验请求头 Referer,非本站来源的图片请求拒绝返回,防止自己站点的图片被外链白嫖流量

```python
# settings.py
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# urls.py(调试期暴露媒体目录)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 📖 DRF图书接口项目(RestFramework)


### 1. 项目概览与 RESTful 规范

**围绕图书表写一套**前后端分离的 5 大接口**(查所有/查单条/增/改/删),URL 和方法都遵守 restful 规范。**

- restful 核心:**URL 只表示资源**(名词),**请求方法表示动作**(GET 查 / POST 增 / PUT 改 / DELETE 删)
- 返回统一响应结构 {code, msg, results},前后端只靠 JSON 通信
- 表设计:Book(图书)、Publish(出版社)、Author(作者)、AuthorDetail(作者详情,一对一),图书与作者多对多
- 公共字段抽到 **BaseModel 抽象表**(create_time、is_delete、is_show),其他表继承,配合 filter 过滤

### 2. 序列化器实战

**用 **ModelSerializer** 快速生成序列化器,反序列化走 局部钩子/全局钩子 校验,自定义操作要**重写 create/update**。**

- fields 用 `__all__` 或指定;外键展示用 `source` 或 SerializerMethodField
- 新增图书时要保存多对多作者:**重写 create** 在 context 或序列化器里手动 set 作者
- 批量增删改:many=True 走 ListSerializer,重写 list 方法实现批量更新
- 校验失败抛 ValidationError,DRF 统一转成 400 响应

```python
def validate_title(value):
    if "敏感" in value:
        raise ValueError("书名不合法")
    return value

try:
    validate_title("python入门")
    print("通过")
except ValueError:
    print("拒绝")
```

### 3. 视图集与自动路由

**一个 **ModelViewSet + DefaultRouter** 自动生成 5 大接口路由;自定义接口用 `@action` 装饰器挂在视图集上。**

- ModelViewSet 组合了 list/retrieve/create/update/destroy 五个能力,Router 自动注册 `router.register("books", BookViewSet)`
- queryset + serializer_class 两个类属性是视图集的基础;get_serializer 动态切换序列化类(读用带详情的,写用精简的)
- @action(methods=[GET], detail=False) 生成 /books/xxx/ 自定义接口
- 响应统一用自封装 Response(code/msg/results),配合全局异常处理

### 4. 认证、权限、频率三大组件

**登录用 **jwt 签发 token**,请求头携带 token 走自定义认证类;权限控制不同角色;频率按 ip 限制防刷。**

- jwt 三段式:**header.payload.signature**,签名防篡改,过期时间可配置
- 多方式登录:用户名/邮箱/手机号 Q 查询 + check_password 校验 → 签发 token
- 自定义认证类继承 BaseAuthentication,从 requestMETA 里取 token 校验;权限类控制普通用户/管理员
- 频率:自定义 SimpleRateThrottle 子类,`scope = "ip"`,settings 里配置频率如 `3/m`

```python
import base64
print(base64.b64encode(b"admin").decode())   # jwt 的 payload 段就是 base64 家族编码
```

*base64 编码演示(jwt 组成部分)*

### 5. 分页与接口文档

**列表接口用 **PageNumberPagination 分页**;用 coreapi 自动生成接口文档,前后端对接不再靠嘴说。**

- 分页三件套:page_size、page 查询参数、自定义分页类重写 get_paginated_response 保持统一响应结构
- 批量删除/修改后配合 is_delete 逻辑删除,查询时过滤 is_show
- 接口文档:安装 coreapi,settings 配置,路由挂 OptionalSlashRouter,访问 /docs 查看

### 6. Django 缓存机制

**把「经常读、很少变」的数据放进缓存,省掉重复的数据库查询与渲染:Django 支持多种缓存后端,生产常配 **redis**;视图/接口层用缓存装饰器或 drf 扩展一行生效。**

- 缓存粒度从粗到细:全站缓存(两个中间件)、视图缓存 @cache_page、模板片段 {% cache %}、低阶 API cache.get/set、以及 ORM 查询结果缓存
- 后端在 settings.CACHES 配置:开发用 LocMemCache(进程内存),生产用 django-redis 连 redis 服务
- 低阶 API:cache.set(key, value, timeout) 写、cache.get(key) 读、cache.delete(key) 删;key 按业务命名(如 "book_list:page_2")
- **一致性提醒**:增删改接口成功后要同步 cache.delete 对应 key,否则用户会读到旧数据
- DRF 列表接口可用 drf-extensions 的 CacheResponseMixin 直接缓存响应

```python
from django.core.cache import cache

cache.set("book:1", {"title": "Python入门", "price": 50}, timeout=60)
print(cache.get("book:1"))          # 命中缓存,不再查库
cache.delete("book:1")
print(cache.get("book:1"))          # None(已失效)
```

## 📖 课后作业（项目实战）


### 1. 三大项目作业清单

**项目阶段的作业就是把**三个项目亲手落地一遍**:选课系统(面向对象)→ BBS(Django 全家桶)→ DRF 图书接口(前后端分离),每个项目都有必须独立完成的功能点。**

- 选课系统作业:管理员建校/建课、学生注册选课退课(不能重复选、没选不能退)、老师查看学生改分数 —— 六个类的关系先画图再动手,对应本站「选课系统项目」章
- BBS作业:注册(头像/验证码)、多方式登录、个人站点侧边栏、点赞点踩防重复、评论楼中楼 —— 对应「BBS博客项目」章
- DRF作业:图书五大接口(查所有/查单条/增/改/删)+ 批量逻辑删除 + jwt 登录 —— 对应「DRF图书接口项目」章
- 做项目先跑通主流程再抠细节:表设计 → 路由 → 视图 → 模板/序列化器,每完成一步就 git commit 一次,坏了随时能回
- 做完每个项目,到「题库练习」把对应项目章的题刷一遍,错题进错题本

```python
# 项目作业自查清单(以 DRF 为例)
# [ ] Book/Author 模型建好并迁移
# [ ] 五大接口全部通过 postman 测试
# [ ] 删除走逻辑删除(is_delete=True),列表接口记得过滤
# [ ] 登录用 jwt 签发 token,响应统一 {code, msg, results}
```

*项目落地自查清单*

---
