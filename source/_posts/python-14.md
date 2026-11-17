---
title: 代码精选 51 段
date: 2026-11-14 09:00:00
tags:
  - Python
  - 代码
categories:
  - 练习与代码
---

> 我的学习笔记,边学边记,持续修订。

> 本文整理视频里老师敲的重点课堂代码,每段标注对应集数与练习要点。
> 建议:先遮住代码自己写,写完对照;改参数看变化。

---

## ⌨️ 变量引用与 id / is / ==(第一周必敲)


🎯 **这段练什么:** 变量存的是**引用**不是值本身;b = a 后两个名字共用对象;`is` 比地址、`==` 比值。敲完这段,后面所有"改了a怎么b也变了"的问题都能自己推导。

```python
a = [1, 2, 3]
b = a              # b 和 a 指向同一个列表
b.append(4)
print(a)           # [1, 2, 3, 4]  改b即改a
print(a is b)      # True 同一个对象

c = [1, 2, 3, 4]
print(a == c)      # True 值相等
print(a is c)      # False 但不是同一个对象
print(id(a), id(c))  # 两个不同的内存地址
```

---

## ⌨️ 可变 / 不可变 类型行为实验


🎯 **这段练什么:** 不可变类型"改值"=换新对象(id 变);可变类型原地改(id 不变)。这是默认参数坑、字典键限制的根源,务必亲手敲一遍看 id。

```python
x = 1000
print(id(x))       # 例如 233...840
x += 1
print(id(x))       # 地址变了:不可变,换新对象

lst = [1, 2]
print(id(lst))     # 例如 233...992
lst.append(3)
print(id(lst))     # 地址没变:可变,原地修改

# 推论:可变对象不能做字典的键
# d = {[1, 2]: 'v'}   # TypeError: unhashable
```

---

## ⌨️ 赋值 / 浅拷贝 / 深拷贝 三连对比


🎯 **这段练什么:** 老师 Day07 的画图实验代码:改**内层**列表,看三种"复制"谁跟着变。面试口诀就从这组实验来。

```python
import copy
a = [1, [2, 3]]

b = a                  # 赋值:同一个对象
c = copy.copy(a)       # 浅拷贝:第一层新,内层共享
d = copy.deepcopy(a)   # 深拷贝:全部独立

a[0] = 999
a[1].append(4)
print(b)   # [999, [2, 3, 4]]  全跟着变
print(c)   # [1, [2, 3, 4]]     外层没变,内层跟着变
print(d)   # [1, [2, 3]]        完全不变
```

---

## ⌨️ 用列表模拟队列与堆栈


🎯 **这段练什么:** 队列**先进先出**(pop(0)),堆栈**先进后出**(pop())。这页代码同时练列表两端操作,数据结构第一课。

```python
# 队列:先进先出(排队买饭)
queue = []
queue.append("A")
queue.append("B")
queue.append("C")
print(queue.pop(0))   # A  先来的先走
print(queue)          # ['B', 'C']

# 堆栈:先进后出(叠盘子)
stack = []
stack.append(1)
stack.append(2)
stack.append(3)
print(stack.pop())    # 3  最后放的最先出
print(stack)          # [1, 2]
```

---

## ⌨️ 字典完整增删改查与安全取值


🎯 **这段练什么:** Day09 字典五连:增改一条龙、`del/pop` 删、`get` 安全取、`setdefault` 不覆盖、items 遍历。写用户管理功能就是这套。

```python
users = {"alex": 18, "yuan": 20}

users["eva"] = 22          # 增/改:有则改无则增
print(users.get("tom"))        # None,不报错
print(users.get("tom", 0))     # 0,给默认值
users.setdefault("alex", 99)   # 键已存在则不动
print(users["alex"])            # 18

users.pop("yuan")          # 删(指定键)
for name, age in users.items():
    print(name, age)        # 遍历键值对
```

---

## ⌨️ 集合去重与关系运算


🎯 **这段练什么:** set 天然去重 + 四种关系运算符。爬虫去重、共同好友、差集推荐全靠它。注意空集合必须写 `set()`。

```python
lst = [1, 2, 2, 3, 3, 3]
print(set(lst))         # {1, 2, 3} 去重(无序)
print(list(set(lst)))   # 转回列表

pythoner = {"alex", "yuan", "eva"}
linuxer = {"yuan", "tom"}
print(pythoner & linuxer)   # 交集 {'yuan'} 都会
print(pythoner | linuxer)   # 并集 全部人
print(pythoner - linuxer)   # 差集 只会python
print(pythoner ^ linuxer)   # 对称差 只会一样
```

---

## ⌨️ if 分支 + 三元表达式(成绩等级)


🎯 **这段练什么:** if/elif 从上到下**命中即止**;三元是"一行if",写前端模板和推导式的基础。注意 elif 别写成 else if。

```python
score = 85
if score >= 90:
    level = "A"
elif score >= 80:
    level = "B"
elif score >= 60:
    level = "C"
else:
    level = "D"
print(level)   # B

# 三元表达式:值1 if 条件 else 值2
res = "及格" if score >= 60 else "不及格"
print(res)     # 及格
```

---

## ⌨️ while + break / continue / else(猜年龄)


🎯 **这段练什么:** 课程第一经典练习:while 控次数、break 跳出、**while-else** 只在"没被 break"时执行——else 正好表达"三次都没猜中"。

```python
age, count = 56, 0
while count < 3:
    guess = int(input("猜年龄:"))
    if guess == age:
        print("猜对了!")
        break
    print("猜大了" if guess > age else "猜小了")
    count += 1
else:
    print("三次机会用完")   # 没被break才会走到这
```

---

## ⌨️ for 嵌套:九九乘法表


🎯 **这段练什么:** 外层控制行、内层控制列;`print` 的 **end 参数**控制不换行。嵌套循环规律:外层走一步,内层走一圈。

```python
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}x{i}={i*j}", end="\t")
    print()   # 一行结束换行
# 1x1=1
# 1x2=2  2x2=4  ...
```

---

## ⌨️ 列表生成式组合拳(过滤+变换+三元)


🎯 **这段练什么:** Day19 一集讲完生成式家族:`[表达式 for x in ... if 条件]`。先把 for 循环写对,再翻译成生成式,不要硬想。

```python
nums = [1, 2, 3, 4, 5, 6]

# 只留偶数再平方
r1 = [x * x for x in nums if x % 2 == 0]
print(r1)   # [4, 16, 36]

# 带三元的变换:奇偶分类
r2 = ["偶" if x % 2 == 0 else "奇" for x in nums]
print(r2)   # ['奇', '偶', '奇', '偶', '奇', '偶']

# 字典/集合生成式:把 [] 换成 {} 即可
r3 = {x: x * x for x in range(4)}
print(r3)   # {0: 0, 1: 1, 2: 4, 3: 9}
```

---

## ⌨️ 文件读三种方式 + with 上下文


🎯 **这段练什么:** read 全量 / readline 一行 / readlines 行列表,大文件用 **for 逐行**;with 自动 close。注意 w 会清空、a 是追加。

```python
with open("demo.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")

with open("demo.txt", encoding="utf-8") as f:
    print(f.read())            # 全部读成一个字符串

with open("demo.txt", encoding="utf-8") as f:
    print(f.readlines())       # ['第一行\n', '第二行\n']

with open("demo.txt", encoding="utf-8") as f:
    for line in f:             # 推荐:逐行,内存友好
        print(line.rstrip("\n"))
```

---

## ⌨️ 文件修改的两种方式(临时文件替换)


🎯 **这段练什么:** 文件没有"局部修改",只有**覆盖式(r+)和替换式(临时文件)**。替换式是工程做法:写临时文件→os.replace 原子替换。

```python
import os

# 方式一:r+ 从头覆盖(危险:长短不齐会残留)
# 方式二:全部读出改完写临时文件,再替换(推荐)
with open("demo.txt", encoding="utf-8") as f1, \
     open(".tmp", "w", encoding="utf-8") as f2:
    for line in f1:
        f2.write(line.replace("旧词", "新词"))
os.replace(".tmp", "demo.txt")   # 原子替换
print(open("demo.txt", encoding="utf-8").read())
```

---

## ⌨️ 函数参数全家桶(位置/关键字/默认/*args/**kwargs)


🎯 **这段练什么:** Day14 参数一集通:定义侧与调用侧各自怎么写;*args 收多余**位置**参数成元组,**kwargs 收多余**关键字**参数成字典。

```python
def register(name, age=18, *args, **kwargs):
    print("位置:", name)
    print("默认:", age)
    print("*args:", args)
    print("**kwargs:", kwargs)

register("alex", 20, "male", "shanghai", city="上海", tel="123")
# 位置: alex
# 默认: 20
# *args: ('male', 'shanghai')
# **kwargs: {'city': '上海', 'tel': '123'}

# 经典坑:默认参数别用可变对象
# def bad(x, lst=[]): ...   # 所有调用共享同一个列表!
```

---

## ⌨️ 装饰器从闭包到模板的五步演进(必敲)


🎯 **这段练什么:** Day17 老师一步步推:无参装饰器→闭包引用外层变量→把函数当参数传→return inner→语法糖。**敲完这五步,装饰器就是填空题**。

```python
from functools import wraps

# 第1步:函数也是对象,可以当参数传
def talk():
    return "hello"

def deco(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print("调用前")
        res = func(*args, **kwargs)   # 执行原函数
        print("调用后")
        return res                    # 返回值别弄丢
    return inner

# 第2步:语法糖等价于 index = deco(index)
@deco
def index():
    return "我是index"

print(index())
# 调用前 / 我是index / 调用后
```

---

## ⌨️ 有参装饰器(三层结构)


🎯 **这段练什么:** 在通用装饰器外**再包一层收参数**。记住执行顺序:先 `@route("GET")` 求值得真装饰器,再装饰函数。最多三层。

```python
from functools import wraps

def route(method):              # 第1层:收装饰器参数
    def outer(func):            # 第2层:收函数
        @wraps(func)
        def inner(*args, **kwargs):   # 第3层:收调用参数
            if method == "GET":
                return func(*args, **kwargs)
            return "405 不允许"
        return inner
    return outer

@route("GET")
def page():
    return "页面"

@route("POST")
def save():
    return "保存"

print(page())   # 页面
print(save())   # 405 不允许
```

---

## ⌨️ 迭代器协议与 for 循环本质


🎯 **这段练什么:** 手写 `__iter__/__next__` 造一个迭代器,再用 while+next 复刻 for 的执行过程——for 面试题的标准答案代码。

```python
class MyRange:
    def __init__(self, n):
        self.i, self.n = 0, n
    def __iter__(self):
        return self
    def __next__(self):
        if self.i >= self.n:
            raise StopIteration   # 迭代完毕的信号
        self.i += 1
        return self.i - 1

# for 的本质 = iter() + 反复 next() + 捕获StopIteration
it = iter(MyRange(3))
while True:
    try:
        print(next(it))       # 0 1 2
    except StopIteration:
        break
```

---

## ⌨️ 生成器:yield 与 send 表达式


🎯 **这段练什么:** 函数体里有 yield 就是生成器函数;`x = yield 值` 的 send 能**从外面往里传值**。这是协程思想的雏形。

```python
def eater():
    print("开饭!")
    total = 0
    while True:
        food = yield total    # 暂停点:交出total,等send送来food
        total += 1
        print("吃到:", food)

g = eater()
print(next(g))        # 启动到第一个yield -> 0(必须先next)
print(g.send("包子"))  # 吃到包子 -> 1
print(g.send("面条"))  # 吃到面条 -> 2
```

---

## ⌨️ 递归与二分法查找


🎯 **这段练什么:** 递归两阶段:**递推(压栈)→ 回溯(弹栈)**,必须有终止条件;二分法每次砍一半,前提是**有序**。

```python
def binary_search(lst, item):
    print("查找:", lst)          # 观察每次砍半
    if not lst:
        return False
    mid = len(lst) // 2
    if lst[mid] == item:
        return True
    elif lst[mid] > item:
        return binary_search(lst[:mid], item)
    else:
        return binary_search(lst[mid+1:], item)

nums = list(range(0, 100, 2))    # 有序偶数
print(binary_search(nums, 66))   # True
print(binary_search(nums, 67))   # False
```

---

## ⌨️ OOP 全家桶:类 / 继承 / super / 绑定方法


🎯 **这段练什么:** Day27~29 一条线敲完:类属性与实例属性、`__init__` 初始化、继承重写、super 复用父类、**绑定方法默认传 self**。

```python
class Animal:
    kind = "动物"            # 类属性:所有实例共享
    def __init__(self, name):
        self.name = name     # 实例属性:各管各的
    def shout(self):         # 绑定方法:调用时自动传self
        return f"{self.name}在叫"

class Dog(Animal):
    def __init__(self, name, color):
        super().__init__(name)    # 复用父类初始化
        self.color = color
    def shout(self):              # 重写=多态
        return super().shout() + ",汪汪!"

d = Dog("旺财", "黄")
print(d.name, d.kind, d.shout())
# 旺财 动物 旺财在叫,汪汪!
```

---

## ⌨️ property / classmethod / staticmethod 三件套


🎯 **这段练什么:** property 把方法伪装成属性(取值/赋值/删除三连);classmethod 第一个参数是**类**、staticmethod 谁都不自动传。

```python
class Student:
    school = "Python学院"
    def __init__(self, name):
        self._name = name

    @property
    def name(self):                # 像属性一样取:s.name
        return self._name
    @name.setter
    def name(self, v):             # 像属性一样赋:s.name = x
        if not v:
            raise ValueError("名字不能空")
        self._name = v

    @classmethod
    def from_school(cls):          # 类方法:替代构造
        return cls("新同学")

    @staticmethod
    def is_adult(age):             # 静态方法:工具函数
        return age >= 18

s = Student.from_school()
print(s.name, Student.is_adult(20))   # 新同学 True
```

---

## ⌨️ 反射:getattr 按字符串调度功能(选课系统核心)


🎯 **这段练什么:** 用户输入编号→**getattr(obj, "函数名")** 直接拿到方法调用。加新功能只要注册菜单,不改调度逻辑——选课系统/Django CBV 同款思想。

```python
class Menu:
    def login(self):
        return "登录页"
    def register(self):
        return "注册页"
    def quit(self):
        return "退出"

mapping = {"1": "login", "2": "register", "q": "quit"}
obj = Menu()
choice = input("输入功能编号:")     # 例如输入 1
func = getattr(obj, mapping.get(choice, "quit"), None)
print(func() if func else "没有这个功能")
```

---

## ⌨️ TCP 服务端 / 客户端(双循环标准版)


🎯 **这段练什么:** 背下来的结构:**链接循环套通信循环**;accept 返回 conn 才是收发用的;客户端断开处理两条路径(空数据/ConnectionResetError)。

```python
# ===== server.py =====
import socket
server = socket.socket()
server.bind(("127.0.0.1", 8000))
server.listen(5)
while True:                       # 链接循环
    conn, addr = server.accept()
    while True:                   # 通信循环
        try:
            data = conn.recv(1024)
            if not data: break    # 客户端正常关闭
            conn.send(data.upper())
        except ConnectionResetError:
            break                 # 客户端异常断开
    conn.close()

# ===== client.py =====
# import socket
# c = socket.socket()
# c.connect(("127.0.0.1", 8000))
# while True:
#     msg = input(">>> ").strip()
#     if not msg: continue
#     c.send(msg.encode("utf-8"))
#     print(c.recv(1024).decode("utf-8"))
```

---

## ⌨️ struct 报头解决黏包(发送/接收成对)


🎯 **这段练什么:** 黏包终结者:先发**4字节定长报头**说明正文长度,接收方"收固定长→解出真长→循环凑满"。大文件传输就用它。

```python
import struct, json

def send_msg(sock, obj):
    body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    head = struct.pack("i", len(body))     # 定长4字节报头
    sock.send(head + body)

def recv_msg(sock):
    head = sock.recv(4)                    # 1.先收固定4字节
    size = struct.unpack("i", head)[0]     # 2.解出正文长度
    chunks, got = b"", 0
    while got < size:                       # 3.循环凑满
        chunk = sock.recv(size - got)
        if not chunk: break
        chunks += chunk
        got += len(chunk)
    return json.loads(chunks.decode("utf-8"))

# 本地自测报头逻辑
body = json.dumps({"cmd": "ls", "out": "x" * 3000}).encode()
print(struct.unpack("i", struct.pack("i", len(body)))[0] == len(body))  # True
```

---

## ⌨️ 多进程创建 / join / 数据隔离


🎯 **这段练什么:** 两种创建方式(Process传target / 继承重写run);join=等它跑完;**进程间数据隔离**要亲手看一次。Windows 必加 main 保护!

```python
from multiprocessing import Process

def work(x):
    x = 200
    print("子进程里 x =", x)

if __name__ == "__main__":      # Windows多进程必写!
    x = 100
    p = Process(target=work, args=(x,))
    p.start()
    p.join()                    # 等子进程结束再往下
    print("主进程里 x =", x)     # 100:进程间数据隔离

# 输出:
# 子进程里 x = 200
# 主进程里 x = 100
```

---

## ⌨️ 互斥锁:多人抢票只卖一张


🎯 **这段练什么:** 共享数据竞争:不加锁会**超卖**;`with lock:` 包住"查-改"两步。锁的粒度越小越好,别把整个循环锁进去。

```python
from threading import Thread, Lock

ticket = 1                     # 只剩1张票
lock = Lock()

def grab(name):
    global ticket
    with lock:                 # 上锁:查-改 两步变成原子
        if ticket > 0:
            print(name, "购票成功")
            ticket -= 1
        else:
            print(name, "没票了")

if __name__ == "__main__":
    ts = [Thread(target=grab, args=("用户" + str(i),)) for i in range(3)]
    for t in ts: t.start()
    for t in ts: t.join()
    # 一次只有一个成功,另外两个"没票了"
```

---

## ⌨️ 生产者消费者模型(Queue + 哨兵)


🎯 **这段练什么:** Queue 自带锁;生产完放 **None 哨兵**通知收工。注意哨兵数=消费者数;这模型就是爬虫"采集-解析"分工的骨架。

```python
from queue import Queue
from threading import Thread

q = Queue(maxsize=5)           # 满了put会阻塞,天然限流

def producer():
    for i in range(1, 5):
        q.put(f"任务{i}")
        print("生产:任务", i)
    q.put(None)                # 哨兵:告诉消费者收工

def consumer():
    while True:
        item = q.get()
        if item is None: break
        print("消费:", item)

if __name__ == "__main__":
    Thread(target=producer).start()
    Thread(target=consumer).start()
```

---

## ⌨️ 线程池:submit / map / 结果回收


🎯 **这段练什么:** submit 提交拿 future、result() 取值;**map 批量且有序**;with 块结束自动等全部完成。IO密集(批量请求)标准写法。

```python
from concurrent.futures import ThreadPoolExecutor
import time

def download(url):
    time.sleep(0.3)             # 模拟网络IO
    return f"{url} 的内容"

if __name__ == "__main__":
    urls = ["a.com", "b.com", "c.com", "d.com"]
    start = time.time()
    with ThreadPoolExecutor(4) as pool:      # 4个工作线程
        for fut in pool.map(download, urls):  # 有序批量
            print(fut)
    print("耗时:", round(time.time() - start, 2), "秒")  # 约0.3秒而非1.2
```

---

## ⌨️ 异常处理全家桶(结构/自定义/主动抛)


🎯 **这段练什么:** 完整结构 try-except-else-finally + **自定义异常继承 Exception** + raise 主动抛。finally 遇 return 也会先执行——面试经典。

```python
class BalanceError(Exception):
    """余额不足异常"""

def withdraw(balance, amount):
    if amount > balance:
        raise BalanceError(f"余额不足:{balance}")
    return balance - amount

try:
    print(withdraw(100, 30))          # 70
    print(withdraw(70, 200))          # 抛异常
except BalanceError as e:
    print("业务错误:", e)
except Exception as e:                # 兜底放最后
    print("其他错误:", e)
else:
    print("没出异常才走这")
finally:
    print("无论如何都执行:关资源放这")
```

---

## ⌨️ 开启线程的两种方式(target / 继承重写run)


🎯 **这段练什么:** 开线程两种姿势:**Thread(target=函数)最常用**,继承重写 run 适合封装复杂逻辑。坑:`args=("x",)` 单元素元组的**逗号**不能丢;调 `start()` 才真正开线程,直接调 `run()` 只是普通函数调用。

```python
from threading import Thread

# 方式一:实例化Thread,把函数当target传入(最常用)
def download(name):
    print(name, "下载中")

t1 = Thread(target=download, args=("电影A",))  # args是元组,单个参数记得带逗号
t1.start()          # start()才真正开线程,自动去执行target

# 方式二:继承Thread,重写run方法
class MyThread(Thread):
    def __init__(self, who):
        super().__init__()
        self.who = who
    def run(self):          # start()底层就是调用run(),别自己调run
        print(self.who, "下载中")

t2 = MyThread("电影B")
t2.start()
t1.join()          # 等两个线程跑完再收尾
t2.join()
print("主线程收尾")
# 输出:两部电影各打印一次"下载中",最后打印"主线程收尾"
```

---

## ⌨️ TCP服务端并发版:一个客户端一条线程


🎯 **这段练什么:** 并发服务端雏形:**链接循环只管接待,通信循环丢给新线程**——一个客户端一条线程,A聊天时B不用排队。需服务端/客户端配合(本地演示可用本机两个终端,客户端用 cc-22 那段),代码 compile 通过,通信循环逻辑与串行版完全一致。

```python
# 并发版TCP服务端:主线程只管accept接待,每来一个客户端
# 就开一条新线程跑通信循环,互不堵塞。
# 需服务端/客户端配合:本地演示可用本机两个终端,
# 终端1跑本文件,终端2跑客户端(见cc-22的client.py),可同时开多个。
import socket
from threading import Thread

def working(conn):
    """通信循环:专职伺候一个客户端"""
    while True:
        try:
            data = conn.recv(1024)
            if not data:               # 客户端正常断开
                break
            conn.send(data.upper())    # 收到啥就大写回啥
        except ConnectionResetError:   # 客户端异常断开
            break
    conn.close()

if __name__ == "__main__":
    server = socket.socket()
    server.bind(("127.0.0.1", 8080))
    server.listen(5)
    print("服务端启动,等待客户端连接...")
    while True:                        # 链接循环:只接待,不聊天
        conn, addr = server.accept()
        print("客户端上线:", addr)
        Thread(target=working, args=(conn,)).start()  # 一客一线程
# 串行版一次只能伺候一个;线程版客户端A发消息时,B照样能秒回
```

---

## ⌨️ 线程 join / 数据共享 / is_alive / getName


🎯 **这段练什么:** 线程四连问:`join` 之后主线程才往下走、`is_alive` 判断活没活、`t1.name`(课程里的 `getName()`,新版本已弃用)拿线程名;与进程最大的不同——**线程共享进程内的全局变量**(money 变 2000100,进程版永远停在 100)。共享是双刃剑:查-改两步的竞争还得靠加锁。

```python
from threading import Thread

money = 100            # 全局变量:进程内所有线程共享这一份

def work():
    global money
    for _ in range(1000000):
        money += 1     # 两线程改的是同一个money(进程版永远是100)

if __name__ == "__main__":
    t1 = Thread(target=work)
    t2 = Thread(target=work)
    print("start前 is_alive:", t1.is_alive())   # False:还没启动
    t1.start()
    print("运行中 is_alive:", t1.is_alive())    # True:正在跑
    t2.start()
    print("t1的名字:", t1.name)   # 默认Thread-1;课程里的getName()等价但已弃用
    t1.join()          # join:等t1跑完,主线程才往下走
    t2.join()
    print("join后 is_alive:", t1.is_alive())    # False:已结束
    print("money =", money)   # 2000100:线程间数据共享,改的是同一份
    # 共享的坑:多线程同时"查-改"会竞争,抢票场景必须加锁
```

---

## ⌨️ 守护线程:主线程结束,子线程陪葬


🎯 **这段练什么:** `daemon=True` 设守护线程:**主线程代码一跑完,守护线程立刻被杀**,循环没跑完也陪葬。必须在 `start()` 之前设置;反过来,非守护线程就算不 join,主线程也会等它跑完才退出。

```python
from threading import Thread
import time

def beep():
    for i in range(10):
        time.sleep(0.1)
        print("守护线程:", i)

# daemon=True设为守护线程:主线程一结束,它立刻陪葬
# 必须在start()之前设置!(也可以先创建再 t.daemon = True)
t = Thread(target=beep, daemon=True)
t.start()

time.sleep(0.3)        # 主线程干自己的活
print("主线程代码跑完,进程直接退出")
# 守护线程大约只来得及打印0/1/2,剩下的循环被强制带走
```

---

## ⌨️ GIL验证实验:多线程算数并不快


🎯 **这段练什么:** 验证 **GIL**(全局解释器锁):同一时刻只允许一个线程执行字节码,所以两线程做纯计算和串行**耗时差不多**——多线程对计算密集型没有收益。结论:计算密集用多进程,IO 密集才用多线程/协程。

```python
from threading import Thread
import time

def count(n):
    """纯Python计算:不碰任何IO"""
    s = 0
    for i in range(n):
        s += i

N = 5_000_000

# 串行:一个算完另一个再算
start = time.time()
count(N)
count(N)
t_serial = time.time() - start

# 并发:两线程"同时"算
start = time.time()
t1 = Thread(target=count, args=(N,))
t2 = Thread(target=count, args=(N,))
t1.start(); t2.start()
t1.join(); t2.join()      # 记得join完再取耗时,否则测的是启动时间
t_concurrent = time.time() - start

print(f"串行耗时:  {t_serial:.2f}秒")
print(f"并发耗时:  {t_concurrent:.2f}秒")
print("耗时差不多!GIL让同一时刻只有一个线程在执行字节码")
print("结论:计算密集用多进程,IO密集才用多线程/协程")
```

---

## ⌨️ 死锁与递归锁 RLock


🎯 **这段练什么:** 死锁=两个线程**各拿一把锁还互等对方**,程序卡死(注释里的代码运行会卡死,理解即可,可给 `acquire(timeout=3)` 体验);解法:换成 `RLock` 递归锁——**同一线程可多次 acquire**,拿几次就 release 几次。

```python
from threading import Thread, RLock
import time

# ---------- 死锁现象(运行会卡死,理解即可)----------
# lockA, lockB = Lock(), Lock()
# def run1():
#     lockA.acquire()      # 线程1拿到A
#     time.sleep(1)        # 确保对方拿到了B
#     lockB.acquire()      # 想拿B,可B在线程2手里 -> 死等
# def run2():
#     lockB.acquire()      # 线程2拿到B
#     time.sleep(1)
#     lockA.acquire()      # 想拿A,可A在线程1手里 -> 互相等,卡死
# 想真跑一次感受卡死,可给acquire传超时:lockB.acquire(timeout=3)

# ---------- 递归锁RLock:同一线程可以多次acquire ----------
rlock = RLock()   # 内部记录锁主人+计数,自己拿几次都行

def eat(name):
    rlock.acquire()
    rlock.acquire()      # 若换成普通Lock,第二次acquire就死锁了
    print(name, "拿到两层锁,开吃")
    rlock.release()
    rlock.release()      # 拿了几次就释放几次

t1 = Thread(target=eat, args=("alex",))
t2 = Thread(target=eat, args=("egon",))
t1.start(); t2.start()
t1.join(); t2.join()
print("RLock不死锁:同一线程多次acquire只是计数+1")
```

---

## ⌨️ 信号量 Semaphore:5个人3个坑


🎯 **这段练什么:** `Semaphore(3)` 相当于 3 把钥匙:同一时刻最多放 3 个线程进入,其余排队等 release——**限流神器**(5 个线程抢 3 个坑位,分两批进)。用法和 Lock 一致,只是钥匙从 1 把变成 3 把。

```python
from threading import Thread, Semaphore
import time

sm = Semaphore(3)      # 3把钥匙:同一时刻最多3个线程同时进入

def toilet(name):
    with sm:            # 等价于 sm.acquire() / sm.release()
        print(name, "占坑")
        time.sleep(0.5)
        print(name, "出坑")

if __name__ == "__main__":
    ts = [Thread(target=toilet, args=(f"第{i}人",)) for i in range(1, 6)]
    for t in ts: t.start()
    for t in ts: t.join()
    print("5人3坑:前3个先进,出一个补一个,正好分两批")
```

---

## ⌨️ Event红绿灯 + 线程queue三种队列


🎯 **这段练什么:** `event.wait()` 挂起等通知、`event.set()` 广播放行——红绿灯/发令枪模型;线程间传数据用 queue 三件套:**Queue 先进先出、LifoQueue 后进先出、PriorityQueue 数字小的先出**,它们都自带锁。

```python
from threading import Thread, Event
import queue, time

# ---------- Event:等红灯变绿灯 ----------
event = Event()

def car():
    print("车到路口:红灯,等待")
    event.wait()          # 卡在这,直到有人 event.set()
    print("绿灯亮了,通行")

t = Thread(target=car)
t.start()
time.sleep(1)             # 红灯持续1秒
print("红灯计时结束,亮绿灯")
event.set()               # 通知所有wait的线程放行
t.join()

# ---------- 线程queue三种队列(自带锁,线程间传数据)----------
q1 = queue.Queue()              # FIFO:先进先出
for x in (1, 2, 3): q1.put(x)
print("Queue:", q1.get(), q1.get(), q1.get())     # 1 2 3

q2 = queue.LifoQueue()          # LIFO:先进后出(堆栈)
for x in (1, 2, 3): q2.put(x)
print("LifoQueue:", q2.get(), q2.get(), q2.get()) # 3 2 1

q3 = queue.PriorityQueue()      # 优先级:数字越小越先出
q3.put((20, "低优先"))
q3.put((1, "高优先"))
q3.put((10, "中优先"))
while not q3.empty():
    print("PriorityQueue:", q3.get()[1])          # 高/中/低
```

---

## ⌨️ 进程池:并行统计素数个数


🎯 **这段练什么:** `ProcessPoolExecutor` 多进程**绕开 GIL 真并行**,适合计算密集(统计素数);submit/map 用法和线程池一致。大坑:Windows 下**必须加 main 保护**,否则子进程无限递归启动直接报错。

```python
from concurrent.futures import ProcessPoolExecutor
import time

def count_prime(n):
    """数[2, n)里的素数个数——纯计算,适合多进程"""
    cnt = 0
    for num in range(2, n):
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                break
        else:
            cnt += 1     # 内层for没被break:是素数
    return cnt

if __name__ == "__main__":      # Windows下进程池同样必须有main保护!
    ns = [50000, 100000, 150000, 200000]
    start = time.time()
    with ProcessPoolExecutor(4) as pool:     # 4个工作进程
        results = list(pool.map(count_prime, ns))
    for n, c in zip(ns, results):
        print(f"{n}以内素数个数: {c}")
    print("耗时:", round(time.time() - start, 2), "秒")
    # 5万->5133,10万->9592,15万->13848,20万->17984
```

---

## ⌨️ 协程原理:yield手动切换 + gevent


🎯 **这段练什么:** 协程=单线程并发:**在 yield 处主动交出执行权**,切换时机代码说了算(与线程被系统抢占的最大区别);gevent 用 `monkey.patch_all()` 让阻塞 IO 自动触发切换——需 `pip install gevent`,没装时本段只跑上半部分(yield 演示)。

```python
# ---------- 协程原理:用yield手动切换 ----------
# 协程=单线程并发:在yield处主动交出执行权,切换时机自己说了算

def task1():
    for i in range(3):
        print("任务1:", i)
        yield              # 交出执行权,下次next从这继续

def task2():
    for i in range(3):
        print("任务2:", i)
        yield

g1, g2 = task1(), task2()
for _ in range(3):         # 我们自己当调度器:交替推进
    next(g1)
    next(g2)
# 打印顺序:任务1:0 / 任务2:0 / 任务1:1 / ... 交替执行

# ---------- gevent:遇到IO自动切换(需 pip install gevent)----------
# 本机没装gevent时跑不起来,标准写法如下(语法正确,装好即可用):
#
# import gevent
# from gevent import monkey
# monkey.patch_all()               # 把标准库的阻塞IO打补丁,遇IO自动切换
#
# def download(name):
#     print(name, "开始下载")
#     gevent.sleep(1)              # 模拟IO:必须用gevent.sleep才会切换
#     print(name, "下载完成")
#
# g1 = gevent.spawn(download, "A")   # 造协程
# g2 = gevent.spawn(download, "B")
# gevent.joinall([g1, g2])           # 等全部结束
# # 两个下载几乎同时开始,总耗时约1秒而非2秒
```

---

## ⌨️ 非阻塞IO:setblocking(False)轮询


🎯 **这段练什么:** `setblocking(False)` 后 recv 没数据就抛 `BlockingIOError`,**不傻等但得不停轮询**——'一直问好了没'的代价是空转占 CPU,所以它只是通往 IO 多路复用的中间一站。需服务端/客户端配合,本段 compile 看骨架即可。

```python
# 非阻塞IO:把socket设成非阻塞,recv没数据就抛异常,不傻等
# 需服务端/客户端配合(本机两个终端),此处看骨架逻辑,compile即可
import socket

client = socket.socket()
client.connect(("127.0.0.1", 8080))   # connect本身仍是阻塞的
client.setblocking(False)             # 之后recv/send全部变非阻塞

while True:
    try:
        data = client.recv(1024)      # 没数据:抛BlockingIOError
    except BlockingIOError:
        print("还没数据...先干点别的")  # 轮询间隙能处理别的事
        continue                      # 但马上又回来问:空转烧CPU
    if not data:
        break                         # 服务端关闭
    print("收到:", data.decode("utf-8"))
```

---

## ⌨️ IO多路复用 selectors 与 asyncio


🎯 **这段练什么:** selectors(**IO 多路复用**):一个线程注册监听一堆 socket,`select()` 阻塞到谁就绪处理谁——不空转不烧 CPU(骨架,compile 即可);asyncio 是官方协程库:`async def` 造协程、`await` 遇 IO 让出、`gather` 并发汇总(本段下半部分可直接运行)。

```python
# ---------- selectors:IO多路复用,一个线程监听一堆socket ----------
# 骨架代码,需配合客户端运行,此处compile看逻辑即可
# import selectors, socket
#
# sel = selectors.DefaultSelector()
# server = socket.socket()
# server.bind(("127.0.0.1", 8080))
# server.listen(100)
# server.setblocking(False)
# sel.register(server, selectors.EVENT_READ)   # 注册:监听"可读"事件
#
# while True:
#     events = sel.select()        # 阻塞到任一socket就绪(不烧CPU)
#     for key, mask in events:
#         if key.data is None:     # 是监听socket:有新连接
#             conn, _ = key.fileobj.accept()
#             conn.setblocking(False)
#             sel.register(conn, selectors.EVENT_READ, data=conn)
#         else:                    # 是连接socket:有数据可读
#             data = key.fileobj.recv(1024)
#             if not data:
#                 sel.unregister(key.fileobj)   # 客户端断开,取消注册
#             else:
#                 key.fileobj.send(data.upper())

# ---------- asyncio:官方协程库(可直接运行)----------
import asyncio

async def download(name):
    print(name, "开始")
    await asyncio.sleep(1)      # 遇IO主动让出,切去跑别的协程
    return name + "完成"

async def main():
    results = await asyncio.gather(    # 并发跑3个,总耗时约1秒
        download("A"), download("B"), download("C")
    )
    print(results)

asyncio.run(main())     # 3.7+的标准启动方式
# 三个"开始"几乎同时打印,约1秒后拿到全部结果
```

---

## ⌨️ 变量内存管理:引用计数与 del


🎯 **这段练什么:** 理解 Python 怎么回收内存:**引用计数**为主(名字删一个少一个),循环引用靠**标记清除**兜底。这段实验亲手看引用计数变化。

```python
import sys
a = [1, 2, 3]
print(sys.getrefcount(a))   # 2(变量a + getrefcount临时引用)
b = a
print(sys.getrefcount(a))   # 3:多了一个引用
del b                       # 删名字b,引用计数减1
print(a)                    # a 还能正常用
# 循环引用:引用计数永远不为0,靠标记清除回收
x = []
x.append(x)
del x                       # 标记清除负责回收
```

---

## ⌨️ 列表与元组操作清单


🎯 **这段练什么:** 列表增删改查+排序+反转全套;元组**只读**(只能数和查)。`tuple(lst)` 一转换就锁死,需要改就用列表。

```python
lst = [3, 1, 4, 1, 5]
lst.insert(0, 9)          # 指定位置插入
lst.sort()                # 原地排序
print(lst)                # [1, 1, 3, 4, 5, 9]
print(lst.index(4))       # 查位置
lst.reverse()             # 反转
print(lst)

t = (1, 2, 3)             # 元组:不可变
print(t[0], len(t))
# t[0] = 9                # TypeError: 不支持修改
print(tuple([7, 8]))      # 列表转元组
```

---

## ⌨️ 编码解码实战:utf-8 与 gbk


🎯 **这段练什么:** str 与 bytes 双向转换;同一句话两种编码**字节数不同**;编码错配就是乱码/报错的根源——文件操作三配合的底层原因。

```python
s = "Python人生"
b1 = s.encode("utf-8")
b2 = s.encode("gbk")
print(len(b1), len(b2))          # 字节数不同
print(b1.decode("utf-8"))        # 正确解码
print(b2.decode("gbk"))          # 正确解码
try:
    b1.decode("gbk")             # 编码错配 -> 乱码或报错
except UnicodeDecodeError as e:
    print("错配报错:", e)
```

---

## ⌨️ 函数定义三种形式与返回值


🎯 **这段练什么:** 空函数(占位)/有参无返回/有参有返回;**return 可以一次返回多个值**(本质是元组);没写 return 默认返回 None。

```python
def empty():            # 空函数:先占位再实现
    pass

def no_return(x):       # 有参无返回
    print(x * 2)

def calc(a, b):         # 有参有返回
    return a + b, a * b # 多值返回:本质是元组

print(no_return(3))     # 打印6,函数本身返回None
print(calc(3, 4))       # (7, 12)
print(empty())          # None
```

---

## ⌨️ 函数对象:函数能当参数传


🎯 **这段练什么:** 函数和数字一样是对象:能**赋值、存进列表、当参数传**。闭包和装饰器的地基——先接受"函数是值"。

```python
def add(x):
    return x + 1

def mul(x):
    return x * 2

ops = [add, mul]              # 函数存进列表
for f in ops:
    print(f(10))              # 11 / 20

def apply(func, x):           # 函数当参数传
    return func(x)

print(apply(add, 5))          # 6
print(apply(mul, 3))          # 6
```

---

## ⌨️ lambda 与 map / filter / reduce


🎯 **这段练什么:** 匿名函数一行搞定简单逻辑;**map 逐个变换、filter 过滤、reduce 累计**;配合 sorted 的 key 参数就是排序利器。

```python
from functools import reduce

nums = [1, 2, 3, 4, 5]
print(list(map(lambda x: x * 2, nums)))       # 全部翻倍
print(list(filter(lambda x: x > 2, nums)))    # 过滤
print(reduce(lambda a, b: a + b, nums))       # 累计:15

students = [("alex", 80), ("yuan", 95), ("eva", 88)]
print(sorted(students, key=lambda t: t[1], reverse=True))  # 按分数降序
```

---

## ⌨️ random 验证码 / os 目录操作 / time 计时


🎯 **这段练什么:** 三个高频模块小工具:**随机验证码、遍历目录找文件、程序计时**——作业和项目里天天用。

```python
import random, os, time

chars = "0123456789abcdefghijklmnopqrstuvwxyz"
code = "".join(random.choices(chars, k=4))
print("验证码:", code)

print("当前目录的py文件:", [f for f in os.listdir(".") if f.endswith(".py")])

start = time.time()
time.sleep(0.3)
print("耗时:", round(time.time() - start, 3), "秒")
```

---

## ⌨️ json / pickle 序列化 与 hashlib 加盐


🎯 **这段练什么:** **json** 存人能读的文件(跨语言通用);**pickle** 存 python 对象(更快但只限python);**加盐** = 密码+盐一起算MD5,防彩虹表破解。

```python
import json, pickle, hashlib

user = {"name": "alex", "scores": [80, 95]}
with open("u.json", "w", encoding="utf-8") as f:
    json.dump(user, f, ensure_ascii=False)      # 存:人能读
with open("u.json", encoding="utf-8") as f:
    print(json.load(f))                          # 取

with open("u.pkl", "wb") as f:
    pickle.dump(user, f)                        # pickle 存对象
with open("u.pkl", "rb") as f:
    print(pickle.load(f))

pwd, salt = "123456", "abc123"
m = hashlib.md5()
m.update((pwd + salt).encode("utf-8"))
print("加盐MD5:", m.hexdigest())
```

---

## ⌨️ logging 最小可用版


🎯 **这段练什么:** logging 比 print 专业:**分级别、能落盘**;开发期用 DEBUG,上线改 WARNING。字典完整配置见「代码模板速查」章,这是最小上手版。

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,                          # 低于DEBUG的忽略
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename="app.log",                           # 写到文件
    encoding="utf-8",
)
logging.debug("调试信息")
logging.warning("警告:磁盘快满了")
logging.error("出错了!")
print("日志已写入 app.log")
```

---

## ⌨️ 元类与 __call__ 一页入门


🎯 **这段练什么:** **type(类名, 父类, 属性字典)** 能动态造类——这就是 class 语句背后做的事(元类的本质);对象加 **__call__** 后能像函数一样被调用。

```python
class Greeter:
    def __call__(self, name):     # 对象可调用
        return f"你好,{name}"

g = Greeter()
print(g("alex"))                  # 像函数一样调用

# type 动态造类(元类的本质)
Dog = type("Dog", (object,), {"sound": "汪汪", "bark": lambda self: self.sound})
d = Dog()
print(d.bark())
print(type(Dog))                  # <class 'type'>:类也是对象
```

---

## ⌨️ re 正则:提取手机号与分组


🎯 **这段练什么:** **findall** 提取全部匹配、**match** 从头匹配、**分组()** 拿子串、**sub** 替换打码——爬虫与日志解析必备。

```python
import re

text = "电话:13812345678,备用:15987654321;邮箱 alex@xx.com"
print(re.findall(r"1[3-9]\d{9}", text))      # 提取手机号

m = re.match(r"(\w+)@(\w+)\.com", "alex@xx.com")
print(m.group(0), m.group(1), m.group(2))    # 整体/分组1/分组2

print(re.sub(r"\d", "*", "号码110101199001011234"))  # 替换打码
```

---
