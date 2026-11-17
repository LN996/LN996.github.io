---
title: 流程控制与文件操作
date: 2026-11-02 09:00:00
tags:
  - Python
  - 基础
categories:
  - Python基础
---

> 我的学习笔记,边学边记,持续修订。最后更新:2026-11。

## 📖 流程控制(if / while / for)


### 1. if 分支结构

**Python 用**缩进**(推荐4空格)表示代码块,`if / elif / else` 从上到下命中一个分支后其余不再执行。**

- 条件为真的值:非0数字、非空字符串/列表/字典;`None` 为假
- 多条件用 and / or 连接;判断区间可连写 `90 > score >= 80`
- elif 可以有多个,else 最多一个且可不写
- 三元表达式:`值1 if 条件 else 值2`

```python
score = 85
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C")
level = "及格" if score >= 60 else "不及格"
```

### 2. while 循环与 break / continue

**while 适合“不知道循环次数”的场景;`break` **跳出整个循环**,`continue` **跳过本次**进入下一次。**

- while True + break 是最常见的“菜单循环”写法
- while 后面可以直接接 else:循环**没有被 break 打断**时执行
- 注意循环变量要自己更新,否则就是死循环

```python
i = 0
while i < 5:
    i += 1
    if i == 3:
        continue   # 跳过 3
    print(i, end=" ")  # 1 2 4 5
```

### 3. for 循环与 range

**for 用于遍历**可迭代对象**(字符串、列表、字典、文件…);`range(起, 止, 步长)` 同样**含头不含尾**。**

- `range(5)` → 0 1 2 3 4;`range(1, 10, 3)` → 1 4 7
- 遍历字典默认取键:`for k in d`;取键值对用 `d.items()`
- 嵌套循环:外层走一步,内层走完一圈
- for 也能接 else(没被 break 打断时执行)

```python
count = 0
for i in range(3):
    for j in range(i, 3):
        count += 1
print(count)   # 3+2+1 = 6
```

### 4. 推导式(列表/字典/集合)

**推导式是“循环+判断+生成”一行的简写,格式:**[表达式 for x in 可迭代 if 条件]**。**

- 列表推导式:`[x*x for x in range(1, 6) if x % 2 == 1]` → [1, 9, 25]
- 字典推导式:`{k: v for k, v in pairs}`
- 推导式比 for 循环快,但复杂逻辑不要硬塞,可读性优先
- 生成器表达式把 [] 换成 ():不占内存,只能遍历一次

```python
lst = [x * x for x in range(1, 6) if x % 2 == 1]
print(lst)   # [1, 9, 25]
d = {k: k * 2 for k in "abc"}
print(d)     # {'a': 'aa', 'b': 'bb', 'c': 'cc'} 字符串*2是重复
```

### 5. while-else 与 for-else

**循环可以接 **else**:只有循环**正常跑完、没有被 break 打断**才执行 else;continue 不影响 else,循环体一次没跑也会执行 else。**

- 语法:while 条件: ... else: ...;for x in it: ... else: ...;else 与循环体同级对齐
- 触发规则:循环**正常结束**(条件不满足/迭代完毕)→ 执行 else;一旦 **break 跳出 → 跳过 else**
- continue 只是跳过本轮、循环继续,不会跳过 else;循环条件一开始就不满足(循环体一次没执行)同样会执行 else
- 典型用途:"查找类"需求 —— 找到就 break,循环跑完还没找到,在 else 里统一处理"不存在",不用额外设 found 标志变量
- 判断质数、校验用户名是否已注册,都是 for-else 的经典场景

```python
names = ["alex", "wusir"]
for n in names:
    if n == "xiaoming":
        print("找到了", n)
        break
else:
    print("名单里没有这个人")

i = 0
while i < 3:
    i += 1
    if i == 1:
        continue     # 不影响 else
else:
    print("while正常结束, i =", i)   # while正常结束, i = 3
```

*for-else 与 while-else*

### 6. 嵌套循环:break 只跳一层

**嵌套循环中 **break 只能跳出它所在的那一层**,外层照常继续;想一次退出多层,要么逐层判断标志位,要么封装成函数用 return。**

- break 和 continue 都只对**当前这层循环**生效:内层 break 后,外层这一轮剩余代码照走、外层继续下一轮
- 方案一标志位:内层满足条件时设 flag = True 再 break,外层每轮开头检查 flag 决定是否也 break
- 方案二封装函数:把整个嵌套循环放进函数,满足条件直接 return,一次跳出所有层,Python 中最干净
- while 嵌套要点:内层的循环变量(计数器)要在**外层每一轮开始时重置**,否则内层只会跑一遍
- 经典结构:外层控制"共几轮",内层控制"每轮做几次" —— 打印三角形、九九乘法表都是这个套路

```python
flag = False
for i in range(3):
    for j in range(3):
        if i == 1 and j == 1:
            flag = True
            break           # 只跳出内层
    if flag:
        break               # 外层再看标志位
print(i, j)                 # 1 1
```

*标志位跳出多层循环*

### 7. 短路运算(and / or 的返回值)

****and 遇到假就停、or 遇到真就停**,表达式直接返回那个"决定结果"的操作数 —— 结果不一定是 True/False,常用来写默认值。**

- a and b:a 为假直接返回 a(结果已定),a 为真则返回 b;"第一个为真才看第二个"
- a or b:a 为真直接返回 a,a 为假返回 b;最常用:x = user_input or "默认值",输入为空串时自动用默认
- 优先级 not > and > or;混合时先算 and 再算 or:3 and 5 or 0 → 5
- 短路意味着后面的表达式**可能根本不执行**:0 and 1/0 不报错,因为 1/0 没跑;别把必须执行的副作用代码(打印、修改)放在 and/or 后面
- 布尔判断:0、0.0、""、[]、{}、None 都为假;if lst: 等价于 if len(lst) > 0:

```python
print(0 or "默认值")       # 默认值
print("a" and "b")          # b(and 返回最后一个)
print(0 and 1 / 0)          # 0:短路,1/0 没执行,不报错
print(3 and 5 or 0)         # 5
```

*短路运算示例*

### 8. 三元表达式(条件表达式)

****值1 if 条件 else 值2**:条件为真取值1、为假取值2,把"二选一"压缩成一行表达式;有返回值,可以嵌进赋值、f-string、列表生成式,复杂逻辑不要硬塞。**

- 语法:max_ab = a if a > b else b —— 先判断条件,True 取 if 前面的值,False 取 else 后面的值
- 它是**表达式**而不是语句:有返回值,能写在赋值右侧、f-string 里、列表生成式的元素位置;普通 if/else 语句则不能嵌在这些位置
- 两个以上分支可以嵌套:`a if x > 0 else (b if x == 0 else c)`,超过一层可读性骤降,老老实实写 if/elif
- 和列表生成式的两种 if:`[取值 if 条件 else 另值 for x in it]` 是**逐个取值**;`[x for x in it if 条件]` 是**过滤**,过滤版 if 后面没有 else
- 常见错误:漏写 else(语法直接报错,三元必须三段齐全);把冒号写成中文;条件里再套赋值(表达式里不允许 =)

```python
a, b = 10, 20
print(a if a > b else b)                    # 20
score = 85
print("及格" if score >= 60 else "不及格")   # 及格
scores = [58, 76, 90]
print(["及格" if s >= 60 else "不及格" for s in scores])
# ['不及格', '及格', '及格']
```

*三元表达式与生成式结合*

## 📖 文件操作


### 1. 打开文件与三种基础模式

**`open(路径, 模式, encoding=编码)`,核心模式:**r 读 / w 写(清空) / a 追加**,默认都是文本模式。**

- r:只读,文件**不存在直接报错** FileNotFoundError
- w:只写,文件不存在则创建,**存在则清空重写**
- a:追加,不存在则创建,存在则在**末尾续写**
- 加 `+` 变读写模式:r+ 从**文件头**开始覆盖写、写多少覆盖多少
- 加 `b` 变字节模式(rb/wb):处理图片、视频等二进制文件,不能指定 encoding
- 文本模式一定要写 `encoding="utf-8"`,Windows 默认 gbk 会乱码

```python
f = open("a.txt", "w", encoding="utf-8")
f.write("hello")
f.write("world")   # 接着写,不换行
f.close()          # 必须关闭才落盘
```

### 2. 读取文件的三种方式

**`read()` 全部读成字符串、`readline()` 一次一行、`readlines()` 全部读成**行列表**;大文件用 for 逐行迭代。**

- read():文件多大内存吃多少,大文件慎用
- readlines():返回列表,每个元素是一行(带换行符 \n)
- 推荐:`for line in f` 每次只加载一行,内存友好
- 读取后指针在文件末尾,再 read 得到空字符串

```python
with open("a.txt", encoding="utf-8") as f:
    for line in f:
        print(line.rstrip("\n"))   # 逐行处理,去掉换行符
```

### 3. with 上下文管理器

**`with open(...) as f:` 结束时**自动调用 close**,即使中途报错也会关闭,是最推荐的写法。**

- with 内部实现了 __enter__ / __exit__,属于上下文管理协议
- 可以同时打开多个:`with open(a) as f1, open(b) as f2:`
- 文件指针:read 之后想重新读,要 `f.seek(0)` 把指针拨回开头;`f.tell()` 查看当前位置

```python
with open("src.txt", encoding="utf-8") as f1, \
     open("dst.txt", "w", encoding="utf-8") as f2:
    f2.write(f1.read())   # 一行完成文件复制
```

### 4. 字符编码发展史(ASCII → GBK → Unicode → UTF-8)

**编码的进化:**ASCII(英文)→ 各国自定(GBK 等)→ Unicode(全球统一编号)→ UTF-8(Unicode 的变长实现)**;理解这条线就看懂了乱码。**

- 计算机只认二进制,字符必须按"对照表"翻译成数字再存储:这张对照表就是**字符编码**
- ASCII:美国制定,1 字节 8 位,收录英文、数字、符号共 127 个,英文世界够用
- 各国自己扩展:中国 GBK 用 2 字节表示一个汉字(向下兼容 ASCII);日本、韩国各搞一套,互不兼容 —— **A 编码存的文件用 B 编码打开必然乱码**
- Unicode(万国码):把全球所有字符统一编号,任何语言都用同一张表;但它是"编号标准",定长存储对英文太浪费(一个字母也要占多字节)
- UTF-8:Unicode 的**变长编码实现**:英文 1 字节、汉字 3 字节,向下兼容 ASCII,成为互联网事实标准;平时说的"Unicode 编码"实际多指 UTF-8
- 乱码两大类:① 存取编码不一致 → 用正确编码重新解码可救回 ② 存的时候字符就不在表里(如用 gbk 存 emoji)→ 换 utf-8 才能救

### 5. 文件修改的两种方式

**硬盘数据无法原地修改,**改文件 = 读入内存改好再写回**:方式一整读整写(占内存),方式二逐行写临时文件再改名顶替(省内存、推荐)。**

- 原理:文本编辑器"改文件"也是把文件读进内存、改完后保存写回硬盘;程序修改文件同理,不是在硬盘上直接改
- 方式一:read() 一次性读入内存 → 字符串 replace 修改 → 以 w 模式重新写回;简单粗暴,文件大就爆内存
- 方式二:以 r 模式逐行读原文件,边改边写入**临时文件**;全部处理完后 os.remove 删原文件、os.rename 把临时文件改名顶替 —— 内存始终只有一行
- 两个注意:rename 前要先 remove(Windows 下目标名已存在会报错);读写都显式指定 encoding="utf-8"
- 记忆:小文件用方式一图省事,**大文件(日志、账单)必须用方式二**

```python
import os
with open("a.txt", "r", encoding="utf-8") as f_read, \
     open("a.txt.bak", "w", encoding="utf-8") as f_write:
    for line in f_read:
        f_write.write(line.replace("alex", "ALEX"))

os.remove("a.txt")               # 删原文件
os.rename("a.txt.bak", "a.txt")  # 临时文件顶替原名
```

*文件修改方式二(推荐)*

### 6. x 模式与 b 模式

****x:独占创建写,文件已存在直接报错**,防止误覆盖;**b:字节模式(rb/wb/ab)**读写图片视频等二进制,write 必须传 bytes 且不能指定 encoding。**

- x 模式:文件不存在 → 创建并写;文件已存在 → 抛 FileExistsError。和 w 的区别就在这:w 会静默清空原文件,x 会提醒你"已经有了"
- b 模式是"读写单位变成字节",要和 r/w/a 组合成 rb、wb、ab、r+b 使用
- b 模式**不能传 encoding 参数**;read() 得到 bytes、write() 必须传 bytes,文本要先 .encode("utf-8")
- 典型应用:复制图片/视频/音频(rb 读 + wb 写);网络(socket)传来的数据天生是 bytes
- b 模式下指针 seek 按**字节**移动,可以精确定位;二进制处理、断点续传等场景都靠它

```python
with open("logo.png", "rb") as f1, open("copy.png", "wb") as f2:
    f2.write(f1.read())               # 二进制文件复制

with open("b.txt", "wb") as f:
    f.write("中文".encode("utf-8"))   # 文本必须先编码成 bytes
# f.write("中文")                     # ❌ TypeError
```

*b 模式读写二进制*

### 7. 文件指针详解(seek / tell / truncate)

**文件有一个**指针**标记当前读写位置:r/w 打开在开头、**a 固定在末尾**;tell() 查位置、seek() 移动,且 whence=1/2 只能在 b 模式下用。**

- 指针规则:r 模式打开指针在文件开头;w 打开(先清空)指针在开头;**a 模式指针在末尾且写入永远发生在末尾**,seek 挪不动写入位置
- tell():返回当前指针位置;read(n)/readline() 读完指针停在已读内容之后,再 read() 就是空 —— 想重读要 f.seek(0)
- seek(offset, whence):whence=0 从文件开头(默认)、1 从当前位置、2 从文件末尾;**1 和 2 只能在 b 模式下使用**,文本模式只支持 seek(0) 或 tell() 返回的位置
- 文本模式按**字符**移动、b 模式按**字节**移动:处理二进制或需要精确定位(比如只读文件最后 200 字节)时用 rb
- f.truncate(n):把文件截断,只保留开头 n 个字节(常在 b 模式下用);不传参数则截断到当前位置

```python
with open("a.txt", "rb") as f:
    print(f.tell())      # 0
    f.read(3)            # 读 3 个字节
    print(f.tell())      # 3
    f.seek(0)            # 拨回开头,可以重读
    f.seek(-2, 2)        # 从末尾倒数 2 字节(仅 b 模式)
```

*指针操作*

### 8. 文件对象的其他方法(flush/closed/readable 等)

**除了读写,文件对象还有一组"状态与控制"方法:**flush 强制刷缓冲落盘、closed 判断是否关闭、readable/writable 判断权限、name/encoding 查看打开属性**。**

- flush():write 的数据先躺在**内存缓冲区**,攒够或 close 才真正写硬盘;flush() 强制立刻落盘 —— 常驻程序写日志时"写一条 flush 一条",避免断电丢日志
- closed:布尔属性,文件是否已关闭;with 代码块结束后自动变 True,手动 open 的文件 close 后变 True
- readable()/writable():当前模式有没有读/写权限,如 r 模式 readable() 为 True、writable() 为 False,对 r 打开的文件 write 会报错
- name / mode / encoding:文件路径、打开模式、打开时用的编码;排查乱码第一件事就是 print(f.encoding),确认读写用的是不是同一张表
- readline():一次读一行(带 \n),读到末尾返回空字符串,配合 while 也能逐行处理,但更推荐直接 for line in f

```python
f = open("a.txt", "w", encoding="utf-8")
print(f.writable(), f.readable())   # True False
f.write("hello")
f.flush()          # 立刻落盘,不等缓冲
print(f.closed)    # False:还没关闭
f.close()
print(f.closed)    # True
```

*文件对象状态方法*

---
