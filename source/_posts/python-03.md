---
title: 函数与模块
date: 2026-11-03 09:00:00
tags:
  - Python
  - 基础
categories:
  - Python基础
---

> 我的学习笔记,边学边记,持续修订。

## 📖 函数


### 1. 函数定义与返回值

**函数用 `def` 定义,**没有 return 或只写 return 时默认返回 None**;return a, b 本质是返回一个**元组**。**

- 定义:`def 函数名(参数):` + 缩进的函数体;函数**先定义后调用**,定义时函数体并不执行
- return 会**立即结束函数**;没有 return 或 return 后面不带值,统一返回 None
- `return a, b` 是把两个值打包成**元组**返回,接收时 `a, b = f()` 解包
- 函数体第一行可写三引号字符串作文档说明,用 `函数名.__doc__` 查看
- 函数名遵循变量命名规范,且不能与内置函数重名(如自定义 list 会遮蔽内置 list)

```python
def my_max(a, b):
    """返回较大的数"""
    return a if a > b else b

print(my_max(3, 7))     # 7
print(my_max.__doc__)   # 返回较大的数
```

*定义函数并调用*

### 2. 函数参数(位置/关键字/默认/*args/**kwargs)

**常见定义顺序:**位置参数 → 默认参数 → *args → **kwargs**;默认参数**千万不要用可变类型**,否则多次调用共享同一个对象。**

- 位置参数按顺序对应;关键字参数指名道姓传 `f(age=18)`,可以不按顺序
- 默认参数要写在位置参数后面:`def f(a, b=1)` 合法,`def f(a=1, b)` 直接报错
- **坑**:默认值是 list/dict 等可变类型时,它在**定义时只创建一次**,多次调用会往同一个列表里追加
- 标准解法:默认值写 None,函数体内 `if lst is None: lst = []` 再创建新列表
- `*args` 收集多余**位置参数**成**元组**;`**kwargs` 收集多余**关键字参数**成**字典**

```python
def f(a, b=2, *args, **kwargs):
    print(a, b, args, kwargs)

f(1)                 # 1 2 () {}
f(1, 9, 3, 4, x=5)   # 1 9 (3, 4) {'x': 5}

def add(x, lst=None):   # 避开可变默认参数的坑
    if lst is None:
        lst = []
    lst.append(x)
    return lst

print(add(1), add(2))   # [1] [2]
```

### 3. 名称空间与作用域(LEGB、global/nonlocal)

**取值顺序 **LEGB:Local → Enclosing → Global → Built-in**;函数内给全局变量**重新赋值**要 global,嵌套函数改外层变量要 nonlocal。**

- 三类名称空间:内置、全局、局部;加载顺序 内置→全局→局部,查找名字按 **LEGB**
- 函数内只读全局变量不用声明;**重新赋值**不可变类型的全局变量必须 `global x`
- 直接修改全局**可变对象**的内容(append 等)不需要 global,因为只是改内容、没有改变量的指向
- `nonlocal` 只作用于**外层函数**的局部变量,和全局名称空间无关
- 作用域在**函数定义时**就确定了,和在哪里调用无关

```python
x = 1
def f():
    global x
    x = 10
f()
print(x)   # 10

def outer():
    n = 0
    def inner():
        nonlocal n
        n += 1
        return n
    return inner

inc = outer()
print(inc(), inc())   # 1 2  闭包让 n 常驻内存
```

### 4. 闭包与装饰器(含带参装饰器)

**闭包 = **内层函数引用外层函数变量 + 外层返回内层函数**;装饰器本质是“接收函数、返回函数”的闭包,`@deco` 就是 `func = deco(func)` 的语法糖。**

- 装饰器在**函数定义时**立即执行(打印装饰器内的 print 会先出现),原函数在**调用时**才执行
- wrapper 里通常 `*args, **kwargs` 透传参数、`return func(...)` 透传返回值,保证和原函数行为一致
- 被装饰后函数名其实指向 wrapper,可用 `functools.wraps(func)` 保留原函数的元信息
- 带参装饰器是**三层**嵌套:`@deco(arg)` 先执行 deco(arg) 返回真正的装饰器,再装饰函数
- 典型用途:登录验证、计时、日志,不改原函数代码就能加功能

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(func.__name__ + " 被调用")
        return func(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    return a + b

print(add(1, 2))   # 先打印 add 被调用,再打印 3
```

*装饰器基本结构*

### 5. 迭代器与生成器(yield、next)

**函数里一出现 **yield** 就变成生成器函数;生成器用 `next()` 逐个取值、**取完抛 StopIteration**,惰性求值省内存,只能向前走一遍。**

- 可迭代对象(list/str/dict…)用 `iter()` 拿到迭代器;迭代器同时实现 `__iter__` 和 `__next__`
- for 循环本质:先 `iter()`,再不断 `next()`,捕获 StopIteration 自动结束
- 执行到 yield 会**暂停**并交出一个值,下次 next 从暂停处继续;调用函数拿到的是生成器对象而不是返回值
- 生成器**不能回头重遍历**,耗尽后要重新创建;适合大文件、死循环数据流等省内存场景
- 生成器表达式把 [] 换成 ():`(x * 2 for x in range(3))`,用 list() 才能看到全部结果

```python
def gen():
    yield 1
    yield 2

g = gen()
print(next(g), next(g))   # 1 2
# print(next(g))          # 再取就抛 StopIteration

g2 = (x * 2 for x in range(3))
print(list(g2))           # [0, 2, 4]
```

### 6. 递归、lambda 与常用内置函数

**递归必须有**出口**,默认深度上限约 1000;`lambda 参数: 表达式` 配合 **map / filter / sorted / zip / max / min / enumerate** 处理序列最常用。**

- 递归:函数自己调用自己;没有出口会 RecursionError,深度上限约 1000(`sys.getrecursionlimit()` 查看)
- `map(f, it)` 逐个加工、`filter(f, it)` 留下为 True 的;都返回迭代器,要 `list()` 才能直接看
- `sorted(lst, key=函数, reverse=True)` 排序;`max/min` 也支持 key,如按字典值找最大
- `zip(a, b)` 按位配对成元组;`enumerate(lst)` 同时给下标和值
- lambda 冒号后只能是**一个表达式**,常作 sorted/map/filter 的参数一次性使用

```python
nums = [3, -1, 2]
print(sorted(nums, key=abs))                # [-1, 2, 3]
print(list(map(str, [1, 2])))               # ['1', '2']
print(list(filter(lambda x: x > 0, nums)))  # [3, 2]
print(list(zip([1, 2], "ab")))              # [(1, 'a'), (2, 'b')]
print(list(enumerate("xy")))                # [(0, 'x'), (1, 'y')]

def fact(n):   # 递归要有出口
    return 1 if n <= 1 else n * fact(n - 1)

print(fact(5))   # 120
```

### 7. 函数定义的三种形式与调用形式

**定义函数三形式:**无参、有参、空函数**;空函数用 pass 占位、先搭项目骨架再逐步实现;调用函数有语句、表达式、当参数三种用法。**

- 无参函数:def hello(): ...,功能不依赖外部数据,直接 hello() 调用
- 有参函数:结果随外部输入变化,把依赖做成参数:def my_max(a, b) —— 参数是函数与外界的"接口"
- 空函数:函数体写 pass(或只写文档字符串),先把程序有哪些功能想清楚、占好位置,再逐个填充 —— 项目开发先搭框架的常用手段
- 调用函数的三种形式:① 语句形式:只执行功能不要返回值 f() ② 表达式形式:拿返回值参与运算 x = f() * 2 ③ 函数当参数:sorted(lst, key=f),把函数名传给另一个函数
- 记住:定义时不执行函数体,调用才执行;必须**先定义后调用**,先写调用行会 NameError

```python
def register():
    """注册功能(待实现)"""
    pass            # 空函数:先占位

def my_max(a, b):   # 有参:依赖外部数据
    return a if a > b else b

print(my_max(3, 7))   # 7
```

*函数定义三形式*

### 8. 递归的两个阶段与二分法

**递归 = **递推(层层深入)→ 回溯(层层带回)**,必须写**出口**,否则 RecursionError;二分法在**有序**数据上每次排除一半,最多 log₂n 次定位。**

- 递推阶段:函数不断自己调用自己,问题规模一点点缩小;碰到**出口**(终止条件)停止递推
- 回溯阶段:从最里层开始一层层往回返回结果,把答案带回最外层 —— 先递推到底、再回溯返回
- 没有出口 → 无限递归,触发 RecursionError;py 默认递归深度约 1000(sys.getrecursionlimit() 查看)
- 二分法前提:**序列必须有序**(先 sort);拿中间值与目标比较,中间值小了去右半边找、大了去左半边找,区间为空说明不存在
- 效率:10 万个数据最多约 17 次比较(2^17 ≈ 13 万),比从头遍历快得多;可用 while 循环或递归实现

```python
def binary_search(lst, target):
    left, right = 0, len(lst) - 1
    while left <= right:
        mid = (left + right) // 2
        if lst[mid] == target:
            return mid           # 找到,返回下标
        if lst[mid] < target:
            left = mid + 1       # 去右半边
        else:
            right = mid - 1      # 去左半边
    return -1                    # 不存在

print(binary_search([1, 3, 5, 7, 9], 7))   # 3
```

*二分查找(非递归版)*

### 9. yield 表达式形式(send 给 yield 传值)

**`data = yield 值` 是 yield 的**表达式形式**:用 **g.send(v)** 可以在生成器暂停时给它传值,生成器从"只输出"升级为"能收能发"。**

- x = yield 值:next() 推进时交出右边的值并暂停;g.send(v) 会先把 v 赋给 x,再推进到下一个 yield
- **先初始化再 send**:生成器刚创建停在函数开头,还没走到 yield,直接 g.send(值) 报 TypeError;必须先 next(g) 或 g.send(None) 推到第一个 yield
- send 的返回值:推进后停在的下一个 yield 右边的值 —— 一次 send 既是"传值进去"也是"取值出来"
- 典型结构:生成器里 while True + x = yield,不断接收外部数据做加工(吃包子案例);用完 g.close() 关闭
- 这是协程思想的雏形:程序在"暂停点"之间双向传值,asyncio 的底层思路与之一脉相承(了解)

```python
def eater():
    while True:
        food = yield "等待投喂"
        print("吃到:", food)

g = eater()
print(next(g))         # 先初始化:等待投喂
print(g.send("包子"))  # 吃到: 包子,返回下一个 yield 值
print(g.send("饺子"))  # 吃到: 饺子
g.close()
```

*send 给 yield 传值*

### 10. 面向过程与函数式编程思想

****面向过程**:把大问题拆成一步一步的小函数按流水线执行,核心是"步骤";**函数式**:用纯函数 + lambda/map/filter/reduce 处理数据,不依赖外部状态。**

- 面向过程:关注"先干什么、再干什么",把复杂流程拆成一个个函数按顺序调用,像工厂流水线;写起来直接,适合脚本、小工具
- 短板:步骤之间靠变量传递状态,一处修改可能牵连整条流水线,程序变大后难维护 —— 这正是后来引入面向对象的原因
- 函数式思想:源自数学函数 —— **相同输入永远得到相同输出、不修改外部变量**(纯函数),代表工具 lambda、map、filter、reduce
- functools.reduce(f, 序列):把前两个元素算出的结果继续和下一个元素累计运算,reduce(lambda x, y: x + y, [1, 2, 3, 4]) → 10(累加器)
- 实际开发是混合风格:流程骨架用面向过程组织,数据加工环节用 map/filter/reduce 这类无状态小函数

```python
from functools import reduce
nums = [1, 2, 3, 4]
total = reduce(lambda x, y: x + y, nums)          # 10
even_doubled = list(map(lambda x: x * 2,
                        filter(lambda x: x % 2 == 0, nums)))
print(total, even_doubled)   # 10 [4, 8]
```

*函数式小函数组合*

### 11. 函数对象与函数嵌套

**函数名就是变量名——函数是**第一类对象**:可以赋值给变量、当参数、当返回值、存进容器按名字调用;函数体内还能**嵌套定义**另一个函数,嵌套定义是闭包的前提。**

- 函数对象四大用法:`f = foo` 赋值给变量、把函数名**当参数**传给别的函数、`return foo` 当返回值、把函数存进 dict/list 按名字调度
- 函数名**不带括号**是函数本身(对象),**带括号**才是调用执行 —— `func_map["login"]` 拿到函数,`func_map["login"]()` 才执行
- 经典应用:用字典 + 函数对象替代一长串 if/elif 分支(模拟 switch),新增功能只要往字典里加一条,主逻辑不用改
- 嵌套定义:函数体里 def 的函数只在外层函数体内可见,出了外层作用域就取不到 —— 想在外面用,必须让外层把它 return 出去
- 嵌套调用 vs 嵌套定义:前者是在函数体里**调用**已定义好的函数,后者是在函数体里**定义**新函数;闭包 = 嵌套定义 + 内层引用外层变量 + 外层返回内层

```python
def login():
    return "登录成功"

def pay():
    return "支付成功"

func_map = {"login": login, "pay": pay}   # 函数当值存进字典
print(func_map["login"]())                # 登录成功

def outer():
    def inner():                          # 嵌套定义
        return "inner 执行"
    return inner                          # 函数当返回值带出去

f = outer()
print(f())                                # inner 执行
```

*函数对象与嵌套定义*

### 12. 叠加多个装饰器的执行顺序

**多个装饰器**从下往上**依次包装(离 def 最近的先包),调用时**从上往下**执行 wrapper 代码——口诀:装饰从下往上,执行从上往下,像洋葱一层套一层。**

- @deco1 在上、@deco2 在下:加载阶段先执行 deco2(hello) 得到新函数,再执行 deco1(新函数)——等价于 hello = deco1(deco2(hello))
- 最外层的 wrapper 来自**最上面的**装饰器 deco1,调用 hello() 时最先执行它的前半段
- 执行顺序像洋葱:deco1 前半段 → deco2 前半段 → 原函数 → deco2 后半段 → deco1 后半段;打印语句写在 func() 之前属于前半段、之后属于后半段
- 实战建议:和业务强相关的装饰器放里层,通用能力(计时、日志)放外层;叠太多层排查困难,每层职责要单一

```python
def deco1(func):
    def wrapper():
        print("deco1 before")
        func()
        print("deco1 after")
    return wrapper

def deco2(func):
    def wrapper():
        print("deco2 before")
        func()
        print("deco2 after")
    return wrapper

@deco1   # hello = deco1(deco2(hello))
@deco2
def hello():
    print("hello")

hello()
# 输出:deco1 before -> deco2 before -> hello -> deco2 after -> deco1 after
```

*双层装饰器洋葱模型*

### 13. 三元表达式与列表生成式

**`值1 if 条件 else 值2` 一行写完取值逻辑;`[表达式 for x in 可迭代 if 条件]` 一行生成列表,换成 {} 写字典/集合生成式、换成 () 写生成器表达式。**

- 三元表达式:res = "及格" if score >= 60 else "不及格" —— 先写条件成立的值,再写 if 条件、else 不成立的值,**必须有 else** 不能省
- 列表生成式语法:[处理后的值 for 变量 in 可迭代对象 if 筛选条件],if 筛选可省略;执行顺序是先跑 for、再过 if、最后算表达式
- 两种条件位置别混:写在 for **后面**的是筛选(不满足直接丢弃),写在 for **前面**的是三元表达式(每个元素都要给出结果)
- 其他生成式:{k: v for ...} 字典生成式、{x for ...} 集合生成式、(x for ...) 生成器表达式(惰性,用 next 或 for 消费)
- 一行写得清楚才用生成式;要套两层以上 for/if 就老老实实写普通循环,可读性优先

```python
scores = [55, 72, 90]
print(["及格" if s >= 60 else "不及格" for s in scores])
# ['不及格', '及格', '及格']

nums = [1, 2, 3, 4, 5, 6]
print([x * x for x in nums if x % 2 == 0])   # [4, 16, 36]

print({x: x ** 2 for x in (1, 2, 3)})        # {1: 1, 2: 4, 3: 9}
g = (x for x in nums if x > 3)               # 生成器表达式
print(next(g))                               # 4
```

*生成式家族*

### 14. 迭代器优缺点总结

**优点:**惰性求值省内存**、提供统一遍历协议(不依赖下标);缺点:**只能向前不能后退**、**没有 len() 不支持下标**、耗尽即废。**

- 优点一 惰性:next 一次才计算一个值,处理超大文件、无限数据流时内存占用恒定 —— 这是迭代器/生成器最大的价值
- 优点二 通用:list/str/dict/文件对象都能用同一套 for + next 遍历,不要求容器支持下标访问,协议统一
- 缺点一 不能回头:迭代器没有指针回退,想重头再来只能重新 iter() 或重建生成器
- 缺点二 不好定位:len(it) 报错、it[0] 报错,只能逐个 next 或用 for 消费;想要第 5 个元素就得先走完前 4 个
- 选型结论:一次性顺序消费、大数据要省内存 → 迭代器/生成器;需要反复随机访问、多次遍历 → 老实用 list

```python
it = iter([1, 2, 3])
print(next(it))     # 1 惰性取值
print(list(it))     # [2, 3] 只剩没取过的
# print(len(it))    # TypeError:迭代器没有长度
# print(it[0])      # TypeError:不支持下标
```

*迭代器的长与短*

## 📖 模块与常用模块


### 1. 模块与包、import 机制

**import 时模块顶层代码**只执行一次**(有缓存);`from m import x` 直接用名字;测试代码要放在 `if __name__ == "__main__":` 下。**

- 模块就是一个 .py 文件;包是含 `__init__.py` 的文件夹,导入包时先执行包下的 `__init__.py`
- `import m` 后用 `m.x`;`from m import x` 直接用 x;`from m import x as y` 可起别名
- `__name__` 被直接运行时是 "__main__",被导入时是模块名,常用来让测试代码只在直接运行时执行
- 搜索路径:先内存中已加载的 → 内置模块 → `sys.path`(通常第一个是脚本所在目录)
- 循环导入(两个模块互相 import)会报错:把公共内容抽到第三个模块,或把 import 写进函数里延迟导入

```python
# 文件 mymod.py
print("mymod 模块被加载")

def hi():
    print("hi")

if __name__ == "__main__":
    hi()   # 只有直接运行 python mymod.py 才执行

# 文件 main.py
import mymod    # 只打印: mymod 模块被加载,不会执行 hi()
mymod.hi()
```

*__name__ 的作用*

### 2. os 与 sys

**os 负责**操作系统**(目录、文件、路径),sys 负责 **Python 解释器本身**(命令行参数、搜索路径、递归深度)。**

- `os.getcwd()` 当前工作目录、`os.listdir()` 列目录、`os.makedirs()` 递归建目录、`os.remove()` 删文件
- `os.path.join()` 按平台拼路径、`os.path.exists()` 判断存在、`os.path.basename/dirname` 取文件名/目录名
- `os.name` 看平台、`os.sep` 路径分隔符(win 是 \,linux/mac 是 /)
- `sys.argv` 命令行参数列表(argv[0] 是脚本名)、`sys.path` 模块搜索路径、`sys.exit()` 退出程序
- `sys.modules` 记录已加载的模块;`sys.getrecursionlimit()` 查看递归上限

```python
import os, sys
print(os.getcwd())              # 当前工作目录
print(os.path.exists("a.txt"))  # True / False
print(os.path.join("a", "b"))   # a/b 或 a\b(看平台)
print(sys.argv)                 # ['脚本名', '命令行参数...']
```

### 3. time / datetime / random

**`time.time()` 拿时间戳、`time.strftime()` 格式化;datetime 用 `timedelta` 做日期加减;random 的 `randint(a, b)` **含 a 也含 b**。**

- 时间三种表示:时间戳(float)、格式化字符串、结构化时间 struct_time,`time.localtime()` 转结构化
- `time.strftime("%Y-%m-%d %H:%M:%S")` 格式化输出;`time.sleep(秒)` 让程序暂停
- `datetime.datetime.now()` 当前时间,`± datetime.timedelta(days=3)` 算前后三天
- `random.random()` 得 [0,1) 小数、`random.randint(a, b)` 含两端整数、`random.choice(seq)` 随机取一个
- `random.shuffle(lst)` 原地打乱;`random.sample(seq, n)` 不重复抽样,适合做验证码

```python
import time, datetime, random
print(time.strftime("%Y-%m-%d"))          # 如 2020-03-01
now = datetime.datetime.now()
print(now - datetime.timedelta(days=3))   # 三天前
print(random.randint(1, 6), random.choice("abc"))   # 1~6 的整数、随机字符
```

### 4. json 与 pickle(序列化)

**两者都做序列化:**json 是跨语言通用文本但类型少**,**pickle 是 Python 专有、几乎什么对象都能存**,但反序列化不可信数据有安全风险。**

- json 四件套:`dumps/loads`(对象↔字符串)、`dump/load`(对象↔文件)
- json 只支持 str/int/float/bool/None/list/dict(tuple 会转成列表)
- json 与 Python 的差异:True→true、False→false、None→null,引号统一变双引号
- pickle 是二进制字节,能存函数、对象等几乎全部 Python 类型,只适合 Python 自己保存数据
- `pickle.loads` 可能执行任意代码,**永远不要**加载来历不明的 pickle 数据

```python
import json, pickle
s = json.dumps({"ok": True, "n": None})
print(s)             # {"ok": true, "n": null}
d = json.loads(s)    # 还原回字典
b = pickle.dumps([1, 2])
print(pickle.loads(b))   # [1, 2]
```

### 5. re 正则表达式

**常用元字符 `\d \w \s . * + ? {n,m} [] |`;**match 只匹配开头,search 找第一个,findall 返回所有匹配的列表**;量词默认贪婪,加 ? 变非贪婪。**

- 元字符:`\d` 数字、`\w` 字母数字下划线、`\s` 空白、`.` 除换行外任意字符、`^` 开头、`$` 结尾
- 量词:`*` 0次以上、`+` 1次以上、`?` 0或1次、`{2,5}` 2到5次;默认**贪婪**尽可能多匹配
- match 从头匹配失败返回 None;search 返回第一个 Match 对象,`m.group()` 取内容、`m.group(1)` 取分组
- findall 直接返回**所有匹配组成的列表**;正则里有分组时,返回的是分组内容
- 写法:`re.findall(r"\d+", s)`,加 r 原始字符串避免转义问题;字符组 `[.]` 里就是字面量的点

```python
import re
print(re.findall(r"\d+", "a1b22c333"))   # ['1', '22', '333']
m = re.search(r"(\d+)-(\d+)", "2020-03")
print(m.group(0), m.group(1), m.group(2))   # 2020-03 2020 03
print(re.findall(r"a.+?", "aab"))           # ['aa'] 非贪婪
```

### 6. hashlib 加密与 logging 日志

**hashlib 提供 **md5/sha 系列**单向摘要:只认**字节**、不可逆,常用来“存摘要不存明文”;logging 五个级别 **DEBUG < INFO < WARNING < ERROR < CRITICAL**,默认只输出 WARNING 及以上。**

- `update()` 必须传字节:`hashlib.md5("abc".encode("utf-8"))`;`hexdigest()` 返回十六进制字符串
- 摘要不可逆:数据库一般存密码摘要而不是明文;相同内容摘要一定相同,可加“盐”防彩虹表
- `update()` 可以多次调用,效果等同于把所有内容拼接后一次性 update
- `logging.basicConfig(level=logging.INFO, format=...)` 设置级别和格式
- 级别低于设定值的不输出:设为 INFO 后,debug 看不到、info 及以上能看到

```python
import hashlib
m = hashlib.md5()
m.update("hello".encode("utf-8"))
m.update("world".encode("utf-8"))
print(m.hexdigest() == hashlib.md5(b"helloworld").hexdigest())   # True

import logging
logging.basicConfig(level=logging.INFO)   # 低于 INFO 的不输出
logging.info("系统启动")
```

### 7. 包与相对导入

**包 = 含 **__init__.py** 的文件夹;包内用**相对导入**(. 本包、.. 上一级包)组织模块,但相对导入**只能在包内使用**,直接运行包内文件会报错。**

- 导入包本质是执行包下的 __init__.py;包用来把一组相关模块组织成层级结构,避免所有模块堆在顶层互相重名
- 绝对导入:from mypkg import utils、from mypkg.api import core,以顶层包名开头写全路径,任何入口都能用
- 相对导入:from . import utils(本包)、from .. import utils(上一级包)、from .helper import run;**只有被当成包导入时**才能解析 . 和 ..
- 大坑:直接 python mypkg/api/core.py 运行,该文件没有"包"身份,相对导入抛 ImportError;正确姿势是 python -m mypkg.api.core 或改用绝对导入
- __init__.py 常用来汇总导出:里面写 from .utils import f1,外部就能 from mypkg import f1,调用方更简洁

```python
# 目录:mypkg/__init__.py  mypkg/utils.py  mypkg/api/core.py
# core.py 内部:
from .. import utils          # 上一级包 mypkg 的 utils
from .helper import run       # 同包 api 下的 helper

# 运行方式决定成败:
# python mypkg/api/core.py      ❌ 相对导入报错
# python -m mypkg.api.core      ✅ 以包方式运行
```

*相对导入与运行方式*

### 8. 软件开发的目录规范

**项目按固定目录分层:**bin(启动)/ conf(配置)/ core(业务)/ db(数据)/ lib(公共库)/ log(日志)**,入口负责把项目根目录加入 sys.path。**

- 典型结构:bin/start.py 是**唯一启动入口**;conf/settings.py 放配置;core/src.py 写核心业务;db/db_handle.py 管数据文件;lib/common.py 放公共函数(校验、加密);log/access.log 记日志
- 入口第一件事:把项目根目录加进 sys.path(sys.path.append(根目录路径)),否则 from core import ... 找不到模块
- 配置与代码分离:路径、开关、密钥等常变的东西放 settings.py,业务里 from conf import settings 读 —— 改配置不改代码
- lib 是"人人可用"的公共层,谁都可以 import 它;core 只编排业务流程,不写底层工具函数
- 再加 README.md 说明项目介绍与运行方式;规范的价值:团队协作、排查问题都按固定位置找文件,新人上手快

### 9. configparser、shelve 与 xml

**三个"存取数据"的补充工具:**configparser** 读写 ini 配置、**shelve** 把字典直接持久化到文件、**xml** 解析标签式老格式(了解)。**

- configparser:操作 xxx.ini;结构是 [section] 下 key = value;config.read("conf.ini") 读入,config["section"]["key"] 取值(全是字符串),改完要 config.write(f) 才落盘
- shelve:import shelve;d = shelve.open("data") 得到一个**持久化字典**,d["user"] = 任意 Python 对象,close 时自动序列化存盘 —— 比 pickle 更省心的本地缓存
- xml:标签嵌套的数据格式,标准库 xml.etree.ElementTree 解析:tree = ET.parse("x.xml");root = tree.getroot();root.iter("标签") 遍历
- 选型:程序配置用 configparser(更现代可换 yaml,需第三方库);本地对象缓存用 shelve;跨语言交换数据还是 json 为主;xml 多见于老系统对接

```python
import configparser
c = configparser.ConfigParser()
c["server"] = {"port": "8000"}
with open("conf.ini", "w") as f:
    c.write(f)
print(c["server"]["port"])    # 8000

import shelve
db = shelve.open("data")
db["user"] = {"name": "alex"}
db.close()
```

*configparser 与 shelve*

### 10. 猴子补丁(monkey patch)

****猴子补丁 = 程序运行中动态替换模块/类的属性方法**:`模块.名字 = 新函数` 就完成替换;典型用途是把慢实现悄悄换成快实现,调用方一行不改。**

- 原理:Python 属性在运行期随时可改,import json 后执行 json.loads = my_fast_load,之后所有 json.loads 都走新实现
- 经典案例:用性能更好的 ujson 替换标准库 json —— 业务代码里仍然 import json、json.dumps(...),实际干活的是 ujson
- 打补丁的时机:尽量在**程序入口处统一打**,越早越好;散落在各处打补丁会让行为不可预测
- 代价:补丁让"看到的代码"和"实际执行的代码"不一致,排查问题要绕个弯;必须在注释里写清楚补丁的目的
- 它也是一种"不改源码改行为"的思想,本质是鸭子类型给的运行时自由

```python
# pip install ujson 之后,在程序入口统一打补丁:
import json, ujson
json.dumps = ujson.dumps    # 猴子补丁
print(json.dumps({"a": 1}))  # 调用方无感知,实际由 ujson 执行
```

*猴子补丁替换 json 实现*

### 11. subprocess 执行系统命令

****subprocess** 在 Python 里执行操作系统命令并**拿到输出结果**,是 os.system 的升级版,自动化运维脚本的标配。**

- res = subprocess.run("命令", shell=True) 执行命令,返回 CompletedProcess 对象;res.returncode 是退出码,0 表示成功
- 拿输出:run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE),结果在 res.stdout / res.stderr(bytes),要 .decode() 才能看
- Windows 命令行输出默认是 **gbk** 编码,res.stdout.decode("gbk");Linux/Mac 一般 decode("utf-8")
- 对比 os.system(cmd):只负责把命令丢给终端执行、返回退出码,**拿不到命令输出**;要结果就用 subprocess
- 安全提醒:shell=True 拼接用户输入有命令注入风险,外部输入别直接拼进命令

```python
import subprocess
res = subprocess.run("dir", shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(res.returncode)             # 0 表示执行成功
print(res.stdout.decode("gbk"))   # 打印 dir 的输出(Windows)
```

*执行系统命令并拿结果*

### 12. 打印进度条(\r 与 flush)

**进度条核心是**\r 回到行首覆盖打印** + **flush=True 强制立刻输出**:`print(..., end="", flush=True)` 在同一行不断重写百分比。**

- \r 是回车符:光标回到本行开头,下一次打印从行首覆盖旧内容;\n 则换到下一行 —— 进度条靠 \r 实现"原地刷新"
- print 默认 end="\n" 且有缓冲,必须改成 end="" 不换行,并加 flush=True 立刻刷出,否则终端迟迟看不到更新
- 百分比 = 已完成 / 总数 × 100;再换算成字符块更直观:bar = "#" * int(pct / 5),拼出 [#####     ] 50% 的样子
- time.sleep(0.1) 只是模拟耗时;真实场景(下载、批量处理)把 sleep 换成实际任务,每完成一批刷一次

```python
import time
total = 30
for i in range(total + 1):
    pct = i / total * 100
    bar = "#" * int(pct / 5)
    print(f"\r[{bar:<10}] {pct:.0f}%", end="", flush=True)
    time.sleep(0.1)
```

*命令行进度条*

### 13. shutil 文件与目录的高级操作

**shutil 在 os 之上封装**目录级高级操作**:copytree 复制整个目录、rmtree 强删非空目录、move 移动/改名,make_archive 还能一行打包 zip。**

- 复制三兄弟:copyfile(src, dst) 只拷内容;copy 再拷权限;copy2 连修改时间等元数据一起拷 —— 备份场景用 copy2
- shutil.copytree("src", "dst") 递归复制整个文件夹树;os 模块只能一个文件一个文件处理,目录级操作就靠 shutil
- shutil.rmtree("dir") 递归删除整个非空目录;对比:os.remove 只能删文件、os.rmdir 只能删空目录
- shutil.move(src, dst) 移动文件或文件夹,目标名不同时就是重命名,等价于剪切+粘贴
- shutil.make_archive("base_name", "zip", root_dir="要打包的目录") 一行压缩打包;解压用 zipfile/tarfile 模块

```python
import shutil
shutil.copytree("data", "data_backup")    # 整个目录连内容复制
shutil.move("data_backup", "bak")         # 改名/移动
shutil.rmtree("bak")                      # 连目录带内容删除
shutil.make_archive("log2020", "zip", root_dir="log")   # 打包 zip
```

*目录级复制/移动/删除*

### 14. 函数的类型提示(type hints)

**参数和返回值可用**类型注解**说明意图:`def add(x: int, y: int) -> int:`;它不是强制校验,而是给 IDE、静态检查工具和人看的"说明书"。**

- 写法:参数后冒号加类型,返回值用 -> 类型;带默认值照常写:def f(age: int = 18) -> str
- 注解**不参与运行校验**:add("a", "b") 照样执行返回 ab,类型写错解释器不拦 —— 想静态检查要配 mypy 等工具
- 容器类型:from typing import List, Dict 后写 List[int]、Dict[str, int];Python 3.9+ 也可以直接写 list[int]、dict[str, int]
- 好处:IDE 补全和告警更准、mypy 能提前抓类型 bug、代码即文档,团队协作时函数签名一眼看懂
- 变量也能注解:name: str = "alex";函数的注解存在 __annotations__ 字典里可以查看

```python
def add(x: int, y: int) -> int:
    return x + y

print(add(1, 2))            # 3
# print(add("a", "b"))      # 不报错,返回 ab:注解不强制

from typing import List

def total(nums: List[int]) -> int:
    return sum(nums)

print(total([1, 2, 3]))     # 6
```

*类型注解示例*

### 15. logging 进阶(格式、落盘、日志字典与轮转)

**logging 可用 **format 定制格式**、**filename 让日志落盘**;配置多时收成**日志字典**交给 dictConfig 一次生效;大日志用 **RotatingFileHandler 按大小轮转**防止写满磁盘。**

- 常用格式字段:%(asctime)s 时间、%(levelname)s 级别、%(name)s 日志器名、%(message)s 内容、%(lineno)d 行号、%(filename)s 文件名
- basicConfig(filename="app.log", encoding="utf-8") 写文件;不传 filename 输出到控制台 —— level/format/filename/encoding 各管一件事
- 日志字典:把 version、formatters、handlers、loggers 写成一个 dict,logging.config.dictConfig(cfg) 一次性生效;配置可以挪到 conf 目录当设置文件
- 日志轮转:RotatingFileHandler("app.log", maxBytes=10*1024*1024, backupCount=5) 单文件超 10MB 就切新文件,最多留 5 个历史文件
- 日志命名:logging.getLogger("业务名") 按名字拿 logger,模块里常用 __name__ 命名;名字不同互不干扰,日志一眼看出来源

```python
import logging

fmt = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=fmt,
    filename="app.log",     # 写入文件而不是控制台
    encoding="utf-8",
)
logging.info("服务启动")
logging.warning("磁盘空间不足")

# 配置项多时:cfg = {...}; logging.config.dictConfig(cfg)
# 大日志:from logging.handlers import RotatingFileHandler
```

*日志格式与落盘*

### 16. 密码加盐(salt)

**裸 md5("123456") 能被彩虹表反查;把一段**随机字符串(盐)拼进密码**再做摘要,相同明文也得到不同摘要,反查难度大幅提升。**

- 加盐摘要:m.update((盐 + 密码).encode("utf-8"));校验时用**同一个盐**再算一遍,比对两次的 hexdigest
- 盐的最佳实践:**每个用户一个随机盐**(os.urandom(16).hex() 或 uuid4().hex),随摘要一起存库;固定全局盐也能对抗通用彩虹表
- 安全性来自「不可逆 + 盐随机」:攻击者拿到库,也要对每个用户的盐单独建表,成本大幅上升
- 工程上更推荐 bcrypt/argon2 等专用算法(自动加盐、故意算得慢);md5+盐是理解原理的入门实现
- 项目实战(Day25 注册登录)就是把「明文 → 拼盐 → md5 → 存摘要」封装成 lib/common.py 的公共加密函数,登录认证装饰器复用它

```python
import hashlib, os

def make_digest(password, salt):
    m = hashlib.md5()
    m.update((salt + password).encode("utf-8"))
    return m.hexdigest()

salt = os.urandom(16).hex()          # 每个用户一份随机盐
d1 = make_digest("123456", salt)
print(d1 == make_digest("123456", salt))          # True 同盐同密码
print(make_digest("123456", "另一份盐") == d1)    # False 盐变摘要变
```

*加盐摘要*

---
