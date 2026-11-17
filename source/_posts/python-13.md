---
title: 运维与面试
date: 2026-11-13 09:00:00
tags:
  - 运维
  - 面试
categories:
  - 运维与面试
---

> 我的学习笔记,边学边记,持续修订。

## 📖 Git 与 Linux


### 1. Git 三区模型、基础命令与版本回退

**Git 分**工作区、暂存区、版本库**三个区域,`add` 进暂存区、`commit` 进版本库;`reset --hard` 回退版本,误操作用 `git reflog` 找回。**

- 三区模型:**工作区**(正在编辑的目录)→ `git add` 进**暂存区**(stage)→ `git commit` 进**版本库**(.git 里的提交历史)
- `git init` 初始化本地仓库;`git clone url` 克隆远程仓库(自带全部历史);`git status` 看三区状态,`git diff` 看工作区与暂存区的差异,`git log --oneline` 一行一条看提交历史
- 回退:`git reset --hard 提交id`(或 `HEAD^`、`HEAD~2`)把分支指针移过去,工作区、暂存区、版本库**一起回退**;`--soft` 只动 HEAD、改动留在暂存区;`--mixed`(默认)改动留在工作区
- `git log` 只显示**当前分支可达**的提交;回退后「消失」的提交用 **`git reflog`**(记录 HEAD 每一次移动)查到 id,再 reset 回去即可找回
- 丢弃某个文件的工作区修改:`git checkout -- 文件名`;提交说明要写清楚改动内容,方便日后回溯

```python
git add .                        # 工作区 -> 暂存区
git commit -m "修复登录bug"       # 暂存区 -> 版本库
git reset --hard a1b2c3d         # 回退到指定提交
git reflog                       # 记录 HEAD 每次移动,可找回提交
```

*三区流转与回退速查*

### 2. 分支与合并冲突

**分支是**平行开发线**:`checkout -b` 创建并切换,`merge` 合并;两个分支改了**同一处代码**才会冲突,手动解决后 add、commit。**

- `git branch` 查看、`git branch dev` 创建、`git checkout dev` / `git switch dev` 切换、`git checkout -b dev` 创建并切换、`git branch -d dev` 删除分支
- 习惯:master 保持稳定,功能开发在 dev/feature 分支上做,完成后 `git merge dev` 合并回去
- 从同一提交分叉后合并会产生一个**合并提交**(有两个父提交);快进合并(fast-forward)只在 master 没有新提交时发生
- 冲突的必要条件:两个分支改了**同一行代码**;冲突时文件里出现 `<<<<<<< HEAD`、`=======`、`>>>>>>> dev` 三对标记,`git status` 中该文件显示 both modified
- 解决冲突四步:打开文件手动保留想要的代码 → 删掉标记行 → `git add 文件` → `git commit` 完成合并

```python
git checkout -b dev      # 创建并切换到 dev
# ...开发、提交...
git checkout master
git merge dev            # 把 dev 合并进 master
git branch -d dev        # 删除已合并的分支
```

### 3. 远程协作与 .gitignore

**`push` 推送、`pull` 拉取(**fetch+merge**)、`fetch` 只下载不合并;认证用 **SSH key 或 token**;`.gitignore` 忽略不该提交的文件。**

- `git remote add origin url` 关联远程仓库(github/gitee 用法一致);首次推送 `git push -u origin master` 并建立跟踪关系
- `git pull` = **fetch + merge**:fetch 只把远程新提交下载到本地仓库(不动工作区,更安全),pull 下载后直接尝试合并进当前分支
- 认证:HTTPS 方式推送用**用户名 + token**(github 已禁止密码);SSH 方式先 `ssh-keygen` 生成密钥对,把**公钥**粘贴到平台的 SSH 设置里
- 多人协作习惯流程:开工先 `pull` 拉最新 → 本地开发并提交 → `push`;push 被拒绝说明远程有新提交,先 pull(必要时解决冲突)再推
- `.gitignore` 声明不纳入版本控制的文件:`*.pyc`、`.idea/`、`venv/`、日志文件;**数据库密码等敏感配置绝不能提交**上去

```python
# .gitignore 示例
*.pyc
__pycache__/
.idea/
venv/
*.log
.env
```

### 4. Linux 常用命令与权限
**目录文件记牢 `ls -l`、`mkdir -p`、`rm -rf`、`cp`、`mv`;查日志 `tail -f`、过滤 `grep` 配合管道 `|`;进程 `ps aux`/`top`/`kill`;`chmod 755` = 所有者 rwx、组和其他人 r-x。**

- 浏览定位:`pwd` 当前路径、`ls -l` 详细列表、`cd` 切换目录;`which` / `whereis` 查命令的安装位置;`useradd` 创建用户
- 文件操作:`mkdir -p a/b/c` 递归创建、`cp` 复制、`mv` 移动/重命名、`rm -rf` 强制递归删除(**高危命令,回车前看清路径**)
- 查看内容:`cat` 看小文件、`less` 分页翻大文件、`tail -f app.log` **实时追踪**日志新增
- 文本与管道:`grep 关键词 文件` 过滤;管道 `|` 把左边命令的输出交给右边处理,如 `ps aux | grep python`;`ps aux` 进程快照、`top` 实时动态、`kill -9 进程号` 强杀
- 压缩:`tar -zcvf x.tar.gz 目录` 打包压缩、`tar -zxvf x.tar.gz` 解压
- 权限:r=4、w=2、x=1,三位分别对应**所有者/同组/其他人**;`chmod 755` = 所有者 rwx(7)、同组 r-x(5)、其他人 r-x(5)

```python
tar -zxvf app.tar.gz          # 解压 .tar.gz
ps aux | grep python          # 找 python 进程
kill -9 12345                 # 强制结束进程
chmod 755 start.sh            # 所有者 rwx,组和其他人 r-x
tail -f app.log               # 实时追踪日志
```

*运维常用命令速查*

### 5. vim 三种模式与部署基础
**vim 有**命令、插入、末行**三种模式:`i` 进插入、`Esc` 回命令、`:wq` 保存退出;部署常见组合 **nginx 反向代理 + gunicorn/uwsgi**,后台挂起用 `nohup ... &` 或 `screen`。**

- **命令模式**(打开文件默认):yy 复制行、p 粘贴、dd 删行、u 撤销、G 跳到末尾;按 `i` / `a` / `o` 进入**插入模式**才能输入文字,Esc 退回命令模式
- **末行模式**(按 `:` 进入):`:w` 保存、`:wq` 保存退出、`:q!` 不保存强制退出、`:set nu` 显示行号
- nginx **反向代理**:请求先到 nginx,由它转发给后端应用,客户端感知不到后端;顺带做静态文件托管和**负载均衡**
- gunicorn / uwsgi 是 **WSGI 服务器**,真正负责运行 Python web 应用;典型组合:nginx(80 端口)→ gunicorn/uwsgi → Django/Flask
- 后台运行:`nohup python xxx.py &`(退出终端不中断,输出写入 nohup.out);`screen` 可以开一个会话挂起(detach),断线后 attach 回来任务还在跑

```python
# vim:yy 复制行  p 粘贴  dd 删行  u 撤销  :wq 保存退出  :q! 强制退出

# 部署链路:nginx(80端口) -> gunicorn/uwsgi -> Django
nohup python manage.py runserver 0.0.0.0:8000 &   # 后台启动,输出写 nohup.out

screen -S deploy      # 新建名为 deploy 的会话
# Ctrl+A 再按 D:挂起会话;screen -r deploy:恢复
```

*vim 与部署常用操作*

## 📖 爬虫基础


### 1. 爬虫流程与 requests 发请求
**爬虫四步:**发起请求 → 获取响应 → 解析 → 存储**;requests 中 `params` 拼 URL 参数、`data` 提交表单,`text` 是 str、`content` 是 bytes。**

- 四步流程:模拟浏览器发 HTTP 请求 → 拿到 HTML/JSON 响应 → 用解析库提取目标字段 → 存到文件或数据库
- `requests.get(url, params=字典)` 把参数拼到 URL 问号后面;`requests.post(url, data=字典)` 把表单放进请求体(登录、提交常用)
- 伪装浏览器:`headers` 里放**User-Agent** 浏览器 UA 字符串,否则默认 UA(python-requests)很容易被识别拦截
- `response.text` 返回 **str**(按编码解码后的字符串),`response.content` 返回 **bytes**(存图片、视频用它,或自己 `.decode()`)
- `response.status_code` 判断结果:200 成功、404 资源不存在、403 被拒绝、5xx 服务器错误;加 `timeout=3` 防止卡死,超时抛异常

```python
import requests

url = "https://www.example.com/search"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
r = requests.get(url, params={"wd": "python"}, headers=headers, timeout=3)
print(r.status_code)    # 200
print(r.url)            # https://www.example.com/search?wd=python
```

### 2. 会话保持:Session 与 cookie
**`requests.Session()` 会**自动保存并携带 cookie**,登录一次后,后续请求自动带上,实现会话保持。**

- HTTP 本身无状态,服务器靠 cookie 识别「你是谁」;直接用 requests 每次请求都是「新面孔」
- `s = requests.Session()`,之后用 `s.get` / `s.post` 发请求:登录接口返回的 Set-Cookie 自动保存,下次请求自动携带
- 典型场景:需要登录的网站——先 post 登录接口,再用同一个 Session 访问只有登录后才能看的页面
- 也可以手动携带:`requests.get(url, cookies=cookie字典)`,但 Session 方式更省心

```python
import requests

s = requests.Session()
s.post("https://example.com/login", data={"user": "py", "pwd": "123"})
r = s.get("https://example.com/user")   # 自动携带登录后的 cookie
```

### 3. 解析方式:bs4 / xpath / 正则 / json
**HTML 用 **bs4 或 xpath** 解析,接口返回的 JSON 直接 `r.json()` 转字典取字段,正则适合提取有固定规律的文本。**

- bs4:`soup.find("div", class_="box")` 找第一个、`find_all("a")` 找全部返回**列表**、`tag.get_text()` 取文本、`tag.get("href")` 取属性
- bs4 的 css 选择器:`soup.select("div.box > a")`,同样返回列表,元素还要 `.get_text()`
- xpath(lxml):`//div[@class="box"]/a/@href` 中 `//` 表示任意层级、`@` 取属性、`contains(@class, "box")` 模糊匹配、`/text()` 取文本
- 接口数据:`r.json()` 把 JSON 响应直接转成 dict/list,再按键取值,比解析 HTML 干净得多
- 正则:`re.findall(r'模式', html)`,注意贪婪 `.*` 与非贪婪 `.*?` 的区别,爬虫里绝大多数情况用非贪婪

```python
from bs4 import BeautifulSoup

html = '<div class="box"><a href="/1">一</a><a href="/2">二</a></div>'
soup = BeautifulSoup(html, "html.parser")
print(len(soup.find_all("a")))       # 2
print(soup.select("div.box a"))      # css 选择器
print(soup.find("a").get("href"))    # /1
print(soup.find("a").get_text())     # 一
# xpath 等价写法://div[@class="box"]/a/@href
```

### 4. 反爬手段与应对策略
**常见反爬:**UA 检测、IP 封禁、频率限制、验证码、cookie 校验**;应对思路是把自己伪装成正常用户:UA 池、代理池、限速、遵守 robots 协议。**

- UA 检测:服务器检查 User-Agent → 维护 UA 列表,每次请求**随机换**(UA 池)
- IP 封禁:同一 IP 请求过多被封 → **代理池**,用 `proxies={"http": "ip:port"}` 换出口 IP
- 频率控制:请求太快被限制 → `time.sleep(random.uniform(1, 3))` 随机间隔,既是礼仪也是自保
- 验证码与 cookie 校验:复杂验证码可借助打码平台;有些接口校验 cookie/token,要先访问页面拿到合法 cookie 再发请求
- **robots 协议**:网站根目录 `/robots.txt` 声明哪些内容允许抓取,属于行业规范(君子协定),爬之前先看一眼

```python
import time, random
import requests

UA_LIST = ["Mozilla/5.0 (Windows NT 10.0)", "Mozilla/5.0 (Macintosh)"]
headers = {"User-Agent": random.choice(UA_LIST)}
proxies = {"http": "http://113.200.0.1:8000"}   # 代理池取出的 ip:port
r = requests.get("https://example.com", headers=headers, proxies=proxies, timeout=3)
time.sleep(random.uniform(1, 3))   # 随机限速
```

### 5. scrapy 框架:架构与运行
**scrapy 五大组件:**Engine(引擎)、Scheduler(调度器)、Downloader(下载器)、Spider(爬虫)、Pipeline(管道)**,项目目录里 `scrapy crawl 爬虫名` 运行。**

- 数据流:Engine 是总指挥;Scheduler 负责请求**排队去重**;Downloader 负责下载;Spider 写解析逻辑;Pipeline 负责**清洗和存储**;下载中间件、爬虫中间件可拦截加工请求与响应
- 入口:`start_urls` 列表里的地址会被自动请求,响应交给 `parse(self, response)` 方法解析
- 翻页/跟进:在 parse 里 `yield scrapy.Request(下一页url, callback=self.parse_detail)`(或 `response.follow`)把新请求交回引擎继续调度
- 运行:项目目录下 `scrapy crawl 爬虫名`;想直接存文件可以加 `-o data.json`
- settings 常用:`ROBOTSTXT_OBEY = True` 遵守 robots、`DOWNLOAD_DELAY = 2` 下载间隔、`USER_AGENT` 设 UA;开启管道要在 `ITEM_PIPELINES` 里注册
- **CrawlSpider**:通过 Rule(LinkExtractor + callback)自动跟进符合规则的链接,适合全站批量爬取

```python
import scrapy

class JobSpider(scrapy.Spider):
    name = "job"
    start_urls = ["https://example.com/list"]

    def parse(self, response):
        for item in response.css("div.item"):
            yield {"title": item.css("h3::text").get()}
        next_url = response.css("a.next::attr(href)").get()
        if next_url:
            yield response.follow(next_url, callback=self.parse)

# 项目目录下运行:scrapy crawl job
```

## 📖 综合面试高频


### 1. is 和 == 有什么区别?

****`==` 比较值是否相等,`is` 比较是否是同一个对象**(内存地址是否相同)。**

- `==` 调用对象的 `__eq__` 方法比较内容;`is` 比较 `id()` 是否相同
- `a = [1,2]; b = [1,2]`:`a == b` 为 True,`a is b` 为 False(两个不同列表)
- 小整数池(-5~256)和字符串驻留会让个别 `is` 也返回 True,这是实现细节,**不要依赖**
- 判断 None 的规范写法是 `if x is None`

```python
a = [1, 2]
b = [1, 2]
print(a == b, a is b)   # True False
```

### 2. 深拷贝和浅拷贝的区别?

**浅拷贝只复制**第一层**,嵌套的可变对象仍然共享;深拷贝 `copy.deepcopy` **递归复制所有层**,完全独立。**

- `copy.copy()`:产生新对象,第一层是新的,但里面的子对象还是**引用**
- `copy.deepcopy()`:递归复制每一层,拷贝后互不影响
- `b = a` 既不是浅拷贝也不是深拷贝,只是给同一个对象起了个别名
- 不可变元素(int/str/tuple)拷不拷贝都共享,不会产生副作用

```python
import copy
a = [1, [2, 3]]
b = copy.copy(a)
c = copy.deepcopy(a)
a[1].append(4)
print(b)   # [1, [2, 3, 4]] 浅拷贝内层共享
print(c)   # [1, [2, 3]] 深拷贝完全独立
```

### 3. Python 函数传参是传值还是传引用?

**都不是,是**传对象引用(共享传参)**:函数内能修改传入的**可变对象**,对**不可变对象**重新赋值只影响函数内部。**

- 形参拿到的是实参所引对象的引用,不是复制品
- 传 list/dict/set:函数内 append、修改会**影响外部**
- 传 int/str/tuple:函数内重新赋值只是让形参指向新对象,外部不变
- 经典坑:可变默认参数 `def f(x, lst=[])` 只在定义时创建一次,多次调用共享同一个列表;推荐默认写 None 再在函数内创建

### 4. *args 和 **kwargs 是什么?
**`*args` 把多余的位置参数打包成 **tuple**,`**kwargs` 把多余的关键字参数打包成 **dict**,让函数能接受任意参数。**

- `def f(a, *args, **kwargs)`:调用 f(1, 2, 3, x=4) 时 a=1、args=(2,3)、kwargs={'x':4}
- 调用时 `*lst` / `**d` 是反向操作:**解包**再传参
- 装饰器的万能签名就是 `def wrapper(*args, **kwargs)`
- 参数顺序:位置参数 → `*args` → 默认/关键字参数 → `**kwargs`

```python
def f(a, *args, **kwargs):
    print(a, args, kwargs)

f(1, 2, 3, x=4)   # 1 (2, 3) {'x': 4}
```

### 5. GIL 是什么?多线程和多进程怎么选?
**GIL 是 CPython 的**全局解释器锁**,同一时刻只有一个线程执行字节码;选型口诀:**CPU 密集用多进程,IO 密集用多线程/协程**。**

- GIL 保证同一进程内同一时刻只有一个线程执行 Python 字节码,所以多线程**无法利用多核并行计算**
- 线程在等待 IO(网络、磁盘、sleep)时会**释放 GIL**,所以 IO 密集任务多线程依然有效
- CPU 密集(大量计算)→ `multiprocessing` 多进程,每个进程有独立解释器和 GIL
- 协程(asyncio)单线程内切换,适合超高并发的网络 IO 场景
- 面试一句话:计算多开进程,IO 多开线程/协程

### 6. 手写一个装饰器
**装饰器本质是**接收函数、返回新函数的高阶函数**,用 @ 语法在不改原函数的前提下加功能;通用模板要加 `functools.wraps`。**

- 结构:外层函数接收被装饰函数,内层 wrapper 完成附加逻辑后调用原函数并返回结果
- 装饰时机:`@timer` 在**函数定义时**执行,之后的函数名实际指向 wrapper
- `@functools.wraps(func)` 保留原函数的 `__name__`、`__doc__` 等元信息
- 常见应用:计时、日志、登录校验、缓存;带参数的装饰器再包一层(三层函数)

```python
import functools, time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(func.__name__, "耗时", time.time() - start)
        return result
    return wrapper

@timer
def work():
    time.sleep(1)

work()
```

### 7. 迭代器和生成器有什么区别?
**迭代器是实现了 **`__iter__` 和 `__next__`** 的对象;生成器是**用 yield 写出来的迭代器**,惰性求值、省内存。**

- 可迭代对象(Iterable)有 `__iter__`,能被 for;迭代器(Iterator)还要有 `__next__`,for 的本质就是不断调 next
- 生成器:函数里含 `yield`,调用它返回生成器对象;或写生成器表达式 `(x*2 for x in range(10))`
- 惰性求值:用一次算一次,不一次性把数据装进内存,适合大文件、大数据流
- 生成器只能遍历一次,耗尽后再 next 会抛 StopIteration
- `iter(lst)` 可以把列表变成迭代器;list/str/range 都是可迭代对象

### 8. Python 的内存管理与垃圾回收机制?
**以**引用计数**为主,辅以**标记-清除**解决循环引用、**分代回收**提升效率;引用数归零的对象立即释放。**

- 引用计数:每个对象记录被引用的次数,`del` 或离开作用域使计数减 1,**减到 0 立刻回收**
- 缺陷:循环引用(a 引用 b、b 引用 a)计数永不为 0 → **标记-清除**:从根对象出发标记可达对象,清除不可达的
- **分代回收**:0/1/2 三代,新对象在 0 代,经历扫描仍存活就升代,代数越高扫描频率越低
- 小整数池、字符串驻留(intern)减少重复创建对象
- 查看引用计数:`sys.getrefcount(x)`(结果比实际大 1,因为传参本身临时引用了一次)

### 9. 闭包是什么?内层函数能修改外层变量吗?

**闭包 = **内层函数引用了外层函数的变量**并被打包返回;内层修改外层变量需要 **nonlocal**,修改全局需要 **global**。**

- 闭包三要素:函数嵌套、内层引用外层变量、外层把内层函数作为返回值
- 作用域查找顺序 **LEGB**:Local → Enclosing → Global → Built-in
- 内层**读取**外层变量可以直接读;**赋值**会被 Python 当成新的局部变量 → 用 `nonlocal x` 声明才能修改
- 经典坑:循环里创建的闭包是**晚绑定**,全部读到循环变量的最终值;用默认参数 `lambda i=i: i` 固定当时的值
- 装饰器就是闭包的典型应用

```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)          # 闭包晚绑定
print([f() for f in funcs])          # [2, 2, 2]

funcs2 = []
for i in range(3):
    funcs2.append(lambda i=i: i)     # 默认参数固定当时的值
print([f() for f in funcs2])         # [0, 1, 2]
```

### 10. list 和 dict 常见操作的时间复杂度?
**list 按索引取、尾部增删是 **O(1)**,查找和中间插删是 **O(n)**;dict 基于哈希表,查、增、删平均都是 **O(1)**。**

- list:`lst[i]` 取值 O(1);`x in lst` 查找、`insert(0, x)`、删除中间元素 O(n);`append` 和 `pop()` 尾部操作 O(1)
- dict/set:基于**哈希表**,取值、赋值、`in` 判断、增删平均 O(1),哈希冲突严重时退化 O(n)
- 优化点:频繁判断「元素在不在」用 set/dict,别用 list——把 O(n) 变 O(1)
- tuple 不可变,遍历复杂度与 list 相同

### 11. 手写列表去重(保持原顺序)与排序
**去重保序用「遍历 + set 记录 seen」或 `list(dict.fromkeys(lst))`;`list(set(lst))` 去重快但**不保序**;`sorted()` 返回新列表,`lst.sort()` 原地排序。**

- `list(set(lst))`:一行去重,但 set 无序,**顺序会乱**
- 保序去重:遍历原列表,用 set 记录见过的元素,没见过就追加(seen 查找 O(1),整体 O(n))
- 一行保序写法(py3.7+ dict 保序):`list(dict.fromkeys(lst))`
- 排序:`sorted(lst)` 返回**新列表**,`lst.sort()` **原地**修改;`key=` 指定依据,如 `key=len`、`key=lambda x: x[1]`,`reverse=True` 降序

```python
lst = [3, 1, 3, 2, 1]
print(list(set(lst)))            # [1, 2, 3] 顺序可能乱
print(list(dict.fromkeys(lst)))  # [3, 1, 2] 保序去重
print(sorted(lst, reverse=True)) # [3, 3, 2, 1, 1]
```

### 12. 简述 TCP 三次握手和四次挥手
**三次握手建立连接(**SYN → SYN+ACK → ACK**),四次挥手断开(**FIN → ACK → FIN → ACK**),挥手多一次是因为 ACK 和 FIN 要分开发。**

- 握手目的:确认双方收发能力都正常、同步初始序列号,防止失效的连接请求浪费资源
- 握手过程:客户端发 SYN → 服务端回 SYN+ACK → 客户端再回 ACK,连接建立
- 挥手过程:主动方发 FIN → 被动方回 ACK → 被动方数据发完再发 FIN → 主动方回 ACK
- 为什么四次:被动方收到 FIN 时可能还有数据没发完,先回 ACK,等发完才发 FIN,两次只能分开
- 主动方最后进入 **TIME_WAIT** 状态等待 2MSL,确保最后一个 ACK 丢失时还能重发

### 13. TCP 和 UDP 的区别?
**TCP **面向连接、可靠传输、字节流、有拥塞控制**;UDP **无连接、不可靠、数据报、开销小延迟低**。**

- TCP:三次握手建立连接,有确认重传、排序、流量/拥塞控制,适合网页(HTTP)、文件传输、邮件
- UDP:不握手直接发,不保证到达和顺序,头部只有 8 字节,适合视频直播、DNS、联机游戏
- 类比:TCP 是打电话(先接通、说得清),UDP 是寄平信(扔出去就不管)
- 两者都是**传输层**协议;基于 TCP 的还有 FTP/SMTP,基于 UDP 的还有 DHCP

### 14. HTTP 和 HTTPS 的区别?
**HTTPS = HTTP + **TLS/SSL 加密**:默认端口 **443**(HTTP 是 80)、需要 **CA 证书**、内容加密防窃听防篡改。**

- HTTP 明文传输,可被窃听、篡改;HTTPS 对称加密传输数据,用非对称加密交换密钥
- 证书:HTTPS 需要向 CA 申请证书,验证服务器身份,防止「中间人」冒充
- 端口:HTTP 默认 80,HTTPS 默认 443
- 代价:握手多几次往返、加解密消耗 CPU,但换来安全性,现代网站基本都是 HTTPS
- URL 前缀分别是 http:// 与 https://,浏览器对 HTTPS 站点显示锁标志

### 15. GET 和 POST 的区别?

- 参数位置:GET 参数在 URL 的 ? 后面;POST 参数在**请求体(body)**中
- 安全性:HTTP 下两者都是明文,但 GET 参数会留在浏览器历史、服务器日志里,**不适合传密码**
- 幂等性:GET 幂等(重复请求结果一样),POST 不幂等(可能重复创建资源)
- 本质都是 HTTP 方法,区别更多是**约定俗成**的规范用法而非技术强制

### 16. cookie、session、token 的区别?

**cookie 存**客户端**;session 存**服务器端**(浏览器只留 sessionid);token 是**服务端签名的自包含凭证**(如 JWT),服务端不用存状态,天然适合分布式。**

- cookie:存在浏览器,每次请求**自动携带**;用户可以查看和修改,别放敏感数据
- session:用户状态存服务器(内存/redis),浏览器 cookie 里只存一个 sessionid,更安全但占服务器资源
- token(如 JWT):服务端用密钥**签名**后发给客户端,客户端保存,每次请求带上;服务端不存会话状态,分布式/跨域友好
- 分布式部署时 session 要做共享(通常存 redis),token 不需要,这是 token 流行的原因
- 三者常配合:cookie 是「运输工具」,session/token 是「凭证内容」

### 17. MySQL 索引在哪些情况下会失效?
**高频失效场景:**对索引列用函数或运算、like 以 % 开头、隐式类型转换、or 连接非索引列、违反联合索引最左前缀**。**

- 对索引列使用函数或运算:`where year(create_time) = 2024` 不走索引,应改写成范围查询
- like 前置 %:`name like '%明'` 失效;前缀匹配 `name like '明%'` 可以走索引
- 隐式类型转换:phone 是 varchar 却写 `where phone = 13800000000` → 失效
- 联合索引(a, b, c)遵守**最左前缀**:只查 b/c 不走;查 a、c 只能用上 a
- or 两侧只要有非索引列就失效;列区分度太低(如性别)优化器也可能放弃索引
- 排查手段:`explain` 观察 type、key、rows 等字段

### 18. MySQL 有哪些事务隔离级别?分别解决什么问题?
**四个级别从低到高:**读未提交 → 读已提交 → 可重复读(MySQL 默认)→ 串行化**,逐级解决脏读、不可重复读、幻读。**

- 三个并发问题:**脏读**=读到别人未提交的数据;**不可重复读**=两次读同一行值不同(别人 update);**幻读**=两次查询行数不同(别人 insert)
- 读未提交(RU):三个问题都不防
- 读已提交(RC):解决脏读
- 可重复读(RR):再解决不可重复读;InnoDB 的 RR 通过 **MVCC + 间隙锁**基本避免幻读,是 **MySQL 默认级别**
- 串行化:事务完全串行执行,最安全也最慢

### 19. 乐观锁和悲观锁的区别?
**悲观锁**假设冲突常发生,先加锁再操作**(如 `select ... for update`);乐观锁**假设冲突少,提交时校验**(版本号),失败就重试。**

- 悲观锁:`select * from t where id = 1 for update` 直接锁住行,其他事务阻塞等待;适合**写多、冲突激烈**的场景
- 乐观锁:不加真锁,更新时带上条件 `update t set stock = stock - 1, version = version + 1 where id = 1 and version = 旧版本`
- 乐观锁影响行数为 0 说明数据被别人改过,业务层重试即可;常用 version 字段或时间戳实现
- 选型:悲观锁依赖数据库锁、并发低但强一致;乐观锁靠应用层逻辑,**读多写少**时吞吐更高

### 20. 简述 Django 的请求生命周期

****wsgi 接收请求 → 中间件(process_request)→ url 路由 → 视图(ORM/模板)→ 中间件(process_response)→ 返回响应**。**

- 浏览器发请求,web 服务器(uwsgi/gunicorn)按 **WSGI 协议**交给 Django
- 请求先**从上到下**穿过每个中间件的 process_request
- 再到 `urls.py` 匹配路径,把请求分发给对应的**视图函数/类视图**
- 视图通过 **ORM** 操作数据库、用模板渲染页面,产出 HttpResponse
- 响应**从下到上**再穿回中间件的 process_response,最后经 wsgi 返回浏览器
- 视图抛异常会走到中间件的 process_exception 统一处理

### 21. Django 中间件是干什么的?

**中间件是 Django 的**全局钩子层**,在请求进视图前、视图执行时、异常发生、响应返回时统一加工;常用于**登录校验、权限、日志、CORS**。**

- process_request:请求到达视图**之前**(常做登录、权限拦截)
- process_view:路由匹配到视图之后、视图执行之前
- process_exception:视图抛异常时统一兜底
- process_response:响应返回浏览器**之前**(如添加响应头)
- 执行顺序:request 阶段按 settings 里 MIDDLEWARE 列表**从上到下**,response 阶段**从下到上**
- Django 自带中间件:SecurityMiddleware、SessionMiddleware、CsrfViewMiddleware 等

### 22. 什么是缓存穿透、击穿、雪崩?怎么应对?
****穿透**=查不存在的数据,缓存永远不命中;**击穿**=单个热点 key 过期,瞬间打崩数据库;**雪崩**=大批 key 同时失效或 redis 挂掉。**

- 穿透应对:缓存空值(短过期时间)、**布隆过滤器**、入口参数校验(如 id<0 直接拒绝)
- 击穿应对:热点数据**不过期或逻辑过期**、互斥锁(只放一个请求去查库重建缓存)
- 雪崩应对:过期时间**加随机值**打散、redis 高可用(哨兵/集群)、服务限流降级、多级缓存
- 记忆口诀:穿透是「查没有的」,击穿是「一个热点没了」,雪崩是「一大片都没了」

### 23. 可变类型与不可变类型怎么区分?

****不可变**:数字、字符串、元组——「修改」实为创建新对象,id 会变;**可变**:列表、字典、集合——原地修改,id 不变,所有引用同步可见。**

- 不可变类型:int、float、bool、str、tuple——重新赋值(如 a = a + 1、s = s + 'x')是让变量指向**新对象**,id() 变化,原对象不受影响
- 可变类型:list、dict、set——append、pop、update 等**原地修改**,对象 id 不变,所有指向它的变量(包括函数里的形参)都能看到变化
- 自查方法:修改前后各打印一次 id(a),id 变了就是不可变类型,没变就是可变类型
- 注意:tuple 本身不可变,但里面的可变元素仍可改——t = (1, [2]) 后 t[1].append(3) 合法
- 关联考点:只有不可变对象才能做 dict 的 key;函数传参、深浅拷贝的副作用差异都源于可变与不可变

```python
a = "hello"
print(id(a))
a = a + " world"      # 不可变:创建新对象
print(id(a))          # id 变了

lst = [1, 2]
print(id(lst))
lst.append(3)         # 可变:原地修改
print(id(lst))        # id 没变
```

### 24. 字符编码:ASCII、GBK、Unicode、UTF-8 与 encode/decode

**计算机只认字节:ASCII(英文)→ 各国自定码表(GBK 中文 2 字节,互不兼容出乱码)→ Unicode 统一「码位」→ **UTF-8 是 Unicode 最常用的变长存储实现**(英文 1 字节、中文 3 字节);encode 字符串转字节,decode 字节转字符串。**

- 发展脉络:ASCII 只有英文 → 各国自己造码表(GBK、Shift_JIS)互不兼容 → Unicode 给全球字符统一编号 → UTF-8/GBK 是把码位存成字节的**编码方案**,UTF-8 为 Unicode 服务
- Python3 的 str 在内存中按 Unicode 存;存文件、走网络必须转成 **bytes**,所以要 encode/decode
- `s.encode('utf-8')` 得到 bytes,`b.decode('utf-8')` 还原 str;**用什么编码 encode 就必须用同一编码 decode**
- 乱码根源:编码与解码用了不同字符集(如 utf-8 文件用 gbk 解码);Python3 源文件默认 utf-8
- 细节:len(str) 按字符数,len(bytes) 按字节数;'人生' 编成 utf-8 占 6 字节、编成 gbk 占 4 字节

```python
s = "人生"
b = s.encode("utf-8")
print(b)                     # b'\xe4\xba\xba\xe7\x94\x9f'
print(len(s), len(b))        # 2 6:utf-8 中文 3 字节
print(len(s.encode("gbk")))  # 4:gbk 中文 2 字节
print(b.decode("utf-8"))     # 人生
```

### 25. 常用魔法方法(双下方法)有哪些?

**魔法方法是**双下划线包围**的特殊方法,由解释器在特定语法处**自动触发**,不需要手动调用:__init__ 初始化、__str__ 打印、__len__/__getitem__ 让对象支持 len()、下标取值与 for 遍历。**

- __init__:创建实例时自动调用完成初始化;__str__:print(对象)、str() 时调用,必须 return 字符串;__del__:对象被回收时触发
- 实现 __len__ 后 len(对象) 可用;实现 __getitem__(self, index) 后对象支持 obj[i] 下标取值,**还能被 for 遍历和切片**
- __eq__ 定义 == 的行为;__call__ 让对象能像函数一样 obj() 调用;__iter__/__next__ 让自定义类成为迭代器;with 语句依赖 __enter__/__exit__
- 面试常见问法:for 的本质、len() 为什么能作用于自定义对象——答案都落在对应魔法方法上
- 魔法方法按需实现、写了才生效;不要自己发明双下方法名

```python
class Playlist:
    def __init__(self, songs):
        self.songs = list(songs)
    def __len__(self):              # 触发:len(p)
        return len(self.songs)
    def __getitem__(self, i):       # 触发:p[i]、for、切片
        return self.songs[i]
    def __str__(self):              # 触发:print(p)
        return "Playlist(" + ", ".join(self.songs) + ")"

p = Playlist(["晴天", "稻香"])
print(len(p))     # 2
print(p[0])       # 晴天
print(p[1:])      # ['稻香']
print(p)          # Playlist(晴天, 稻香)
```

## 📖 课后作业（运维与面试）


### 1. 就业强化与 Git 作业清单

**就业强化阶段以**面试手写题 + Git/Linux 高频操作**为作业主线:每天 2~3 道手写代码题保持手感,Git 分支/回退/解决冲突要练成肌肉记忆,日志排查命令要能脱口而出。**

- Git 作业:add/commit 三区流转、reset --hard 回退与 reflog 找回、分支合并解决冲突的完整流程,对应本站「Git 与 Linux」章
- Linux 作业:grep/wc 统计日志、find 定位文件、kill 杀进程,排查思路「先看日志量级 → 实时盯日志 → 定位行号跳转」
- 面试手写作业:列表交集/并集、字符串反转单词顺序、去重、排序,每道先自己写再对答案
- 手写题标准:能默写、能讲清时间复杂度、能说出边界情况(空列表、重复元素、多余空格)
- 错题反复:手写题错一道,同类型加练三道,直到 5 分钟内无误写出

```python
grep -c error app.log        # 统计 error 出现的行数
grep error app.log | wc -l   # 等价写法:先匹配再数行
tail -f access.log           # 实时滚动看日志
git reset --hard HEAD^       # 回退到上一个版本
git reflog                   # 找回"消失"的提交
```

*运维与 Git 高频命令速查*

## 📖 并发复习包(Day38~42 考前速记)


### 1. 五天知识地图:一天一条主线


- Day38 进程(P453~P460)必会三点:①多道技术 = **空间复用 + 时间复用**;②三状态图(就绪/运行/阻塞,**阻塞不能直接回运行**);③Process 两种开启方式 + Windows 必须 `if __name__ == "__main__":` 保护
- Day39 锁与队列(P463~P470)必会三点:①join——**先统一 start 再统一 join**;②互斥锁 Lock 把并发改串行保数据安全;③Queue 进程间通信 + 生产者消费者(None 结束信号,几个消费者放几个)
- Day40 线程与 GIL(P473~P482)必会三点:①Thread 写法与 Process 几乎一致但**共享内存**;②守护线程 daemon 随主线程代码结束被带走;③GIL 三句话 + 口诀「计算密集用进程、IO 密集用线程」
- Day41 同步工具与池协程(P485~P495)必会三点:①死锁四条件与 RLock 解法;②Semaphore 限流、Event 线程间通知;③池(submit/map)+ 协程单线程切换
- Day42 IO 模型(P499~P505)必会三点:①**两阶段分析**(等数据/拷数据);②阻塞/非阻塞/多路复用/异步一张表;③select 代表多路复用、asyncio 代表异步,高并发排序:阻塞<非阻塞<多路复用<异步

### 2. 进程 vs 线程对比总表(一张表背完)

**一张表背完进程 vs 线程:模块 multiprocessing vs threading、数据**隔离 vs 共享**、开销大 vs 小、计算密集 vs IO 密集——所有对比题都从这张表推。**

- 创建方式:进程 `Process(target=..., args=...)` 或继承重写 run;线程 `Thread(...)` 写法几乎一致;关键差别:**Windows 下进程必须** `if __name__ == "__main__":` **保护,线程不需要**
- join:两者都是「主 XX **阻塞**等子 XX 结束再往下走」;口诀**先统一 start、再统一 join**——start 一个就 join 一个,并发退化成串行
- 数据:进程**隔离**(子进程改全局变量父进程看不见,通信靠 Queue/Pipe);线程**共享**(同一份内存,改全局变量都看得见,所以要加锁)——「进程安全但通信麻烦,线程高效但要小心竞争」
- 开销:进程 > 线程 > 协程;进程要复制资源、切换要换内存空间;线程只需注册一个执行流;协程在用户态切换几乎免费
- 适用场景口诀:**计算密集用进程(多核并行绕开 GIL),IO 密集用线程/协程(等待时切换)**;稳定性:进程崩了互不影响,线程一个崩全进程陪葬
- 一句话定位:**进程是资源分配的最小单位,线程是 CPU 调度的最小单位**(进程=车间,线程=车间里的工人)

### 3. 三把锁一句话:Lock/RLock/Semaphore

**三把锁一句话:**Lock 一次一个、RLock 可重入、Semaphore N 个坑**;再加死锁四条件(互斥/请求与保持/不可剥夺/循环等待)与预防口诀——锁家族考点一页收全。**

- **Lock 互斥锁**:一次只放一个——谁抢到谁进,其余在 acquire 处阻塞;场景:抢票、计数器等并发修改同一份数据;推荐 `with lock:` 写法,防忘 release 卡死所有人
- **RLock 递归锁**:同一个线程可以重复 acquire(内部计数 +1),配对 release 计数归零才真解锁;场景:「锁中锁」/递归调用里再次抢锁——Lock 会自己锁死自己,换 RLock 即破
- **Semaphore 信号量**:N 个坑——同时最多 N 个进入,第 N+1 个等;acquire 占坑、release 腾坑;场景:限流(最多 3 个爬虫同时抓)、连接池;Lock 相当于 Semaphore(1)
- **死锁四必要条件**:互斥、请求与保持、不可剥夺、循环等待——四个**同时成立**才会死锁,破坏任意一个即可预防
- 最常用预防:**所有线程按固定顺序抢锁**(破坏循环等待);「同线程重复抢锁」型死锁直接换 RLock(允许重入);一次性申请全部资源(破坏请求与保持)
- 背法:**Lock 排队一个进,RLock 同人可重进,Semaphore N 坑随便进;死锁四条件,破一即新生**

### 4. 线程间通信三件套:Queue/Event/线程q

**口诀:**传数据用队列,发通知用事件**——queue.Queue 线程安全先进先出、Event 一 set 全唤醒、multiprocessing.Queue 跨进程专用;三件套什么时候用哪个,一页分清。**

- **queue.Queue 线程队列**(线程q):`put()/get()` 线程安全,空了 get 阻塞等数据;线程间传数据首选,和 multiprocessing.Queue 用法一致
- **Event 事件**:一个线程 `set()`,所有 `wait()` 的线程被唤醒;`is_set()` 查状态、`clear()` 复位;场景:红绿灯/启动开关——等配置加载完、等信号再干活
- **multiprocessing.Queue 进程队列**:进程内存隔离,普通变量传不进子进程;把队列对象通过 args 传给子进程,put/get 背后 = **管道 + 锁 + pickle**;线程的 queue.Queue 传不进子进程,跨进程必须用它
- 生产者消费者模型:队列做**缓冲**(解耦/并发/忙闲互补);生产者做完放 **None 结束信号**——几个消费者放几个 None,少一个就有消费者永远阻塞在 get 上
- 选型一行:线程间传数据 → queue.Queue;线程间发信号 → Event;跨进程传数据 → multiprocessing.Queue;保护共享数据(不是传数据)→ Lock

### 5. 池与协程选型:谁来干活最划算

**池 = 固定数量的工人重复利用,省去反复创建销毁;**线程池治 IO 密集、进程池治计算密集**;协程单线程用户态切换,开销最小、并发量最大——选型一行:进程池吃 CPU,线程池等 IO,超大量连接上协程。**

- 为什么用池:任务多时反复创建/销毁进程线程**开销大**;池预先开好 N 个工人,任务排队领、用完归还;`with Pool(...) as pool:` 结束自动关闭,不用手动 shutdown
- **submit vs map**:submit 提交单个任务,立刻返回 Future,`future.result()` 阻塞拿结果;map **批量**提交,**结果按输入顺序返回**(与谁先跑完无关),最适合「一批输入一批输出」
- **ThreadPoolExecutor 线程池**:适合 IO 密集(网络请求、读写文件);**ProcessPoolExecutor 进程池**:适合计算密集(数值计算、图像处理),多核并行绕开 GIL;Windows 下进程池同样必须 `if __name__ == "__main__":` 保护
- **协程为什么省**:单线程内由程序/协程库在**用户态**切换——没有内核态上下文切换、没有线程栈开销,一个线程能挂成千上万协程;代价是吃不了多核
- 协程两代表:gevent(spawn/joinall + monkey 补丁)、asyncio(async/await 原生);都适合 IO 密集海量并发(如 TCP 并发服务端)
- 选型一行背:**进程池吃 CPU,线程池等 IO,超大量连接上协程**;开销排序:进程 > 线程 > 协程

### 6. IO 四模型一张表:两阶段谁阻塞

**用「两阶段」背 IO 四模型:①等数据到内核缓冲区 ②数据从内核拷到用户空间——**阻塞全堵、非阻塞轮询、多路复用 select 替你等、异步全不堵**;高并发排序:阻塞<非阻塞<多路复用<异步。**

- 两阶段分析框架:一次读 = **阶段① 等数据到内核缓冲区** + **阶段② 把数据从内核拷贝到用户空间**;四个模型的差别只在「这两个阶段各自阻不阻塞」
- **阻塞 IO**:①阻塞、②也阻塞——recv()/accept() 默认形态;最简单,但一个连接要配一个线程,并发一高线程爆炸
- **非阻塞 IO**:`setblocking(False)`,阶段①**轮询**不阻塞(没数据立刻返回/抛 BlockingIOError,自己反复问);阶段②拷贝仍阻塞;缺点是 CPU 空转浪费
- **IO 多路复用**:把一批连接交给 **select/poll/epoll** 帮你盯阶段①,谁有数据通知你,阶段②拷贝仍自己完成;一个线程管成百上千连接,代表 `select.select`
- **异步 IO(asyncio)**:发起后立刻返回,①②**都不用你管**,内核连拷贝都做完再通知你(回调/await 直接拿结果);代表 asyncio、Windows IOCP
- 高并发能力排序:**阻塞 < 非阻塞 < 多路复用 < 异步**;口诀:**select 替你等,asyncio 连等都不用**

### 7. 考前自测清单:10 个能不能

**考前 10 连问,每条先**口述 30 秒**再对答案;卡壳的那条回到 rv-2~rv-6 对应速记点重背——10 条全能脱口而出,并发五天就算毕业。**

- ①守护线程行为?——daemon=True 且必须在 start 前设,**主线程代码结束立刻被带走**,别放重要收尾
- ②GIL 三句话?——CPython 解释器级全局锁;同一时刻一个进程内只有一个线程执行字节码;IO 等待会释放,只卡 CPU 密集
- ③死锁四条件?——互斥、请求与保持、不可剥夺、循环等待(同时成立才死锁,破一即解)
- ④Windows 多进程坑?——spawn 靠**导入父模块**创建子进程,创建代码必须 `if __name__ == "__main__":` 保护,否则无限递归报错
- ⑤join 作用与正确写法?——阻塞等子进程/线程结束;**先统一 start、再统一 join** 才不退化成串行
- ⑥进程和线程在数据上的最大区别?——进程**隔离**(靠 Queue 通信),线程**共享**(靠 Lock 保护)
- ⑦Lock/RLock/Semaphore 一句话?——一次一个 / 同线程可重入 / N 个坑
- ⑧线程池和进程池怎么选?——IO 密集线程池,计算密集进程池(绕开 GIL 吃多核)
- ⑨协程为什么省?——单线程**用户态**切换,无系统上下文切换与线程栈开销,但吃不了多核
- ⑩IO 四模型两阶段谁阻塞?——阻塞全堵、非阻塞轮询(拷贝仍堵)、多路复用 select 替你等(拷贝仍自己做)、异步两阶段都不管

---
