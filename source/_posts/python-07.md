---
title: 异常处理与代码模板
date: 2026-11-07 09:00:00
tags:
  - Python
  - 异常处理
categories:
  - Python学习笔记
---
> 本文是「Python全栈学习中心」系列笔记之一,配套可刷题的本地工具(获取方式见文末)。

---

## 📖 异常处理

> 🎬 对应课程:Python基础(异常处理+日志)

### 1. 为什么要处理异常
> 🎬 对应视频:P418

**异常就是程序运行时发生的错误,**不处理程序会当场崩溃**,处理了就能给出友好提示并继续运行。**

- 异常发生后若不捕获,程序立即终止,并打印异常类型、位置和描述(堆栈信息)
- Python 中一切异常都是**异常类的实例**,不同错误对应不同类型
- 崩溃是不可接受的,尤其是服务端程序:一个用户请求出错不能拖垮整个服务

### 2. try / except / else / finally 完整结构
> 🎬 对应视频:P419~P420

**try 包可能出错的代码,except 捕获并处理,**else 在没异常时执行**,finally **无论如何都执行**。**

- except 可以写多个,从上到下匹配,**子类异常要写在父类前面**
- except 后不写类型 = 捕获所有异常(方便但危险,不推荐用于生产)
- `except XxxError as e` 可以拿到异常对象,print(e) 看错误信息
- else:try 块**没有发生异常**时才执行,常用来放“成功后的收尾逻辑”
- finally:无论是否异常、甚至 try 里 return 了都会执行,放**资源释放**(关文件、断连接)
- try/else 中不能没有 except;else 必须在所有 except 之后、finally 之前

```python
try:
    num = int(input("请输入整数:"))
except ValueError as e:
    print("输入不合法:", e)
else:
    print("输入成功:", num)
finally:
    print("程序结束")
```

### 3. 常见异常类型
> 🎬 对应视频:P419~P420

**记住高频异常和触发场景,看到报错能立刻定位问题。**

- IndexError:索引越界(列表/字符串下标超出范围)
- KeyError:访问字典中**不存在的键**
- ValueError:类型转换/传值不合法(如 `int("abc")`)
- TypeError:类型用错(如 `1 + "a"`)
- NameError:使用了**未定义**的变量
- FileNotFoundError:文件路径不存在
- ZeroDivisionError:除数为 0;StopIteration:next() 越过迭代器末尾

### 4. 主动抛异常 raise 与自定义异常
> 🎬 对应视频:P420

**业务上“不该发生的情况”用 `raise` 主动抛出;自定义异常类**继承 Exception**,让错误信息更语义化。**

- `raise ValueError("b不能为0")`:主动抛异常,后面代码不再执行
- 自定义异常:`class MyError(Exception)`,配合 docstring 写清含义
- assert 断言:`assert 条件, "提示"`,条件为假抛 AssertionError,常用于调试自检,可用 -O 关闭
- 课程强调:不要滥用 try 包住一大段代码,**精确捕获**才好定位问题

```python
class SalaryError(Exception):
    """工资输入不合法"""

def set_salary(v):
    if v < 0:
        raise SalaryError("工资不能为负数")
    return v

try:
    set_salary(-100)
except SalaryError as e:
    print("捕获到:", e)
```

### 5. 多异常捕获与异常类继承体系
> 🎬 对应视频:P419~P420

**一条 except 可用**元组**捕多种异常;异常是类且有继承树——**日常异常都挂在 Exception 分支下**,所以 `except Exception` 能兜住它们。**

- 一条捕获多种:`except (ValueError, KeyError) as e:`,两种异常走同一个处理逻辑
- 多个 except **从上到下匹配、命中即停**;所以**子类要写在父类前面**,如 FileNotFoundError 要放在 OSError 之前,否则永远轮不到子类
- 继承体系:所有异常的祖先是 **BaseException**;日常处理的 IndexError、KeyError、ValueError 等都在 **Exception** 分支下
- KeyboardInterrupt(Ctrl+C)、SystemExit 继承自 BaseException 但**不是 Exception 的子类**——所以 `except Exception` 不会误捕用户的退出操作
- 拿不准类型时,先用 `except Exception as e:` 打印 `type(e).__name__` 和 e 观察真实类型,再改成精确捕获

### 6. 异常处理的本质与 Traceback 堆栈阅读
> 🎬 对应视频:P419~P420

**异常本质是**异常对象沿调用链向上传播**,直到被某个 except 接住;Traceback **从下往上看**:最后一行是异常类型和描述,往上依次是调用路径。**

- 出错时 Python 创建异常对象,当前函数没人处理就**一层层向上传播**给调用者,直到被捕获或冒泡到顶层——程序终止并打印堆栈
- 读堆栈:最后一行是异常类型 + 消息;往上每条 'File xxx, line n' 是'依次调用过的函数',**定位时先找自己写的文件**,不要被库文件带偏
- `import traceback` 后,在 except 里 `traceback.print_exc()` 可以像解释器一样打印完整堆栈;`traceback.format_exc()` 返回字符串,方便写进日志
- except 里写单独的 `raise`(不带任何内容)可以把**当前异常原样重新抛出**,常用于'这里记个日志,再让上层知道出错'
- 读懂堆栈就不用逐行 print 调试:看到 TypeError 先怀疑类型、KeyError 先查键名、AttributeError 先查对象有没有这个属性

```python
import traceback

def a():
    b()          # a 调用 b

def b():
    1 / 0        # 错误发生在 b 里

try:
    a()
except ZeroDivisionError:
    print(traceback.format_exc())
# 打印完整堆栈:最后一行 ZeroDivisionError: division by zero,
# 往上能看到 a -> b 的调用路径和各自行号
```

*traceback 拿到完整堆栈*

### 7. logging 日志与异常记录
> 🎬 对应视频:P420

**logging 按**级别(DEBUG<INFO<WARNING<ERROR<CRITICAL)**输出、可落文件带时间;except 里调 `logging.exception()` 会**自动附上完整异常堆栈**。**

- print 调试是一次性的,日志能分级过滤、写文件、带时间戳,是正式项目排查问题的标准手段
- `logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s %(message)s')` 一次性配置;**低于设定级别的日志不输出**
- 五个级别从低到高:DEBUG < INFO < WARNING < ERROR < CRITICAL;默认级别是 WARNING,所以 info() 默认看不见
- **在 except 块里调用 `logging.exception('描述')`,日志自动附带当前异常的完整堆栈**(等价于 error + exc_info=True),不用手动拼 traceback
- 服务端套路:最外层 try 包住请求 → 捕获 Exception 后 logging.exception 记录 → 给用户返回友好提示;**服务不崩,事后还能翻日志定位**

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",                       # 写入文件
    format="%(asctime)s %(levelname)s %(message)s",
)

try:
    n = int("abc")          # 模拟出错
except ValueError:
    logging.exception("用户输入转换失败")       # 自动带完整堆栈
print("服务继续运行")
# app.log 中:ERROR 级别 + 完整 Traceback + 描述信息
```

*logging.exception 记录异常堆栈*

### 8. 异常链:raise ... from
> 🎬 对应视频:P420

**在 except 里抛新异常,Python 会自动把原异常挂到 `__context__` 形成**异常链**;`raise 新异常 from 原异常` 语义最明确,`from None` 则隐藏根因。**

- except 块里再 raise,堆栈会显示两段:'During handling of the above exception, another exception occurred'——新异常的 `__context__` 自动指向原异常
- `raise NewError('描述') from e`:**显式异常链**,新异常的 `__cause__` 指向 e,堆栈显示 'The above exception was the direct cause of…'
- `from None`:只抛新异常、**隐藏上游异常**,适合不想把内部细节暴露给调用方的场景;慎用,会丢排查线索
- 典型用法:把底层异常(数据库、JSON 解析失败)包装成业务异常向上抛——**调用方只需捕获业务异常,根因仍在链上可查**
- 排查两段式堆栈时:先看最上面(最早的根因),再看最下面(最终暴露的业务错误)

```python
import json

def load_config(path):
    try:
        return json.loads('{"name": "app",')
    except json.JSONDecodeError as e:
        # 把底层解析错误包装成业务异常,根因挂在链上
        raise RuntimeError("配置文件格式错误") from e

try:
    load_config("config.json")
except RuntimeError as e:
    print("捕获业务异常:", e)   # 堆栈里仍能看到原始的 JSONDecodeError
```

*raise ... from 显式异常链*

### 9. 断言 assert 与精确捕获最佳实践
> 🎬 对应视频:P420

**`assert 条件, "提示"` 是写给**开发者自己看的自检**:条件为假抛 AssertionError;它和面向调用者的 raise 是两回事,还能被 -O 参数整体关闭。**

- 语法:`assert 表达式, "描述"`,等价于 `if not (表达式): raise AssertionError("描述")`;表达式为真时什么都不发生
- 用途:检查「程序运行到这里,某条件**必须成立**」——函数入口校验参数、调试时确认中间结果、防止「不可能的情况」悄悄发生
- assert vs raise:raise 抛的是**业务上预期会发生**、需要调用者处理的错误;assert 断的是**不该发生的逻辑错误**,出现了说明代码有 bug
- 致命区别:`python -O` 运行时**所有 assert 语句被跳过**——所以用户输入校验、金额检查等业务校验绝不能用 assert,必须 raise
- 课堂反复强调的最佳实践:try 只包精确的一小段;**精确捕获**异常类型,不写裸 except;捕获后要有动作(提示/日志/重抛),别把异常吞掉

## 📖 代码模板速查

> 🎬 对应课程：各阶段课堂模板总结（装饰器模板P244、套接字模板P433~P447、单例P413、日志P327~P330）

### 1. 通用装饰器模板（必背）
> 🎬 对应视频:P244

****六步写法**：外层收函数 → wraps保元信息 → inner收调用参数 → 前功能 → 执行原函数拿res → 后功能 → return res → 外层return inner。**

- *args, **kwargs 让装饰器**适配任意参数签名**的函数
- res 必须接住并 return，否则被装饰函数的返回值会丢失
- @wraps(func) 不影响功能，但让 __name__ 等元信息保持原样（调试/文档需要）
- @outer 是语法糖，等价于 index = outer(index)

```python
from functools import wraps

def outer(func):
    @wraps(func)                  # 保留被装饰函数的元信息
    def inner(*args, **kwargs):
        print("调用前")           # 前功能
        res = func(*args, **kwargs)  # 执行原函数
        print("调用后，结果:", res)  # 后功能
        return res                   # 把返回值还给调用方
    return inner

@outer                    # 语法糖: index = outer(index)
def index(a, b):
    return a + b

print(index(1, 2))
```

*通用装饰器模板：背熟这12行，应付一切装饰器需求*

### 2. 有参装饰器模板（三层）
> 🎬 对应视频:P248~P249

**在通用装饰器外面**再包一层收参数**：第一层收装饰器参数，第二层收函数，第三层收调用参数。**

- 三层从外到内：route(argv) 收参数 → outer(func) 收函数 → inner(*args, **kwargs) 收调用
- @route("GET") 是先执行 route("GET") 拿到真正的装饰器 outer，再装饰
- 最多三层，超过就是代码设计有问题

```python
from functools import wraps

def route(argv):                    # 第1层: 收装饰器的参数
    def outer(func):                # 第2层: 收被装饰的函数
        @wraps(func)
        def inner(*args, **kwargs): # 第3层: 收调用的参数
            if argv == "GET":
                return func(*args, **kwargs)
            return "405 Method Not Allowed"
        return inner
    return outer

@route("GET")
def index():
    return "页面内容"

@route("POST")
def save():
    return "保存成功"

print(index())   # 页面内容
print(save())    # 405 Method Not Allowed
```

*有参装饰器：Django 里按请求方法路由就用这个思路*

### 3. TCP 服务端模板（链接循环 + 通信循环）
> 🎬 对应视频:P433~P439

**五步：创建 → **bind** → **listen** → **accept** → recv/send；外面套**链接循环**服务多个客户端，里面套**通信循环**反复收发。**

- accept() 返回 (conn, addr)，之后收发都用 conn，不用 server
- recv 返回 bytes，decode 解码；send 参数必须是 bytes，encode 编码
- if not data: break 处理客户端正常关闭；except ConnectionResetError 处理异常断开
- 两个循环缺一不可：没有链接循环只能服务一个客户端，没有通信循环只能收一次

```python
import socket

server = socket.socket()
server.bind(("127.0.0.1", 8000))  # 绑定地址与端口
server.listen(5)                   # 半链接池

while True:                        # 链接循环: 服务多个客户端
    conn, addr = server.accept()   # 等待连接
    print("客户端连入:", addr)
    while True:                    # 通信循环: 反复收发
        try:
            data = conn.recv(1024)
            if not data: break     # 客户端正常关闭
            print("收到:", data.decode("utf-8"))
            conn.send(data.upper())
        except ConnectionResetError:
            break                  # 客户端异常断开
    conn.close()
server.close()
```

*TCP服务端：课程远程执行命令程序就是在这个模板上长的*

### 4. TCP 客户端模板
> 🎬 对应视频:P434~P436

**客户端只有三步：创建 → **connect** → 收发；比服务端少 bind/listen/accept。**

- connect 的参数是服务端的 (ip, port) 元组
- 发消息前 strip() 防止空消息；encode 编码后再 send

```python
import socket

client = socket.socket()
client.connect(("127.0.0.1", 8000))
while True:
    msg = input(">>> ").strip()
    if not msg: continue
    client.send(msg.encode("utf-8"))
    data = client.recv(1024)
    print(data.decode("utf-8"))
client.close()
```

### 5. UDP 模板（recvfrom / sendto）
> 🎬 对应视频:P441

**UDP 无连接：服务端用 **recvfrom** 收（返回数据和对方地址），回信用 **sendto(数据, addr)**；客户端不需要 connect。**

- 创建时 type=socket.SOCK_DGRAM（TCP 默认是 SOCK_STREAM）
- UDP 没有 conn 概念，也没有通信循环的说法——每次 recvfrom 都可能来自不同客户端
- UDP 不黏包（有消息边界），TCP 才黏包

```python
# 服务端
import socket
server = socket.socket(type=socket.SOCK_DGRAM)
server.bind(("127.0.0.1", 8001))
while True:
    data, addr = server.recvfrom(1024)
    print("收到:", data.decode("utf-8"))
    server.sendto(data.upper(), addr)   # 回给对方地址

# 客户端
import socket
client = socket.socket(type=socket.SOCK_DGRAM)
client.sendto(b"hello udp", ("127.0.0.1", 8001))
print(client.recvfrom(1024)[0].decode("utf-8"))
```

*UDP服务端与客户端：无需 accept/connect*

### 6. struct 自定义报头解决黏包模板
> 🎬 对应视频:P445~P446

**先发 **4字节报头**（struct.pack 打包内容长度），再发内容；接收方先收4字节 unpack 出长度，再**精确收**这个长度——黏包终结者。**

- struct.pack("i", n) 把整数压成固定4字节，unpack 解回来是元组，取 [0]
- 先收报头再按长度收内容，不管中间怎么缓冲都不会错位
- 报头里还可以放 json（文件名、大小等元信息），就是课程的“终极大招”

```python
import json, struct

def send_msg(conn, data):
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    head = struct.pack("i", len(body))   # 4字节报头: 内容长度
    conn.send(head + body)               # 报头+内容一起发出

def recv_msg(conn):
    head = conn.recv(4)                  # 先收固定4字节
    body_len = struct.unpack("i", head)[0]
    body = b""
    while len(body) < body_len:          # 内容可能分段到达
        body += conn.recv(body_len - len(body))
    return json.loads(body.decode("utf-8"))
```

*发送与接收成对使用，就是解决黏包的终极大招*

### 7. socketserver 并发模板
> 🎬 对应视频:P447

**继承 **BaseRequestHandler**，把通信逻辑写进 **handle** 方法；ThreadingTCPServer 自动为每个客户端开线程。**

- self.request 就是 conn（连接对象），用法和 recv/send 完全一样
- ThreadingTCPServer 换成 ProcessTCPServer 就是多进程并发
- handle 里也要写通信循环，否则一个客户端只能收一次

```python
import socketserver

class MyServer(socketserver.BaseRequestHandler):
    def handle(self):                    # 每个客户端连入自动执行
        while True:
            data = self.request.recv(1024)
            if not data: break
            self.request.send(data.upper())

if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 8002), MyServer)
    server.serve_forever()               # 一个客户端一个线程
```

### 8. 单例模式模板（__new__ + 双重检查锁）
> 🎬 对应视频:P413

**重写 **__new__** 控制实例创建：类属性 _instance 存唯一实例，**双重检查 + 加锁**保证多线程下也只有一个实例。**

- 第一次 if 避免每次都加锁（性能），with lock 里的第二次 if 保证并发安全
- super().__new__(cls) 才是真正创建对象的一步
- 线程锁用 threading.Lock

```python
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:            # 第1道检查
            with cls._lock:                  # 加锁
                if cls._instance is None:    # 第2道检查
                    cls._instance = super().__new__(cls)
        return cls._instance

a = Singleton()
b = Singleton()
print(a is b)    # True: 永远同一个实例
```

### 9. 生产者消费者模板（Queue + None 哨兵）
> 🎬 对应视频:P469

**生产者往 **Queue** 放数据，消费者 get 处理；生产完放一个 **None 哨兵**，消费者收到哨兵就退出——课程里“生产者消费者模型”的标准实现。**

- Queue 自带锁，多线程下 put/get 天然安全
- 哨兵数量要和消费者数量一致，否则有消费者永远等不到结束
- q.task_done() / q.join() 是另一种收尾方式

```python
from queue import Queue
from threading import Thread
import time

q = Queue()

def producer():
    for i in range(1, 6):
        time.sleep(0.2)
        q.put("任务%d" % i)
        print("生产了", i)
    q.put(None)                    # 哨兵: 通知消费者结束

def consumer():
    while True:
        item = q.get()
        if item is None: break     # 收到哨兵就收工
        print("消费了", item)

Thread(target=producer).start()
Thread(target=consumer).start()
```

### 10. 线程池 / 进程池模板
> 🎬 对应视频:P491~P492

**submit 提交任务拿 **future**，result() 取结果；map 批量提交且结果有序；**with 语句自动等全部完成**。**

- ThreadPoolExecutor(4) 表示最多4个线程；把类名换成 ProcessPoolExecutor 就是进程池
- f.result() 会阻塞到该任务完成；as_completed 按完成顺序取
- 进程池的任务函数必须能被 pickle（写在模块顶层）

```python
from concurrent.futures import ThreadPoolExecutor

def task(n):
    return n * n

with ThreadPoolExecutor(4) as pool:          # 4 个线程
    futures = [pool.submit(task, i) for i in range(1, 6)]
    for f in futures:
        print(f.result())                    # 1 4 9 16 25

# 批量写法(结果有序)
with ThreadPoolExecutor(4) as pool:
    print(list(pool.map(task, range(1, 6)))) # [1, 4, 9, 16, 25]
```

### 11. logging 日志字典模板
> 🎬 对应视频:P327~P330

**课程标准日志配置：**LOG_DICT 字典**定义格式/落盘/级别，dictConfig 一次性加载，getLogger("app") 拿 logger 使用。**

- format 里 %(asctime)s 时间、%(levelname)s 级别、%(name)s 记录者
- handlers 里 FileHandler 落盘；loggers 里把 logger 名字和 handler 绑定
- 轮转用 handlers 的 class 换成 logging.handlers.RotatingFileHandler

```python
import logging.config

LOG_DICT = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "std": {"format": "%(asctime)s [%(levelname)s] %(message)s"}
    },
    "handlers": {
        "file": {"class": "logging.FileHandler",
                 "filename": "app.log",
                 "formatter": "std",
                 "encoding": "utf-8"}
    },
    "loggers": {
        "app": {"handlers": ["file"], "level": "DEBUG"}
    }
}

logging.config.dictConfig(LOG_DICT)
log = logging.getLogger("app")
log.info("服务启动")
log.error("出错了!")
```

*运行后 app.log 里会出现带时间的两行日志*

### 12. 登录认证装饰器模板
> 🎬 对应视频:P340

**装饰器里完成输入校验（MD5 比对），通过才执行原函数——ATM/选课项目的**登录认证装饰器**就是这个模板。**

- 用户数据放文件/字典，密码只存 MD5 值不存明文
- input 写在装饰器 inner 里，被装饰的函数只管业务
- 校验通过 return func(*args, **kwargs)，不通过就给提示

```python
import json, hashlib
from functools import wraps

def read_users():
    with open("users.json", encoding="utf-8") as f:
        return json.load(f)

def auth(func):
    @wraps(func)
    def inner(*args, **kwargs):
        name = input("用户名:").strip()
        pwd = input("密码:").strip()
        md5 = hashlib.md5()
        md5.update(pwd.encode("utf-8"))
        if read_users().get(name) == md5.hexdigest():
            return func(*args, **kwargs)
        return "登录失败"
    return inner

@auth
def shopping():
    return "进入购物系统"

print(shopping())
```

*运行时输入 users.json 里登记的用户名与明文密码即可通过*

---

**系列目录 / 工具获取方式见文末 👇**