---
title: 并发编程逐集精讲
date: 2026-11-06 09:00:00
tags:
  - Python
  - 并发编程
categories:
  - Python学习笔记
---
> 本文是「Python全栈学习中心」系列笔记之一,配套可刷题的本地工具(获取方式见文末)。

---

## 📖 并发编程

> 🎬 对应课程:Python基础 第9章(多进程、多线程、GIL、锁、线程池、协程)

### 1. 进程与线程基本概念
> 🎬 对应视频:P458、P470

****进程是资源分配的最小单位,线程是 CPU 调度的最小单位**;进程间数据隔离,线程间共享进程的内存。**

- 进程:正在运行的程序,是操作系统**分配资源**(内存、文件句柄)的基本单位,进程之间相互独立
- 线程:进程内部的执行单元,**共享**所在进程的全局变量和内存,创建、切换开销比进程小
- 一个进程至少有一个**主线程**;某线程崩溃可能拖垮整个进程,而一个进程崩溃不影响其他进程
- 并行:多个 CPU 核心真正同时执行;并发:单核(或同一核)时间片轮转,**看起来**同时执行
- Python 实践:计算密集用多进程,IO 密集用多线程或协程

### 2. multiprocessing 多进程
> 🎬 对应视频:P458~P460、P463、P468

**`Process(target=函数, args=(参数,))` 创建子进程,`start()` 启动、`join()` 等待;**进程间数据默认隔离**,通信要用 `Queue`。**

- 创建后必须调 `p.start()` 才真正开出子进程;`p.join()` 让**父进程等待**子进程结束后再继续
- `p.daemon = True` 设为守护进程(必须在 start **之前**):父进程结束,守护子进程立即终止,且设置了 daemon 就不能再 join
- 数据隔离:子进程是父进程数据的一份**拷贝**,子进程里改全局变量,父进程完全看不到
- 进程间通信用 `multiprocessing.Queue`(put / get),数据经过 pickle **复制传递**,而不是共享内存
- Windows 下创建进程用 spawn 方式(重新 import 主模块),主逻辑必须放在 `if __name__ == "__main__":` 里,否则递归创建报错

```python
from multiprocessing import Process

def work(name):
    print(name, "子进程执行中")

if __name__ == "__main__":   # Windows 下必须加这行
    p = Process(target=work, args=("p1",))
    p.start()     # 启动子进程
    p.join()      # 父进程等待子进程结束
    print("父进程结束")
```

*多进程基本用法*

### 3. threading 多线程与数据竞争
> 🎬 对应视频:P473、P475~P479

**`Thread(target=函数)` 创建线程,线程**共享进程数据**,多个线程同时改同一变量会产生**竞争**,必须加锁。**

- `t = Thread(target=work, args=(n,))`;`t.start()` 启动,`t.join()` 等待该线程结束
- `t.setDaemon(True)` 设为守护线程(须在 start **之前**):主线程结束,守护线程立即死亡,适合日志、心跳等辅助任务
- 线程共享全局变量,但 `x += 1` 这类操作**不是原子的**(读、加、写三步可能被打断),多线程并发修改结果会出错
- 不加锁时两个线程各加 100 万次,最终结果往往**小于** 200 万,且每次运行可能不同
- 主线程要等所有**非守护**线程结束才会退出

```python
import threading

x = 0
lock = threading.Lock()

def work():
    global x
    for _ in range(1000000):
        lock.acquire()
        x += 1
        lock.release()

t1 = threading.Thread(target=work)
t2 = threading.Thread(target=work)
t1.start(); t2.start()
t1.join(); t2.join()
print(x)   # 加锁后一定是 2000000,不加锁则可能小于它
```

*线程竞争与同步锁*

### 4. GIL 全局解释器锁
> 🎬 对应视频:P480~P482

**GIL 保证**同一进程同一时刻只有一个线程执行 Python 字节码**;因此 IO 密集用多线程、计算密集用多进程。**

- GIL 是 **CPython 解释器**的实现细节,不是 Python 语言规范;JPython 等其他解释器没有 GIL
- 线程执行 IO 操作时会**释放 GIL**,其他线程可以趁机运行——所以爬虫、文件读写、socket 等 IO 密集任务用多线程依然有效
- 计算密集任务(纯数学运算)吃 CPU,GIL 让多线程无法并行计算,应改用 `multiprocessing` 多进程,每个进程有**自己独立的 GIL**,可利用多核
- GIL 不等于业务安全:它只保证同一时刻只有一个线程执行字节码,但一条语句中间仍可能被切换,共享数据**仍需自己加锁**
- 一句话选型:IO 多 → 多线程 / 协程;计算多 → 多进程

### 5. 锁、信号量、事件与安全队列
> 🎬 对应视频:P466~P469、P485~P489

**`Lock` 保证临界区互斥,`Semaphore` 限流,`Event` 发通知,`Queue` 自带锁、天生线程安全,是**生产者消费者模型**的首选。**

- Lock:`acquire()` 抢锁、`release()` 放锁,同一时刻只放一个线程进临界区;抢不到就阻塞
- **死锁**:两个线程各自持有一把锁、又都在等对方手里的锁,谁都不放,程序卡死;RLock(可重入锁)允许同一线程多次 acquire,可缓解嵌套场景
- Semaphore(n):**最多允许 n 个线程**同时访问,比如限制同时只有 3 个线程连数据库
- Event:`wait()` 等待信号、`set()` 发出信号,用于线程间的**通知**机制
- Queue 内部已加锁,多线程 put / get 不会乱:`q.put()`、`q.get()`、`q.qsize()`、`q.task_done()`、`q.join()`
- 生产者消费者模型:生产者只管往队列放任务,消费者只管取任务处理,用 Queue 解耦、削峰

```python
from queue import Queue

q = Queue()

def producer():
    for i in range(3):
        q.put(f"任务{i}")          # 生产者:放任务

def consumer():
    while True:
        item = q.get()             # 消费者:取任务(线程安全)
        print("处理", item)
        q.task_done()
```

*生产者消费者模型(Queue)*

### 6. 进程池线程池与协程
> 🎬 对应视频:P490~P494

**池用 `concurrent.futures` 的 `ThreadPoolExecutor / ProcessPoolExecutor`(`submit / map / result`);协程是**单线程内的并发**,gevent 遇 IO 就切换任务。**

- 用池的意义:复用线程/进程,省去频繁创建销毁的开销,还能**限制最大并发数**
- `executor.submit(fn, 参数)` 返回 Future 对象,`fut.result()` 拿结果(没完成会阻塞);`executor.map(fn, 列表)` 按提交顺序返回全部结果
- 协程:单线程内遇到 IO **主动切换**去执行别的任务,让 CPU 不闲着,切换开销最小,本质是程序自己调度的假并发
- gevent 三件套:`from gevent import monkey; monkey.patch_all()`(把 socket、time 等改成协作式,要放最前面)、`gevent.spawn(函数)` 创建、`gevent.joinall()` 等待全部完成
- asyncio 是 py3.4+ 原生方案:`async def` 定义协程、`await` 处处让出执行权
- 生成器的 `yield` 能让出执行权又记得恢复位置,正是协程切换的思想来源

```python
from concurrent.futures import ThreadPoolExecutor

def down(url):
    return f"{url} 下载完成"

with ThreadPoolExecutor(3) as ex:
    for res in ex.map(down, ["a.jpg", "b.jpg", "c.jpg"]):
        print(res)   # 按提交顺序输出,不会乱序
```

*线程池 map 批量任务*

### 7. 操作系统发展史与多道技术
> 🎬 对应视频:P453~P454

**操作系统为解决 **CPU 在等 IO 时空转**的问题发展出**多道技术**:内存同时驻留多道程序,**空间复用**分内存、**时间复用**切 CPU。**

- 发展脉络:手工操作(穿孔卡片,人机矛盾大)→ 单道批处理(内存里只有一道程序)→ 多道批处理 → 分时系统(时间片轮转、人机交互)→ 实时系统(要求及时响应)
- 核心矛盾:CPU 速度远快于 IO,单道程序等 IO 时 CPU 只能干等,利用率极低;于是让多道程序'互相填坑'
- **空间上的复用**:内存划分给多道程序同时驻留,靠硬件支持内存隔离,各进程互不越界
- **时间上的复用**:CPU 在多道程序间切换——某程序遇到 IO 或时间片用完就切出去,切走前保存上下文(寄存器、执行状态),轮回来再恢复现场
- 效果:宏观上多道程序'同时'运行,微观上 CPU 串行切换;进程、线程、并发这些概念都源于此

### 8. 进程三状态与调度算法
> 🎬 对应视频:P455~P456

**进程在**就绪、运行、阻塞**三态间流转:缺 CPU 是就绪、等 IO 是阻塞;调度算法里**多级反馈队列**综合表现最好。**

- 三状态:就绪(万事俱备,只差 CPU)、运行(正在被 CPU 执行)、阻塞(等 IO、等锁、等事件——CPU 让给它也没法干活)
- 流转规则:就绪→运行(被调度);运行→就绪(时间片用完/被抢占);运行→阻塞(等 IO);**阻塞只能等 IO 完成后回到就绪,不能直接回运行**
- 先来先服务 FCFS:简单公平,但长作业排在前面会把短作业拖死
- 短作业优先 SJF:平均等待时间最优,但长作业可能一直被插队、甚至'饿死'
- 时间片轮转 RR:轮流执行一个时间片,响应快、适合交互系统,但频繁切换有开销
- **多级反馈队列**:多个优先级队列,新任务进最高级(时间片短),用完时间片就降到下一级(时间片变长);IO 密集任务因频繁让出 CPU 留在高优先级被及时响应——兼顾长短作业,是最常用的综合方案

### 9. 僵尸进程、孤儿进程与守护进程
> 🎬 对应视频:P464~P465

****子先死、父不收尸 = 僵尸进程;父先死、子被 1 号进程收养 = 孤儿进程;daemon=True 的守护进程随主进程代码结束而立即终止**。**

- 僵尸进程:子进程先结束,父进程还活着却一直不回收(不调用 join/wait),子进程的 PID 和退出状态会**残留在进程表**里;大量堆积会占用系统 PID 资源
- 回收僵尸:父进程调用 join() 即可'收尸';或等父进程结束后,僵尸被 init/systemd(1 号进程)收养并回收
- 孤儿进程:父进程先结束、子进程还在运行,**被 1 号进程收养**,之后由它负责回收——无害,后台服务常主动利用这一点脱离终端
- 守护进程:`p.daemon = True`(必须在 start 之前设置),**主进程代码一结束,守护子进程立即被强制终止**;适合'主进程只负责监控、子进程是辅助'的场景
- 对比记忆:僵尸是'死了没人收尸'占着资源;孤儿是'父死有人接管'继续活;守护是'主死随死'的跟班

### 10. IO 模型:阻塞、非阻塞、多路复用与 asyncio
> 🎬 对应视频:P499~P505

****阻塞 IO 干等、非阻塞 IO 轮询、IO 多路复用一个线程看多个连接、异步 IO 内核全办好再通知**;asyncio 用事件循环在单线程内调度协程扛高并发 IO。**

- 阻塞 IO(默认):recv/accept 没数据就一直卡着,线程从运行态进入阻塞态,一个线程同一时刻只能伺候一个连接
- 非阻塞 IO:`conn.setblocking(False)`,没数据立刻返回错误,程序在 while 里**轮询**反复问;线程不被卡死但 CPU 空转,浪费严重
- IO 多路复用:用 `selectors`/`select` 模块把**多个连接交给内核监视**,哪个就绪就处理哪个,单线程也能管成百上千连接;socketserver 底层、Nginx、Redis 都是这套机制
- 同步/异步看**结果的通知方式**(主动等或主动问是同步,内核完成后通知你是异步),阻塞/非阻塞看**等待时能不能干别的**;按此标准,阻塞、非阻塞、多路复用都属于同步 IO,真正异步的只有异步 IO 模型
- asyncio:`async def` 定义协程,`await` 处遇到 IO 主动让出,事件循环(event loop)单线程调度所有协程;`asyncio.run(main())` 启动,`asyncio.gather()` 并发跑多个协程并**按传入顺序**收集结果
- 选型:连接很多、每个连接大部分时间在等数据的高并发服务,用多路复用/协程;实际项目中 aiohttp、FastAPI 等都构建在 asyncio 之上

```python
import asyncio

async def fetch(name, sec):
    await asyncio.sleep(sec)     # 遇 IO 让出控制权,事件循环去跑别的协程
    return f"{name} 完成"

async def main():
    # gather 并发执行多个协程,结果按传入顺序收集
    res = await asyncio.gather(fetch("A", 2), fetch("B", 1))
    print(res)

asyncio.run(main())   # 总耗时约 2 秒,而不是 3 秒
```

*asyncio 事件循环并发执行两个协程*

### 11. 同步/异步与阻塞/非阻塞
> 🎬 对应视频:P457

****同步/异步看「结果如何通知你」**(主动等/主动问 vs 内核完成后回调),**阻塞/非阻塞看「等待时能不能干别的」**——两组概念正交,组合出四种调用姿态。**

- 同步:发起调用后需要**主动等待或主动轮询**结果,结果不会自己送上门;异步:调用立即返回,**内核完成后主动通知/回调**你,期间线程可以干别的
- 阻塞:结果没好之前,当前线程被挂起、CPU 让给别人,什么都做不了;非阻塞:调用**立刻返回**,没好就返回错误/空值,线程继续往下跑
- 四种组合:同步阻塞(recv 卡死等,最常见)、同步非阻塞(setblocking(False) 后 while 轮询)、异步非阻塞(理想形态,真正的异步 IO 才是);「异步阻塞」基本只在程序级等待(join、Event.wait)里口头一提
- 判断口诀:先问「有没有人通知我」分同步/异步,再问「等的时候线程是不是被挂死」分阻塞/非阻塞
- 定位:这是 Day38 的前置理论,Day42 讲 IO 模型时按这个标准给五种模型归类——**阻塞、非阻塞、多路复用都属于同步 IO**,因为数据拷贝阶段还得自己等/自己问

### 12. TCP 服务端实现并发效果
> 🎬 对应视频:P474

**单线程服务端 accept 一个客户端后就被通信循环缠住;把每个 conn 的通信循环交给**子线程(或子进程)**,主循环专职 accept,就能同时服务多个客户端。**

- 问题:手写 TCP 服务端是「链接循环套通信循环」,accept 到第一个客户端后就陷在通信循环里 recv/send,第二个客户端只能干等
- 改造:accept 拿到 conn 后,`t = Thread(target=talk, args=(conn,))` + `t.start()`,把通信循环交给线程;主线程**立刻回头继续 accept**
- talk 函数里就是原来的 while recv/send 逻辑,异常要 try 住:客户端强制断开会抛 ConnectionResetError,不处理会拖垮服务端
- 选型:每连接一线程(共享数据、切换快,IO 场景够用)vs 每连接一进程(稳定隔离,但开销大、Windows 启动慢)
- 隐患:连接数不受控,线程一多内存和调度开销爆炸;受控方案 = socketserver 模块(P447)和后面的线程池(P491)

### 13. 协程实现 TCP 并发
> 🎬 对应视频:P495

**`monkey.patch_all()` 打补丁后,accept 到连接就用 `gevent.spawn(talk, conn)` 派一个协程,单线程遇 IO 自动切换,轻量实现 TCP 并发。**

- 写法顺序:`from gevent import monkey; monkey.patch_all()` 必须在 import socket 之前执行,把 recv/send 等 IO 改造成协作式
- 服务端照常 socket → bind → listen → accept;链接循环里 `gevent.spawn(talk, conn)` 把通信循环交给协程,主循环马上回去 accept 下一个
- 原理:某连接的 recv 没数据时,补丁后的代码**自动切给其他连接的协程**;单线程就能「同时」和多个客户端收发
- 对比:每连接一线程,几百连接就是几百线程,内存和切换开销大;每连接一协程,单线程扛上千连接,协程栈开销只有 KB 级
- 软肋:协程靠「遇 IO 让出」驱动,某个协程里有**纯计算死循环**,整个线程被它占死,所有连接都卡住——所以协程只适合 IO 密集

### 14. 开启进程/线程的两种方式
> 🎬 对应视频:P458、P473

**除了 `Process/Thread(target=函数)`,还可以**自定义类继承 Process/Thread**、重写 run 方法,start() 之后自动执行 run——两种方式本质相同。**

- 方式一(函数式):`p = Process(target=work, args=(x,))`,把要执行的函数交给 target、参数交给 args,最常用
- 方式二(继承式):`class MyProcess(Process):` 重写 `run(self)`,参数通过自定义 `__init__(self, x)` 传进来;`p = MyProcess(x)` 后 `p.start()` **自动调用 run**
- Thread 完全同理:`class MyThread(Thread): def run(self)`,继承式适合逻辑复杂、要携带大量状态的场景,把数据和行为封装在一个类里
- 本质相同:Process/Thread 内部定义了 run,target=函数 时 run 的默认实现就是执行这个函数——继承式只是覆盖了 run
- 无论哪种方式,Windows(spawn 启动)下创建进程的代码都必须放在 `if __name__ == "__main__":` 里,否则子进程 import 主模块时递归创建进程报错

## 📖 并发逐集精讲(Day38~39)

> 🎬 对应课程:Day38~39 逐集精讲(操作系统/多道技术/进程/线程理论)

### 1. 章节说明:按集精讲与「并发编程」章节的关系
> 🎬 对应视频:P449~P470

**本章节把 Day38~39 的 **16 个内容小节逐集拆分**,一集一个知识点(title 以集数开头、video 标注单集 P 号),方便**按集查找**;系统性学习并发仍以「并发编程」章节为主,本章节是它的逐集精讲版。**

- 组织方式:Day38-05 ~ Day39-10 共 16 个内容小节,每集对应一个知识点,如「Day38-06 多道技术」对应 P454;听课时按集数或 P 号即可快速定位到对应讲义
- 与「并发编程」章节的关系:「并发编程」章(py-concurrent)按**主题**系统讲解(进程/线程/GIL/锁/池/协程),本章节按**视频集数**逐集精讲——先看前者建立知识体系,再按集复习对照
- Day38 脉络:操作系统发展史 → 多道技术 → 进程调度 → 三状态图 → 同步异步 → 创建进程 → join → 数据隔离;Day39 脉络:进程对象 → 僵尸/孤儿 → 守护进程 → 互斥锁 → 队列 → IPC → 生产者消费者 → 线程理论
- 行政小节(课程安排、自我介绍、今日内容概要、知识回顾,即 P449~P452、P461~P462)不设知识点,只收录 16 个知识小节
- 代码片段均在 Windows(Python 3)下实际运行验证;**Windows 开子进程必须写在 if __name__ == "__main__": 里**,这个坑已在对应知识点反复标注

### 2. Day38-05 操作系统发展史
> 🎬 对应视频:P453

**操作系统从**手工操作(穿孔卡片)→ 批处理系统 → 多道程序系统 → 分时系统**一路演化,核心矛盾始终是「昂贵的 CPU 别闲着」;理解这段历史,才能理解并发技术为什么长成今天这样。**

- 手工阶段(穿孔卡片):程序打在纸卡片上排队上机,**一人独占整台计算机**;机器等人装卡片、CPU 大量空转,利用率极低
- 批处理系统:把一批作业提前攒到磁带上,由**监督程序**自动一个接一个执行,省去人工装卸;联机批处理 CPU 仍要亲自管输入输出,脱机批处理用外围机先把数据倒上磁带,CPU 专心计算
- 多道程序系统:内存里同时放多道程序,CPU 在它们之间切换,一道程序等 IO 时立刻去跑另一道——**CPU 利用率大幅提升**,是现代操作系统和并发编程的基石(下一集展开)
- 分时系统:把 CPU 时间切成小片轮流服务多个终端,每个用户都感觉自己在独占计算机;著名的 **UNIX** 就诞生于分时系统 Multics 项目之后
- 现代操作系统(Windows/Linux/Mac)是多道 + 分时的集大成者;后面的进程、线程、锁、队列,全是操作系统为了「高效且安全地并发」提供的机制

### 3. Day38-06 多道技术
> 🎬 对应视频:P454

**多道技术 = **空间上的复用 + 时间上的复用**:内存同时驻留多道程序(空间复用),CPU 在多道程序间快速切换(时间复用),让单核也能「宏观同时、微观轮流」地跑多个程序。**

- 要解决的问题:单道程序独占计算机时,遇到 IO(读盘、等输入)CPU 只能干等;多道技术在内存里**同时放多道程序**,一家等 IO 就切给另一家,把 CPU 喂饱
- 空间上的复用:把内存划分成多个区域,每个区域放一道程序,**各占各的内存、物理隔离**(后来进程隔离的雏形)
- 时间上的复用:CPU 在多道程序间来回切换,切换时机有两种——① 某程序**遇到 IO** 时切换(把等待时间利用起来,最划算);② 某程序**占用 CPU 时间过长**时切换(切换有开销,但不切别的程序会饿死)
- 并发 vs 并行:单核 CPU 靠切换实现**并发**(微观轮流执行,宏观像同时跑);**并行**才是真同时执行,只有多核 CPU 才做得到
- 切换前要保存当前程序的状态、切回时再恢复(上下文切换),所以并发不是免费的;操作系统就是这套复用机制的总管家

### 4. Day38-07 进程的调度
> 🎬 对应视频:P455

**多个进程抢一个 CPU,操作系统用**调度算法**决定下一个谁上:**先来先服务、短作业优先、时间片轮转、多级反馈队列**;多级反馈队列兼顾长短作业,综合表现最好。**

- 先来先服务(FCFS):按排队顺序执行,公平简单,但**对短作业不友好**——前面一个长作业能把后面一串短作业堵死
- 短作业优先(SJF):谁省时间谁先上,平均等待时间最短;但**对长作业不友好**,长作业可能不断被新来的短作业插队而「饿死」
- 时间片轮转(RR):每个程序轮流执行一个固定时间片(几十毫秒),到点强制切换;响应快、体验公平,是分时系统的基础
- 多级反馈队列:设多个不同优先级的队列,新任务进最高优先级队列;一个时间片内没跑完就**降到下一级**(低级队列时间片更长)——短作业被快速完成,长作业也总能分到时间,综合表现最好
- 现代操作系统的调度都是这些思想的综合改进;记住结论:**没有对所有人都公平的算法,只有权衡**

### 5. Day38-08 进程三状态图
> 🎬 对应视频:P456

**进程在**就绪 → 运行 → 阻塞**三个状态间流转:万事俱备只欠 CPU 是**就绪**,占着 CPU 在跑是**运行**,等 IO 等锁是**阻塞**;阻塞后必须先回就绪重新排队,不能直接跳回运行。**

- 就绪态(Ready):除 CPU 以外的资源都已到位,在就绪队列里排队等调度——缺的只是 CPU
- 运行态(Running):真正占有 CPU 执行代码;单核机器同一时刻最多只有一个进程处于运行态
- 阻塞态(Blocked):在等**非 CPU 资源**——磁盘读写、网络数据、锁等;这时候给它 CPU 也没用
- 流转规则:就绪 →(被调度)→ 运行 →(时间片用完)→ 就绪;运行 →(发起 IO)→ 阻塞 →(IO 完成)→ 就绪;**阻塞态不能直接进运行态**,IO 完成后也要回就绪排队
- 这张图是后面一切的基础:join 让主进程阻塞等子进程;同步异步、阻塞非阻塞讨论的正是「等待时进程处于什么状态、能不能干别的」

### 6. Day38-09 同步异步与阻塞非阻塞
> 🎬 对应视频:P457

****同步/异步关注「结果如何拿到」**(自己盯着等 vs 对方做完通知你),**阻塞/非阻塞关注「等的时候能不能干别的」**(被挂起 vs 立刻返回)——两组概念相互独立,组合出四种调用姿态。**

- 同步:调用发出后,调用方要**主动等待或主动查询**结果才算完成(排队买奶茶,自己站在柜台前盯着做)
- 异步:调用发出后调用方就走,**结果由被调用方做完后主动通知**(扫码下单做好叫号,该干嘛干嘛;常用回调函数实现)
- 阻塞:结果没回来之前,当前进程/线程被**挂起**,CPU 让给别人,自己什么都干不了(对应三状态图里的「阻塞态」)
- 非阻塞:结果没好也**立刻返回**,不挂起,调用方可以接着干别的(通常要配合反复轮询确认结果)
- 两组概念正交:同步不等于阻塞(同步 + 轮询 = 同步非阻塞),异步一般配合非阻塞使用;日常最常见的是「同步阻塞」,高并发服务追求「异步 + 非阻塞」

### 7. Day38-10 创建进程的两种方式
> 🎬 对应视频:P458

**multiprocessing 开子进程两种写法:① `Process(target=函数, args=(参数,))`;② 自定义类**继承 Process 重写 run**;Windows 下创建进程**必须**写在 `if __name__ == "__main__":` 里,否则无限递归报错。**

- 方式一(常用):`p = Process(target=task, args=("甲",))`,target 指定子进程要执行的函数,**args 必须是元组**(只传一个参数也要写逗号);`p.start()` 告诉操作系统开进程,主进程**不等它**、继续往下走
- 方式二:自定义类继承 Process,把逻辑写在 `run` 方法里(逻辑复杂、需要更多自定义属性时用);`p.start()` 后操作系统自动执行 run——注意**直接调 p.run() 不会开新进程**,那只是普通函数调用,start() 才是真正创建进程
- Windows 大坑(课程反复强调):Windows 创建子进程采用**导入父进程模块**的方式(spawn),子进程会重新执行模块顶层代码;不加 `if __name__ == "__main__":` 保护,一运行就无限递归创建进程直接报错;Linux/Mac(fork)不写也能跑,但代码要跨平台就必须写
- 保护生效的原理:子进程导入模块时 `__name__` 不是 "__main__",所以保护块里的创建代码在子进程里不会执行;两种方式本质相同,都要 start() → 操作系统分配资源 → 执行函数或 run
- start 之后父子进程**并发执行**,谁先打印由操作系统调度决定,不要依赖输出顺序

```python
from multiprocessing import Process
import os, time

def task(name):
    print(f"子进程{name}运行中,pid={os.getpid()},父进程pid={os.getppid()}")
    time.sleep(1)

class MyProcess(Process):          # 方式二:自定义类继承 Process
    def __init__(self, name):
        super().__init__(name=name)
    def run(self):                 # start() 之后自动执行 run()
        print(f"子进程{self.name}运行中,pid={os.getpid()}")

if __name__ == "__main__":         # Windows 下必须写,否则无限递归报错
    p1 = Process(target=task, args=("甲",))   # 方式一:指定函数
    p2 = MyProcess("乙")
    p1.start()
    p2.start()
    print("主进程继续往下执行,不等子进程")

```

*创建子进程的两种方式(Windows 必须加 __main__ 保护)*

### 8. Day38-11 join方法
> 🎬 对应视频:P459

**`p.join()` 让主进程**阻塞等待子进程真正结束**再往下执行;想保持子进程并发,要**先统一 start、再统一 join**——start 一个就立刻 join 一个,并发会退化成串行。**

- start() 只是「下单开进程」,主进程立刻继续往下;join() 则让主进程停在原地等子进程执行完毕(可传 timeout 只等指定秒数,配合 is_alive() 判断)
- 本质对应三状态图:join 时主进程进入**阻塞态**,子进程终止后才恢复运行——join 是拿「主进程的时间」换「确定的顺序」
- 经典错误:for 循环里 start 一个就 join 一个,子进程被迫一个接一个跑(**串行**),并发白开了
- 正确姿势:第一个循环把所有子进程 start 完(它们并发执行),第二个循环再统一 join(主进程等全部结束);主进程最后一句代码一定最后打印
- 不 join 行不行?行——子进程照样跑完,但主进程后续代码与子进程的先后顺序不确定;需要「等结果再继续」的场景必须 join

```python
from multiprocessing import Process
import time

def task(name):
    print(f"{name} 开始干活")
    time.sleep(2)
    print(f"{name} 干完了")

if __name__ == "__main__":
    ps = []
    for i in range(3):
        p = Process(target=task, args=(f"子进程{i}",))
        p.start()                  # 先把 3 个子进程全部开起来
        ps.append(p)
    for p in ps:
        p.join()                   # 再统一等待,主进程最后才往下走
    print("所有子进程结束,主进程才打印这句话")

```

*先统一 start,再统一 join*

### 9. Day38-12 进程间数据相互隔离
> 🎬 对应视频:P460

****进程是资源分配的最小单位**,各自拥有独立内存:子进程对全局变量的修改只改了自己那份拷贝,**父进程完全看不见**;想传数据必须用 IPC(队列/管道)。**

- 实验:父进程定义全局 x = 100,子进程里改成 200 并打印——子进程打印 200,父进程 join 后打印的仍是 100,两边互不影响
- 原因:创建子进程时,子进程拿到的是父进程数据的**一份拷贝**(Windows 下相当于把模块重新导入一遍),从此两套内存各过各的
- 对比线程:同一进程内的多个线程**共享**同一份内存,改全局变量彼此都看得见(Day39-10 细讲)——这就是「线程通信方便但有竞争、进程隔离安全但通信麻烦」的根源
- 所以「改全局变量传数据」在进程间行不通;进程通信只能借助操作系统提供的 IPC 机制(multiprocessing 的 Queue/Pipe,见 Day39-08),或文件、socket 等外部介质
- 隔离的好处是安全:一个进程崩溃不会污染其他进程的内存;代价是通信要「过一道系统」,成本比线程高

```python
from multiprocessing import Process

x = 100                              # 全局变量

def change():
    global x
    x = 200                          # 子进程改的只是自己那份拷贝
    print("子进程里 x =", x)

if __name__ == "__main__":
    p = Process(target=change)
    p.start()
    p.join()
    print("主进程里 x =", x)

```

*验证进程间数据隔离*

### 10. Day39-03 进程对象及其他方法
> 🎬 对应视频:P463

**进程对象常用成员:`p.pid` 进程号、`p.name` 进程名、`p.is_alive()` 是否存活、`p.terminate()` 杀进程、`p.join()` 等结束;子进程内用 `os.getpid()/os.getppid()`、`current_process()` 查看自己。**

- 父子互查:父进程用 `p.pid` 拿子进程号;子进程内 `os.getpid()` 看自己、`os.getppid()` 看父进程,两者能对得上;`multiprocessing.current_process()` 拿当前进程对象(主进程默认名 MainProcess)
- `p.name`:创建时用 Process(target=..., name="甲进程") 起名,方便日志调试;`p.is_alive()` 判断进程是否还在运行
- `p.terminate()`:给操作系统发**终止信号**——它是异步的,发完不会立刻生效,要 `p.join()` 等操作系统处理完,`is_alive()` 才变成 False
- 实测注意:Windows 下子进程启动比主进程慢,terminate 发得太早,子进程可能还没来得及执行就没了;被 terminate 杀掉的进程不会执行任何收尾代码,正常结束还是要让子进程自己跑完
- 主进程退出前会自动回收(等)自己创建的非守护子进程——这就是脚本跑完不「扔下」子进程的原因,详见僵尸进程一集

```python
from multiprocessing import Process, current_process
import os, time

def task():
    print(f"子进程 {current_process().name} 运行中,pid={os.getpid()}", flush=True)
    time.sleep(5)                    # 睡 5 秒,给 terminate 制造机会

if __name__ == "__main__":
    p = Process(target=task, name="甲进程")
    p.start()
    print("子进程pid:", p.pid, "| 存活:", p.is_alive())
    time.sleep(1)
    p.terminate()                    # 异步发终止信号,由操作系统执行
    p.join()                         # 等操作系统真正处理完
    print("terminate 并 join 后存活:", p.is_alive())

```

*进程对象常用属性与方法(pid / is_alive / terminate / join)*

### 11. Day39-04 僵尸进程与孤儿进程
> 🎬 对应视频:P464

****子进程死了、父进程不收尸 = 僵尸进程**(占着进程号不放,有害);**父进程先死、子进程被 1 号进程收养 = 孤儿进程**(无害);口诀:僵尸有害,孤儿无害。**

- 进程死后不会立刻消失:会留下一条「死亡记录」(pid、退出状态等)等父进程来**收尸**(wait/join);没被收尸之前它就处于僵尸状态
- 僵尸进程的危害:占着 pid 和进程表空间不释放,pid 是有限资源,僵尸堆积会导致**新进程开不出来**;主要在 Unix/Linux 下讨论(Windows 机制不同,但「父进程要获取子进程退出状态」的概念一致)
- 僵尸的成因与解决:父进程一直活着却从不 join/wait 子进程;解决就是父进程及时 join,或让父进程先退出、由 1 号进程接管收尸
- 孤儿进程:父进程先退出,子进程还活着——会被 **1 号进程(init/systemd)**收养并负责回收,运行不受影响,**无害**;后台服务常以孤儿状态运行
- Python 贴心之处:主进程正常结束前会**自动 join** 所有非守护子进程,所以正常写法基本不会留僵尸;要警惕的是「长期存活的父进程 + 从不 join」的写法

### 12. Day39-05 守护进程
> 🎬 对应视频:P465

**`p.daemon = True`(**必须在 start() 之前设置**)把子进程设为守护进程:**主进程代码一结束它就被强制带走**,不会拖住主进程退出;适合心跳、监控这类辅助任务。**

- 普通子进程:主进程代码跑完后,还要**等所有普通子进程结束**才真正退出(自动回收);守护进程则随主进程代码结束**立即被终止**,不等它跑完
- 设置时机:`p.daemon = True` 必须写在 `p.start()` **之前**,进程已开启再设置会报错;守护的是「主进程的代码」,主进程代码结束的那一刻它就没了
- 典型用途:为主程序打下手的长循环任务——心跳上报、监控、日志收集;主程序一停它们就没有存在的意义,正好一起带走
- 两个限制:守护进程**不允许再开子进程**(会报错);也别指望对它 join 能等到它跑完——主进程代码一结束它就终止了
- 和孤儿进程的区别:守护进程是「主动陪葬」(设计如此),孤儿进程是「被动失怙、被 1 号进程收养」;两者都别和僵尸进程(死了没人收尸)混为一谈

```python
from multiprocessing import Process
import time

def guard():
    while True:
        print("守护进程还在运行", flush=True)
        time.sleep(1)

if __name__ == "__main__":
    p = Process(target=guard)
    p.daemon = True                  # 必须在 start() 之前设置
    p.start()
    time.sleep(3)
    print("主进程代码结束,守护进程被立刻带走")

```

*守护进程随主进程代码结束而立刻终止*

### 13. Day39-06 互斥锁
> 🎬 对应视频:P466

**多个进程并发改同一份数据会产生**竞争**(如抢票超卖):用 `Lock` 把「读-改-写」这段关键代码锁起来,改成**串行**执行,谁先抢到锁谁先操作。**

- 竞争场景:多个进程同时「查余票 → 减 1 → 写回文件」,不加锁时大家都在写回前读到「还剩 1 张」,于是**超卖**;本质是并发修改共享数据(文件)没有保护
- 用法:`lock = Lock()`;`lock.acquire()` 上锁、`lock.release()` 释放;**谁先抢到锁谁先执行,其他进程在 acquire 处阻塞等待**;推荐 `with lock:` 写法,代码块结束自动释放
- 加锁原则:**锁的粒度尽量小**——只圈真正改数据的那几行(购票),查票这类只读操作不必锁;锁的范围越大,并发性越差
- 经典坑:acquire 之后忘了 release(或中间抛异常),其他进程永远等不到锁,程序卡死——用 with 最稳
- 锁保护的是**外部共享资源**(文件、打印终端等),与「进程内存隔离」并不矛盾:进程内存依旧各是各的,只是大家都访问的那份数据需要锁来排队

```python
import json, time
from multiprocessing import Process, Lock

def search(name):
    dic = json.load(open("db.json", encoding="utf-8"))
    print(f"{name} 查到余票 {dic['count']} 张")

def buy(name, lock):
    with lock:                       # 抢到锁才能进入购票环节
        dic = json.load(open("db.json", encoding="utf-8"))
        if dic["count"] > 0:
            dic["count"] -= 1
            time.sleep(0.3)          # 模拟写文件耗时(不加锁时漏洞就在这)
            json.dump(dic, open("db.json", "w", encoding="utf-8"))
            print(f"{name} 购票成功")
        else:
            print(f"{name} 没抢到,票已售罄")

def task(name, lock):
    search(name)                     # 查票可以并发
    buy(name, lock)                  # 买票必须串行

if __name__ == "__main__":
    lock = Lock()
    ps = [Process(target=task, args=(f"用户{i}", lock)) for i in range(3)]
    for p in ps:
        p.start()
    for p in ps:
        p.join()

```

*互斥锁保护抢票:购票环节串行,不再超卖*

### 14. Day39-07 队列介绍
> 🎬 对应视频:P467

**`multiprocessing.Queue` 是**进程安全**的先进先出(FIFO)队列,底层 = **管道(存数据的路)+ 锁(保证读写互斥)**;`put()` 存、`get()` 取,没空位/没数据时**阻塞**。**

- 为什么需要它:进程内存隔离,普通变量、全局变量都传不了数据;队列把「存数据的管道」和「保证安全的锁」打包好,天生可以跨进程使用
- `q = Queue(3)` 指定最多同时存 3 条(不传则只受内存限制);put 时**满了会阻塞**等空位,get 时**空了会阻塞**等数据——这正是三状态图里进程的「阻塞态」
- 先进先出:先 put 的先被 get;能放任何**可以被 pickle** 的对象(字符串、数字、列表、字典都行)
- 常用方法:q.put()/q.get() 阻塞版(可传 timeout);q.put_nowait()/q.get_nowait() 不等待,满/空直接抛异常;q.qsize()/q.empty()/q.full() 查看状态——多进程并发下读到的只是参考值
- 本集先在单个进程内体会 put/get 的行为,下一集把同一个 Queue 传给子进程,就是正式的 IPC 机制

```python
from multiprocessing import Queue

q = Queue(3)               # 最多同时存 3 条数据,先进先出
q.put("first")
q.put(2)
q.put({"k": "v"})
print(q.get(), q.get(), q.get())   # first 2 {'k': 'v'}
print("取空后 qsize/empty:", q.qsize(), q.empty())

```

*Queue 先进先出与取空行为*

### 15. Day39-08 IPC机制
> 🎬 对应视频:P468

**IPC(Inter-Process Communication,进程间通信)专治进程数据隔离:`multiprocessing.Queue` 最常用——把**同一个队列对象**通过 args 传给子进程,一端 put、另一端 get,数据就跨进程过去了。**

- 三步用法:主进程 `q = Queue()` 创建 → 把 q 作为参数传给子进程 `Process(target=child, args=(q,))` → 一端 `q.put(数据)`、另一端 `q.get()` 取;**传的是队列对象,不是数据本身**
- 管道 + 锁的封装让 put/get 天然进程安全;数据在 put 时被 **pickle** 序列化、get 时反序列化,所以只能放可 pickle 的对象(socket、文件句柄这类放不进去)
- 双向通信:主进程 put 子进程 get,子进程也能 put 主进程 get,适合「父发任务、子交结果」的模式(实测:子进程收到任务、处理完把结果传回主进程)
- 另一选择 Pipe(管道):只支持**两个**进程点对点通信,速度略快;Queue 更通用、多进程都能用,日常首选 Queue,了解 Pipe 即可
- 小坑提醒:主进程 put 之后立刻 get,可能**把自己 put 的数据取回来**(大家都在读同一个队列);想让「子进程先收走再回复」,主进程应先 join 再 get

```python
from multiprocessing import Process, Queue

def child(q):
    print("子进程收到:", q.get())     # 队列没数据就阻塞等待
    q.put("子进程:收到,已处理")       # 通过同一个队列把结果传回去

if __name__ == "__main__":
    q = Queue()
    p = Process(target=child, args=(q,))   # 把队列对象传给子进程
    p.start()
    q.put(["主进程的任务", 42])       # 数据被 pickle 后跨进程传递
    p.join()                         # 先等子进程收走消息并回复
    print("主进程收到:", q.get())     # 再从队列取回复

```

*主进程与子进程通过 Queue 双向通信*

### 16. Day39-09 生产者消费者模型
> 🎬 对应视频:P469

**生产者只管产数据放进队列、消费者只管取数据处理,Queue 做中间**缓冲**:两边解耦、各自并发、忙闲互补;结束时**有几个消费者就发几个 None 结束信号**,否则消费者会永远阻塞在 get 上。**

- 三要素:**生产者**(造数据的进程)、**消费者**(用数据的进程)、**队列**(中间缓冲);解决生产快慢不均——生产者不必等消费者腾手,消费者也不怕断粮
- 三大好处:解耦(两边互不认识也能配合)、并发(生产和消费同时进行)、缓冲(高峰排队、低谷不空转)
- 标准写法:生产者循环 put 数据,全部做完后 `q.put(None)` 作为**结束信号**;消费者 `while True: dish = q.get()`,取到 None 就 break 退出
- 结束信号数量 = 消费者数量:2 个消费者就 put 2 个 None,少一个就有消费者永远 get 不到东西、卡死在阻塞里;多个生产者时先 join 所有生产者,再统一发信号
- 进阶:用 `JoinableQueue` 配合 task_done()/join() 可以让主进程等「所有数据被消费完」再结束(了解);这套模型在线程、消息队列(MQ)里还会反复出现

```python
from multiprocessing import Process, Queue
import time, random

def producer(name, food, q):
    for i in range(2):
        time.sleep(random.random() * 0.5)
        dish = f"{food}#{i + 1}"
        print(f"{name} 做好了 {dish}")
        q.put(dish)

def consumer(name, q):
    while True:
        dish = q.get()
        if dish is None:             # 收到结束信号才退出
            break
        print(f"{name} 吃了 {dish}")

if __name__ == "__main__":
    q = Queue()
    ps = [Process(target=producer, args=("厨师甲", "红烧肉", q)),
          Process(target=producer, args=("厨师乙", "清蒸鱼", q))]
    cs = [Process(target=consumer, args=(f"食客{c}", q)) for c in "AB"]
    for p in ps + cs:
        p.start()
    for p in ps:
        p.join()                     # 先等所有生产者做完
    q.put(None)
    q.put(None)                      # 几个消费者就放几个结束信号
    for c in cs:
        c.join()

```

*生产者消费者模型(队列做缓冲,None 作结束信号)*

### 17. Day39-10 线程理论
> 🎬 对应视频:P470

****进程是资源分配的最小单位,线程是 CPU 调度的最小单位**:进程像车间、线程像车间里的工人;同一进程内的线程**共享内存**,创建和切换开销远小于进程。**

- 分工:进程负责「圈资源」(内存空间、打开的文件等),线程负责「真正干活」;一个进程至少有一个主线程,也可以开多个线程共享这份资源
- 类比:进程 = 车间(彼此隔离),线程 = 车间里的工人(共用车间设备和原料);工人之间交流方便(共享内存),车间之间搬东西麻烦(要走 IPC)
- 开销对比:线程的创建、切换不需要换内存空间、不需要重建资源,比进程**轻量得多**;所以线程适合轻量并发和 IO 密集任务,进程适合隔离性、稳定性要求高的场景
- 线程共享数据是把双刃剑:多个线程改同一个全局变量会产生**竞争**(和进程抢票一个道理),必须加锁——进程隔离所以安全,线程共享所以高效但危险
- Python 的 threading 模块提供多线程,接口和 multiprocessing 几乎一致(Process→Thread);由于 GIL 的存在,同一进程内多线程不能并行执行字节码——这个问题后续单独讲

## 📖 并发逐集精讲(Day40~42)

> 🎬 对应课程:Day40~42 逐集精讲(线程/GIL/锁/池/协程/IO模型)

### 1. 章节说明:按集精讲与「并发编程」章节的关系
> 🎬 对应视频:P471~P506

**本章节把 Day40~42 的 **27 个内容小节逐集拆分**,一集一个知识点(title 以集数开头、video 标注单集 P 号),方便**按集查找**;系统性学习并发仍以「并发编程」章为主,本章节是它的逐集精讲版。**

- 组织方式:Day40-03 ~ Day42-08 共 27 个内容小节,每集对应一个知识点,如「Day 40 - 09 线程互斥锁」对应 P479;听课时按集数或 P 号即可快速定位到对应讲义
- 与「并发编程」章的关系:「并发编程」章(py-concurrent)按**主题**系统讲解(pc-3 线程与数据竞争、pc-4 GIL、pc-5 锁/信号量/事件、pc-6 池与协程、pc-10 IO模型),本章节按**视频集数**逐集精讲——先看前者建立知识体系,再按集复习对照
- 三天脉络:**Day40 线程实操**(开启方式 → TCP并发 → join → 数据共享 → 线程对象 → 守护线程 → 互斥锁 → GIL三连问 → 进程线程比较)→ **Day41 同步工具与池协程**(死锁 → 递归锁 → 信号量 → Event → 线程q → 池的概念 → 线程池/进程池 → 协程原理 → gevent → 协程TCP并发)→ **Day42 IO模型**(简介 → 阻塞 → 非阻塞理论/演示 → 多路复用 → asyncio)
- 行政小节不设知识点:P471~P472、P483~P484、P496~P498(复习/今日内容/总结);P505「IO模型总结」的核心对比结论已并入最后一点(Day 42 - 08),P506 为课程收尾
- 代码片段在 Windows(Python 3)下验证:多线程/线程池/进程池/非阻塞/asyncio 实际运行验证(进程池在 Windows 必须 if __name__ == "__main__");含 socket 阻塞调用或依赖第三方的片段只做语法校验(gevent 需 pip install gevent)

### 2. Day 40 - 03 开启线程的两种方式
> 🎬 对应视频:P473

**threading 开线程与 multiprocessing 开进程写法几乎一致:① `Thread(target=函数, args=(参数,))`;② 自定义类**继承 Thread 重写 run**;开线程轻量得多,且 Windows 下**不需要** `if __name__ == "__main__":` 保护。**

- 方式一(常用):`t = Thread(target=task, args=("甲",))`,target 指定子线程要执行的函数,**args 必须是元组**(单个参数也带逗号);`t.start()` 通知操作系统开线程,主线程立刻继续往下,不等它
- 方式二:自定义类继承 Thread,逻辑写在 run 里(任务复杂或要自带属性时用);start() 后自动执行 run——注意**直接调 t.run() 不开新线程**,那只是普通函数调用,与进程的 run 同理
- 与进程的关键差异:线程共享同一进程的内存,子线程里 `os.getpid()` 与主线程**相同**;开线程只是「进程里加个人」,创建开销远小于造一个新进程
- Windows 对比:开进程(spawn 导入父模块)不加保护会无限递归报错;开线程**没有这个问题**,顶层直接 start 也不报错(工程上仍建议把入口写在 __main__ 里,便于统一管理)
- start 之后主线程与子线程并发执行,谁先打印由操作系统调度决定,不要依赖输出顺序

```python
from threading import Thread
import os

def task(name):
    print(f"线程{name}运行中,pid={os.getpid()}", flush=True)   # 与主线程同进程,pid 相同

class MyThread(Thread):                 # 方式二:自定义类继承 Thread,逻辑写进 run
    def run(self):
        print(f"子类线程 {self.name} 运行中,pid={os.getpid()}", flush=True)

t1 = Thread(target=task, args=("甲",))   # 方式一:target 指定函数,args 必须是元组
t2 = MyThread()
t1.start()                              # 通知开线程,主线程立刻继续往下
t2.start()
print("主线程继续执行,不等子线程", flush=True)   # 开线程不需要 __main__ 保护(对比开进程)

```

*开启线程的两种方式(线程无需 __main__ 保护,对比进程)*

### 3. Day 40 - 04 TCP服务端实现并发的效果
> 🎬 对应视频:P474

**单线程 socket 服务端的 accept/recv 都是**阻塞**的,一个客户端不断开别人就进不来;改成**主线程专门 accept、每个连接开一个线程去服务**,就实现了同时服务多个客户端。**

- 痛点:accept() 等新连接、recv() 等数据都是阻塞调用——单线程服务端同一时刻只能伺候一个客户端,其他连接全堵着;这是前面 socket 章遗留的工程问题
- 解法:主线程 `while True` 专门 accept 收新客,每来一个就 `Thread(target=working, args=(conn,)).start()` 把连接交给子线程;各线程各 recv 各的,一个卡住不影响别人
- 代码结构:socket() → bind(("IP", 端口)) → listen(5) → 循环 accept + 开线程;子线程 working 里 recv 到**空字节串**说明客户端断开,close 收尾退出循环
- 为什么用线程不用进程:服务连接是 IO 密集(等数据多、算得少),线程开销小、还天然共享变量(比如在线名单);这套「工人」结构后面还会换成协程(P495),写法几乎不变
- 本片段含阻塞式 socket 调用,仅做语法校验;实测时先跑服务端,再开多个客户端窗口同时收发,观察互不影响——对比单线程版一个客户端独占服务端的现象

```python
import socket
from threading import Thread

server = socket.socket()
server.bind(("127.0.0.1", 8080))
server.listen(5)

def working(conn):
    while True:
        data = conn.recv(1024)          # 阻塞调用:各线程各等各的,互不影响
        if not data:                    # 收到空字节串 = 客户端断开
            break
        conn.send(data.upper())
    conn.close()

while True:
    conn, addr = server.accept()        # 主线程专门接待新连接
    print(f"客户端 {addr} 上线")
    Thread(target=working, args=(conn,)).start()   # 每个连接交给一个子线程服务

```

*每连接开一个线程实现并发服务(含阻塞调用,仅语法校验)*

### 4. Day 40 - 05 线程对象join方法
> 🎬 对应视频:P475

**`t.join()` 让当前线程(通常是主线程)**阻塞等待 t 真正结束**再往下;和进程的 join 一样要**先统一 start、再统一 join**——start 一个立刻 join 一个,并发就退化成串行。**

- start() 只是「通知开线程」,主线程立刻往下走;join() 才是「等它干完」——调用 join 的线程在等待点阻塞(对应三状态图的阻塞态),被 join 的线程结束后才恢复
- 经典错误:for 循环里 start 一个立刻 join 一个——第一个线程干完才轮到第二个 start,三个线程实际**串行**,并发白开了
- 正确姿势:第一个循环把所有线程 start 完(它们并发跑),第二个循环逐个 join;主线程最后一句代码一定最后打印
- join 可传 timeout 只等指定秒数,配合 is_alive() 判断是否还在跑;主线程默认会等所有非守护子线程结束进程才退出,join 的意义是「主线程要在等待点**之后**继续干活」
- 与进程的 join 同名同义、行为一致——threading 的 API 就是照着 multiprocessing 设计的,学过进程版可直接平移

```python
from threading import Thread
import time

def task(name):
    print(f"{name} 开始干活", flush=True)
    time.sleep(1)
    print(f"{name} 干完了", flush=True)

ts = [Thread(target=task, args=(f"线程{i}",)) for i in range(3)]
for t in ts:
    t.start()                  # 三个线程先全部启动(并发跑起来)
for t in ts:
    t.join()                   # 主线程再统一等待:join 哪个就等哪个结束
print("所有子线程结束,主线程最后打印")

```

*先统一 start 再统一 join*

### 5. Day 40 - 06 同一个进程下的多个线程数据共享
> 🎬 对应视频:P476

**同一进程下的多个线程**共享同一份内存**:子线程改了全局变量,主线程立刻看得见——与「进程间数据隔离」正好相反;通信方便了,但并发修改就有竞争,引出后面的互斥锁。**

- 实验:全局 x = 100,子线程里 global x; x = 200,join 后主线程打印的也是 200——同一进程内的线程操作的是**同一个变量**,不是各自的拷贝
- 原因:线程没有独立的内存空间(只有栈等少量私有数据),代码段、数据段、堆都属于进程、由所有线程共享;所以线程间传数据**不必**再走队列/管道那套 IPC
- 对比记忆(并发部分的中心对照):进程 = 数据**隔离**(安全但通信贵,要 Queue/Pipe);线程 = 数据**共享**(通信零成本但不安全,要加锁)
- 坑:多个线程同时执行 x += 1 这种「读-改-写」会互相覆盖,结果小于预期——这就是**数据竞争**;GIL 并不能替你解决业务数据的安全(P480~481 专门辨析),必须自己加互斥锁(下一集)
- 复现建议:开两个线程各对同一个全局变量 +1 十万次,结果常常小于二十万——「共享」不等于「算得对」,这是理解锁存在的最好实验

```python
from threading import Thread

x = 100                        # 全局变量:同一进程内所有线程共享同一份

def change():
    global x
    x = 200                    # 子线程改的就是那份共享的 x
    print("子线程里 x =", x, flush=True)

t = Thread(target=change)
t.start()
t.join()
print("主线程里 x =", x)       # 也是 200 —— 与进程的数据隔离正好相反

```

*验证同进程内线程共享数据(与进程隔离相反)*

### 6. Day 40 - 07 线程对象及其他方法
> 🎬 对应视频:P477

**线程对象常用成员:`t.name`、`t.is_alive()`、`t.join()`;模块级工具 `current_thread()`(我是谁)、`active_count()`/`enumerate()`(全场还有谁);同一进程内所有线程的 **pid 相同**。**

- `t.name`:创建时 `Thread(target=..., name="甲")` 命名,不写默认 Thread-1、Thread-2…;旧的 getName()/setName() 已不推荐,直接用 t.name 属性即可
- `t.is_alive()`:线程是否还在运行(start 之后、run 结束之前为 True);`t.join(timeout=...)` 等待结束——与进程对象同名方法一致
- 线程看自己:`threading.current_thread()` 返回当前线程对象,主线程名字固定是 **MainThread**,子线程里可用它打印「我是谁」;类比进程的 current_process()
- 看全场:`active_count()` 返回存活线程数(含主线程),`enumerate()` 返回存活线程对象列表——排查「线程是否没退出/泄漏」的调试利器
- 有趣证据:所有线程里 `os.getpid()` 打印都相同——它们同属一个进程;线程是 CPU 调度的最小单位,自己不拥有资源,只借用进程的,这一集从代码层面验证了这句理论

### 7. Day 40 - 08 守护线程
> 🎬 对应视频:P478

**`t.daemon = True`(**必须在 start() 之前设置**)把线程设为守护线程:**所有非守护线程一结束它就被强制带走**;主线程代码跑完不算数,进程要等同伙里最后一个非守护线程。**

- 退出规则(与守护进程有个微妙差别):主线程代码跑完后进程并不立刻退出,而是**等所有非守护线程结束**;那一刻一到,守护线程无论执行到哪一行都被直接杀死
- 设置时机:`t.daemon = True` 必须写在 `t.start()` **之前**,线程已启动再设置直接报错;写法与进程一致,含义也是「陪主程序生、陪主程序死」
- 典型用途:心跳上报、定时监控、日志刷新这类「主程序没了它就失去意义」的后台循环任务;关闭它们不需要优雅退出逻辑时,守护线程最省事
- 实测现象:守护线程 while True 打印,主线程睡 1 秒后结束——守护线程打印若干次后戛然而止,最后几条输出可能来不及刷出(被强杀,不给收尾机会)
- 注意:守护线程里别操作需要收尾的外部资源(写文件、数据库事务),它被带走时 finally 都不执行;需要优雅收尾的任务交给普通线程并设计好退出信号

```python
from threading import Thread
import time

def say_hello():
    for i in range(100):
        print(f"守护线程第{i}次问候", flush=True)
        time.sleep(0.2)

t = Thread(target=say_hello)
t.daemon = True                # 必须在 start() 之前设置
t.start()
time.sleep(1)
print("主线程代码运行结束")
# 进程要等所有非守护线程结束才退出;那一刻守护线程被强行带走,收尾代码都不会执行

```

*守护线程随进程(所有非守护线程)结束被带走*

### 8. Day 40 - 09 线程互斥锁
> 🎬 对应视频:P479

**多个线程并发修改共享数据(抢票、计数)会互相覆盖,用 `threading.Lock` 把「查-改-写」整段**锁成串行**,谁抢到锁谁先改;**GIL 保证不了解释器之外你业务数据的安全,必须自己加锁**。**

- 竞争复现:n = 10 张票,三个线程各抢 5 次——不加锁时「查票 → 减 1 → 写回」三步会被别的线程插队,大家都在有票时读到 n、再各自减写,**超卖**;计数器任务结果小于预期同理
- 用法:`lock = Lock()`;`with lock:` 包住关键代码——进入时 acquire、出来自动 release;谁先抢到谁执行,其他线程阻塞在锁上排队,等于把这一段**由并发改成串行**
- 加锁原则:**粒度尽量小**,只锁真正改数据的那几行;查票这类只读操作不必锁进里;锁得太多太粗,多线程退化成单线程还搭上切换开销
- 两个大坑:① acquire 后忘 release(或中间抛异常)→ 其他人永远等锁 → 卡死,坚持用 with;② 锁必须**全局唯一**——每个线程各自新建一把 Lock 等于没锁
- 与 GIL 的关系(下一集展开):GIL 只保证同一时刻一个线程执行字节码,「查-改-写」跨多条字节码仍可能被切走,业务数据照样错——所以解释器有 GIL,你还得有 Lock

```python
from threading import Thread, Lock
import time

n = 10                         # 10 张票:全局变量被三个线程共享
lock = Lock()

def grab(name):
    global n
    for _ in range(5):
        with lock:             # 把「查票-扣票」整体锁成串行
            if n > 0:
                n -= 1
                print(f"{name} 抢到一张,剩余 {n} 张", flush=True)
            else:
                print(f"{name} 没抢到,票已售罄", flush=True)
        time.sleep(0.01)

ts = [Thread(target=grab, args=(f"用户{i}",)) for i in range(3)]
for t in ts:
    t.start()
for t in ts:
    t.join()

```

*互斥锁把「查票-扣票」锁成串行,不再超卖*

### 9. Day 40 - 10 GIL全局解释器锁理论介绍
> 🎬 对应视频:P480

**GIL(全局解释器锁)是 CPython 的历史设计:**同一进程内同一时刻只允许一个线程执行 Python 字节码**——多线程无法利用多核做并行计算,但线程遇到 IO 阻塞时会释放 GIL 让给别人。**

- 是什么:CPython 解释器里的一把**全局大锁**,任何线程执行字节码前都必须拿到 GIL;效果 = 单进程内的多线程在 CPU 执行层面串行,核再多,同一时刻也只有一个核在跑你的 Python 线程
- 为什么存在:CPython 的内存管理(引用计数)**非线程安全**,用一把全局锁保护最省事;注意它是**解释器的实现细节**,不是 Python 语言特性——Jython、IronPython 就没有 GIL(去掉它会拖慢单线程,官方多年权衡未动)
- 关键机制:线程遇到 IO(recv/read/sleep 等)会**释放 GIL**,或时间片到(默认 5ms,sys.getswitchinterval 可查)被强制让出——所以 **IO 密集任务多线程依然有效,计算密集任务多线程毫无加速**
- 必背结论:**计算密集用多进程**(多个进程各有各的 GIL,真并行吃满多核);**IO 密集用多线程/协程**(等待时让出 GIL,切换又便宜)——这一条直接决定 P482 的比较结论
- 澄清边界:GIL 针对的是**同一进程内**的线程;多进程之间各持各的 GIL 互不影响——想真并行就开多个进程,这是进程池存在的根本理由

### 10. Day 40 - 11 GIL与普通互斥锁的区别
> 🎬 对应视频:P481

**GIL 是**解释器级、自动**的锁,保护 CPython 内部数据同一时刻只有一个线程跑;互斥锁是**用户级、手动**的锁,保护你的业务数据不被「查-改-写」打断——**GIL 保护的是解释器,不是你的数据**。**

- 类比:GIL 像公司唯一的大门(自动管理,大家排队轮流进);你自己的保险柜还得配自己的钥匙(手动管理)——大门管得了人流,管不了你柜里的账本
- 为什么有 GIL 还会数据不安全:线程执行途中可能**释放 GIL**(时间片到/遇 IO),「查票-减1-写回」三步被切在中间,另一个线程拿着**旧数据**继续算——GIL 保证「同一时刻只有一个线程在跑」,不保证「我的三步没人插队」
- 区别清单:GIL 全局唯一、解释器自动加/释放;Lock 用户创建、手动(或 with)加/释放;GIL 的临界区是字节码执行,Lock 的临界区**由你圈定**;GIL 何时释放不可控,Lock 何时释放完全听你的
- 验证思路:两个线程对同一变量各加十万次,理论上应等于二十万;若在「读-改-写」之间人为插入 sleep(模拟时间片切换/IO),**稳定**出现少加——说明错账来自竞争而非 GIL 失效
- 一句话:GIL 管解释器的安全,Lock 管数据的安全;层级不同,谁也替代不了谁——这集是 GIL 三连问(P480~482)里最容易被面试问到的一问

### 11. Day 40 - 12 多进程与多线程比较
> 🎬 对应视频:P482

****计算密集用多进程**(绕开 GIL、多核真并行),**IO 密集用多线程/协程**(等待时让出、切换便宜);线程开销小、共享内存但要加锁,进程开销大、数据隔离但更稳——按任务类型选型。**

- 计算密集(纯 CPU:数值运算、压缩、加密):多线程在 GIL 下串行执行,毫无加速还搭上线程切换;多进程各有 GIL、**真并行**,核越多越快——选多进程
- IO 密集(网络、磁盘、sleep 多:爬虫、socket 服务):大部分时间在**等**,等的时候线程让出 GIL/进程让出 CPU,多线程切换比进程便宜得多;更轻的还有协程(Day41 后半)——首选多线程/协程
- 开销对比:进程创建要复制资源、独立内存,切换要换内存空间;线程只在进程内加一份栈和寄存器上下文,**创建和切换都便宜**——轻并发、高频创建选线程
- 数据与稳定性:线程共享内存,通信方便但共享数据要加锁(危险);进程内存隔离,通信要走 Queue/Pipe,但**一个崩不连累另一个**(安全)——稳定性优先(如浏览器多标签)选进程
- 记忆口诀:**重计算开进程,重等待开线程(或协程)**;真实项目常见组合拳——进程池铺满各核,每个进程里再开线程/协程处理 IO,两层并发各取所长

### 12. Day 41 - 03 死锁现象
> 🎬 对应视频:P485

**两个线程**各持一把锁、又都想拿对方那把**,谁也不撒手 → 互相等待、永远阻塞,这就是死锁;典型成因:多把锁加锁顺序不一致,或同一线程对同一把普通锁重复 acquire。**

- 经典场景(筷子吃面):线程1 拿了筷子锁 A 想拿面锁 B,线程2 拿了 B 想拿 A——各自握一把、互等对方,程序**卡死不再有任何输出**,CPU 占用为零(都在阻塞)
- 成因一:多把锁的**加锁顺序不一致**——约定「所有线程都先拿 A 再拿 B」就不会死锁;成因二:同一个线程对同一把 Lock 连续 acquire 两次,第二次等自己释放,**自死锁**(下一集递归锁专治)
- 复现要点:两个线程先 sleep 1 秒错开,保证各自拿到第一把锁后再去抢第二把,死锁 100% 出现;本集代码故意保留死锁,运行后需强制结束进程
- 预防四板斧:① 统一加锁顺序;② 全部用 with 锁,保证异常时也释放;③ acquire(timeout=...) 加超时,拿不到就放弃重试;④ 需要重入就用 RLock
- 可怕之处:死锁**不报错、不退出、不耗 CPU**,线上问题往往要 dump 线程栈才能定位——所以「怎么加锁」从设计起就要讲纪律,而不是出了事再补

```python
from threading import Thread, Lock
import time

lockA = Lock()
lockB = Lock()

def thread_1():
    lockA.acquire()
    print("线程1 拿到A,还想拿B", flush=True)
    time.sleep(1)              # 错开时间,保证线程2先拿到B
    lockB.acquire()            # B在线程2手里,永远等不到 —— 死锁
    print("线程1 同时拿到A和B", flush=True)
    lockB.release()
    lockA.release()

def thread_2():
    lockB.acquire()
    print("线程2 拿到B,还想拿A", flush=True)
    time.sleep(1)
    lockA.acquire()            # A在线程1手里,也永远等不到 —— 互相等,程序卡死
    print("线程2 同时拿到B和A", flush=True)
    lockA.release()
    lockB.release()

t1 = Thread(target=thread_1)
t2 = Thread(target=thread_2)
t1.start()
t2.start()

```

*两人各持一把锁互等对方:死锁(运行后程序将卡死,仅供观察)*

### 13. Day 41 - 04 递归锁
> 🎬 对应视频:P486

**`RLock`(递归锁/可重入锁)允许**同一线程多次 acquire**,内部计数器记层数,**release 同样次数才真正开锁**——专治「同一线程重复拿同一把锁」造成的死锁。**

- 原理:RLock 记录持有者与计数;同一线程再来 acquire 不阻塞、**计数 +1**;每 release 一次计数 -1,**减到 0 才真正释放**,别的线程才能进
- 解决的问题:函数 a 拿锁后调用也要拿**同一把锁**的函数 b——普通 Lock 在 b 里永久等待(自己等自己);RLock 可重入,计数到 2,退出时 release 两次即可
- 也能解救上一集的筷子面条死锁:两把 Lock 换成**一把 RLock**,两个线程各 acquire 两次——同一线程可重入,不会互卡;但工程上更优先「统一加锁顺序」
- 代价:能跑 ≠ 正确,递归锁可能掩盖「不该嵌套加锁」的设计问题;把它当工具,别当免死金牌
- 记法:Lock = 一人进了门,没出来谁也进不去(包括自己);RLock = 同一个人可以反复进,**进几次就要出几次**,门才真正打开

```python
from threading import Thread, RLock

rlock = RLock()                # 递归锁:同一线程可重复 acquire,内部计数器记录层数

def eat(name):
    rlock.acquire()            # 计数 1
    print(f"{name} 拿到筷子", flush=True)
    rlock.acquire()            # 计数 2 —— 换成普通 Lock 这里就把自己锁死了
    print(f"{name} 拿到面条,开吃", flush=True)
    rlock.release()            # 计数 1
    rlock.release()            # 计数 0,别的线程才有机会进

ts = [Thread(target=eat, args=(f"食客{i}",)) for i in range(3)]
for t in ts:
    t.start()
for t in ts:
    t.join()
print("三人都吃上了,没有死锁")

```

*RLock 可重入:同一线程 acquire 多次不卡死*

### 14. Day 41 - 05 信号量
> 🎬 对应视频:P487

**`Semaphore(N)` 允许同一时刻**最多 N 个线程**进入(互斥锁的多人版):第 N+1 个开始排队,有人 release 才放行下一个——适合限流,如最多 5 个并发连接、10 个坑位。**

- 概念:互斥锁本质是 N=1 的信号量;`Semaphore(5)` 相当于锁箱里有 **5 把钥匙**——acquire() 拿钥匙(没钥匙就阻塞),release() 还钥匙,同时最多 5 个线程在临界区里
- 计数语义:内部计数器初始为 N,acquire 减 1(到 0 后再 acquire 阻塞),release 加 1;日常用 `with sm:` 最稳,进出自动配对
- 典型场景:限并发数——数据库连接池上限、爬虫同时最多抓 20 个页面、KTV 只有 5 个包间;注意它只管「同时几个」,不管先后顺序(排队顺序交给队列)
- 与池的辨析(下一集展开):信号量限的是「**进入代码段的并发数**」,线程本身早就开好了;池限的是「干活的**工人数量**」,工人还复用——两者层次不同
- 坑:release 多于 acquire 会让计数悄悄超过 N,「最多 N 个」的约束被放大;acquire 了忘 release 会饿死后来的线程——依然推荐 with 写法

```python
from threading import Thread, Semaphore
import time

sm = Semaphore(5)              # 同一时刻最多 5 个线程进入(类比 5 个坑位)

def toilet(name):
    sm.acquire()               # 第 6 个开始要在这一行排队等
    print(f"{name} 占到一个坑位", flush=True)
    time.sleep(1)
    print(f"{name} 腾出坑位", flush=True)
    sm.release()

ts = [Thread(target=toilet, args=(f"顾客{i}",)) for i in range(10)]
for t in ts:
    t.start()
for t in ts:
    t.join()
print("10 人分两批用完 5 个坑位")

```

*Semaphore(5):10 人抢 5 个坑位,分两批放行*

### 15. Day 41 - 06 Event事件
> 🎬 对应视频:P488

**Event 是线程间的「红绿灯」:一把全局旗子默认 **False**,`wait()` 的线程在旗子没立起来时阻塞;`set()` 一立,**所有等待者同时放行**——适合「多个线程等同一个信号」的联动场景。**

- 核心四方法:`event.set()` 立旗(True)、`event.wait()` 旗子为 False 就阻塞(可传 timeout)、`event.clear()` 收旗复位 False、`event.is_set()` 查看当前状态
- 课程场景(老板喊开饭):多个食客线程 `wait()` 干等,老板线程备菜 2 秒后 `set()`,**所有食客同时开动**——一对一通知用不上它,「一对多同时放行」才是它的主场
- 另一经典场景:多个 worker 线程 wait() 等主线程完成初始化(连数据库、加载配置)再统一开工,避免「边初始化边干活」的错乱;也可做「等所有连接就绪再发车」的起跑线
- 三工具分工:Lock 管互斥(别一起改)、Semaphore 管限量(最多几个一起)、Event 管通知(到点一起走)——线程协作的三个维度各配一把手
- 坑:set() 之后旗子一直立着,**新来的 wait() 直接通过**;要重复发令就得 clear() 复位;更精细的「等待某条件成立」可用 Condition(条件变量)——课程点到为止

```python
from threading import Thread, Event
import time

event = Event()                # 全局唯一的事件,旗子默认 False = 还没开饭

def diner(name):
    print(f"{name} 坐下等开饭", flush=True)
    event.wait()               # 旗子是 False 就阻塞在这里
    print(f"{name} 开始干饭", flush=True)

def boss():
    time.sleep(2)              # 老板花 2 秒上菜
    print("菜上齐了,开饭!", flush=True)
    event.set()                # 旗子立成 True,所有等饭的人同时放行

ts = [Thread(target=diner, args=(f"食客{i}",)) for i in range(3)]
ts.append(Thread(target=boss))
for t in ts:
    t.start()
for t in ts:
    t.join()

```

*Event:老板 set 一声喊,全体食客同时开饭*

### 16. Day 41 - 07 线程q
> 🎬 对应视频:P489

**线程间通信用 **queue 模块**(不是 multiprocessing.Queue):`Queue` 先进先出、`LifoQueue` 后进先出、`PriorityQueue` 按优先级出——自带锁、线程安全,是线程版生产者消费者的标配。**

- 为什么不用 list:裸 list 的「判空再取」这类组合操作没有锁保护,多线程下照样竞态;`queue.Queue` 把锁和条件变量封装好,put/get 可直接放心用
- 三种队列:`Queue()` FIFO 排队;`LifoQueue()` 像栈后进先出;`PriorityQueue()` 放 **(优先级, 数据)** 元组,数字越小越先出(同级再按内容排)
- 常用方法:put/get 阻塞版(满/空时等待,可传 timeout);put_nowait/get_nowait 满/空直接抛 queue.Full/Empty;qsize()/empty()/full() 查状态(并发下仅作参考)
- 别和 multiprocessing.Queue 混:queue.Queue 服务**同一进程内**的线程(共享内存直接传对象);multiprocessing.Queue 要跨进程 **pickle** 传输;两者不可互相替代
- 线程版生产者消费者:结构与 Day39-09 完全一致(生产者 put、消费者 while True get、None 作结束信号,几个消费者放几个 None),只是 Process 换 Thread、Queue 换 queue.Queue——模型跨进程/线程通用

```python
import queue

q = queue.Queue()              # FIFO:先进先出,线程安全的普通队列
q.put("first")
q.put(2)
q.put((3, "third"))
print("FIFO :", q.get(), q.get(), q.get())

lq = queue.LifoQueue()         # LIFO:后进先出,像栈
lq.put(1)
lq.put(2)
lq.put(3)
print("LIFO :", lq.get(), lq.get(), lq.get())

pq = queue.PriorityQueue()     # 优先级队列:数字越小越先出
pq.put((2, "普通任务"))
pq.put((1, "紧急任务"))
pq.put((3, "闲杂任务"))
print("优先级:", pq.get(), pq.get(), pq.get())

```

*线程安全的三种队列:Queue/LifoQueue/PriorityQueue*

### 17. Day 41 - 08 池的概念介绍
> 🎬 对应视频:P490

**池 = **预先创建固定数量的工人**(进程/线程)蹲坑待命,任务来了分给空闲工人,干完**回池复用**——省去「临时创建、用完销毁」的开销,还天然给系统限流兜底。**

- 没有池的问题:来一个任务开一个进程/线程,创建销毁都是系统级开销;任务洪峰一来,成百上千个进程/线程把内存和调度拖垮(线程过多还会疯狂上下文切换,越切越慢)
- 池的机制:启动先开 N 个工人等着 → 任务提交进池 → **空闲工人**领任务执行 → 干完不销毁、回池等下一个——「复用」是池的灵魂,代价都摊薄了
- 附加好处:池天然**限流**——最多 N 个并发,系统压力可控;类似上一集的信号量,但池连工人带限制一起管,还省了反复创建
- N 怎么定:计算密集开 **CPU 核数**(os.cpu_count())个即可,多了也抢不到核;IO 密集可以开更多(几十上百)——等待多、真干活的少;实践中从「核数 ~ 2×核数」试起
- Python 的两代池:老的 `multiprocessing.Pool`(map/apply_async)与新标准 `concurrent.futures` 的 `ProcessPoolExecutor`/`ThreadPoolExecutor`(统一接口、future 取结果)——接下来两集用新接口分别实操线程池与进程池

### 18. Day 41 - 09 线程池
> 🎬 对应视频:P491

**`ThreadPoolExecutor(n)` 建 n 个线程的池:`submit(fn, *args)` 提交任务立刻返回 future,`fu.result()` 阻塞取结果(任务异常在这里抛出),`shutdown()` 收摊——IO 密集任务的推荐写法。**

- 三步走:`pool = ThreadPoolExecutor(5)` 建池 → `fu = pool.submit(job, 参数)` 提交(立刻返回 **future** 凭证,不阻塞)→ `fu.result()` 拿结果(没算完就在这等);用完 `pool.shutdown(wait=True)` 关池
- future 是「未来结果的凭证」:`result()` 阻塞等结果并返回、`exception()` 单独取异常、`done()` 查是否完成——这是异步任务的标准交互对象,后面异步生态里反复出现
- 批量提交:10 个任务 5 个工人,先提交的先被领走,**先干完的工人立刻接下一个**;result() 按提交顺序取结果,谁先算完不影响这个顺序(实测总耗时 ≈ 任务数/工人数 × 单任务耗时)
- 便捷写法:`pool.map(job, range(10))` 一次提交整序列、结果按序可迭代;`with ThreadPoolExecutor(5) as pool:` 语法块结束自动 shutdown,更推荐
- 两个注意:① 任务函数里抛的异常**只在 result() 时才重新抛出**,只 submit 不 result 异常会被静默吞掉;② 池不提供数据保护,任务里改共享数据照样要加锁;另外线程池对任务函数没有 pickle 要求(进程池有,下一集)

```python
from concurrent.futures import ThreadPoolExecutor
import time

def job(n):
    time.sleep(1)              # 模拟耗时任务(IO 等待)
    return f"任务{n}的计算结果"

pool = ThreadPoolExecutor(5)                # 5 个线程伺候所有任务,用完复用
futures = [pool.submit(job, i) for i in range(10)]   # 提交 10 个任务,立刻返回凭证

for fu in futures:
    print(fu.result(), flush=True)          # 没算完就阻塞等;结果按提交顺序返回

pool.shutdown(wait=True)                    # 收摊:等任务全部干完再关池
print("线程池已关闭")

```

*ThreadPoolExecutor:submit 提交、result 取结果*

### 19. Day 41 - 10 进程池
> 🎬 对应视频:P492

**`ProcessPoolExecutor(n)` 与线程池**同一套接口**,把任务交给 n 个工作进程**真并行**(各自 GIL、各自内存);Windows 下必须写在 `if __name__ == "__main__":` 里,任务函数与参数必须可 pickle。**

- 接口完全一致:submit/result/shutdown/map 与线程池一模一样——从线程池换进程池常常只改一行(`ThreadPoolExecutor` → `ProcessPoolExecutor`),这正是 concurrent.futures 的设计目的
- Windows 大坑(进程绕不开):创建工作进程走 **spawn**、会重新导入主模块,不写 `if __name__ == "__main__":` 保护直接报错;任务函数必须定义在**模块顶层**(可被 pickle),lambda 和嵌套函数传不过去
- 结果回传:子进程的返回值经 **pickle** 跨进程送回,`fu.result()` 拿到的就是它;子进程里的异常同样在 result() 时于主进程重新抛出
- 计算密集的收益:纯计算任务 4 核开 4 进程,总耗时约为单进程的 1/4(实测可对拍);IO 密集用进程池收益有限,还多付进程创建与序列化的成本——选型记 P482 的结论
- 工程习惯:池大小计算密集取 os.cpu_count();`shutdown(wait=True)` 等全部任务完成再关,`with ProcessPoolExecutor(n) as pool:` 自动收摊;别在任务里再开同类型池,小心进程爆炸

```python
from concurrent.futures import ProcessPoolExecutor
import os

def job(n):
    return f"任务{n} 由进程 {os.getpid()} 完成"

if __name__ == "__main__":      # Windows 下开进程必须写这行,否则 spawn 报错
    pool = ProcessPoolExecutor(3)           # 最多 3 个工作进程真并行(各自 GIL)
    futures = [pool.submit(job, i) for i in range(6)]
    for fu in futures:
        print(fu.result(), flush=True)      # 返回值经 pickle 跨进程送回主进程
    pool.shutdown(wait=True)
    print("进程池已关闭")

```

*ProcessPoolExecutor 真并行(Windows 必须 __main__ 保护)*

### 20. Day 41 - 11 协程基本原理
> 🎬 对应视频:P493

**协程是**单线程内的并发**:切换由程序员(而非操作系统)控制,在任务之间主动跳转、切走的地方下次接着跑;开销极小,但**遇到阻塞调用整个线程全卡**——协程必须搭配「遇到 IO 就让出」。**

- 与进程/线程的本质区别:进程/线程由**操作系统内核抢占式调度**(说切就切,切换要陷入内核,微秒级);协程在**用户态**由程序自己让出,切换只是保存/恢复少量上下文,纳秒~微秒级,便宜一到两个数量级
- 实现基础:Python 的**生成器 yield** 可以暂停函数、保留现场、恢复执行——最早的协程就是拿生成器拼出来的;greenlet 把「切换」做到 C 层(栈切换);Python 3.5+ 有了 async/await 原生语法
- 协作式的前提:协程靠大家**自觉让出**才有并发;谁调用了真阻塞调用(time.sleep、阻塞 recv),**整个线程连同所有协程一起卡死**——这是协程最大的坑,所以才有下一集的猴子补丁
- yield 直观演示思路:两个生成器交替 next,各自的循环互相「插队」打印——单线程里出现交替执行的假象;多任务「同时推进」不靠多核,靠等待被别人利用
- 定位:协程**不解决并行**(还是一个核一个线程),解决**海量 IO 等待的高并发**——10 万个连接大多在等数据,协程让等待时间被别的任务填满;所以协程 ≈ IO 密集的终极形态(配合事件循环)

### 21. Day 41 - 12 gevent模块
> 🎬 对应视频:P494

**gevent 是基于 greenlet 的第三方协程库:`spawn` 创建协程、`joinall` 等待完成;关键是 **monkey.patch_all()** 把 socket/time 等标准库偷换成「遇到 IO 主动让出」的版本——同步写法、异步效果。**

- 两大件:`monkey.patch_all()` **必须放在其他 import 之前**(文件最顶部),把 socket/time/urllib 等打上猴子补丁;`spawn(函数, 参数)` 创建协程,`joinall([g1, g2, ...])` 阻塞等这批协程全部干完
- 效果验证:3 个各自 `time.sleep(1)` 的任务并发跑,总耗时 ≈ **1 秒**而不是 3 秒——sleep 已被 patch,等 IO 时让出协程给别人;代码一行没改(还是同步写法),行为已变并发
- 第一坑就是补丁位置:忘了 patch_all() 或写在 import time 之后,time.sleep 就还是真阻塞,整个线程所有协程一起干等——「程序变慢但结果正确」的隐蔽问题
- gevent 版服务端套路:主协程 accept,每来一个连接 spawn 一个协程服务它——结构完全复刻线程版 TCP 并发(P474),只是工人从线程换成协程(下一集 P495 实操)
- 现状:第三方库需 `pip install gevent`,常见于老项目和 gunicorn 的 gevent worker;新代码官方路线是 asyncio(P504)——但「把阻塞库偷换成让出式」的思路两者一脉相承

```python
from gevent import monkey
monkey.patch_all()              # 猴子补丁:必须放在其他 import 之前执行
import time
from gevent import spawn, joinall

def task(name):
    print(f"{name} 开始", flush=True)
    time.sleep(1)               # 已被 patch:遇到 IO 让出协程,不是真睡
    print(f"{name} 结束", flush=True)

start = time.time()
gs = [spawn(task, f"协程{i}") for i in range(3)]
joinall(gs)                     # 等所有协程跑完
print(f"3 个各睡 1 秒的任务,总耗时约 {time.time() - start:.1f} 秒")

```

*gevent 并发:3 个各睡 1 秒的任务约 1 秒完成(需 pip install gevent)*

### 22. Day 41 - 13 协程实现TCP并发
> 🎬 对应视频:P495

**把线程版并发服务端的「每连接开一个线程」换成「**每连接 spawn 一个协程**」:accept 主循环 + spawn(handler, conn),被 patch 过的 recv 遇 IO 自动让出——**单线程**撑起大量并发连接。**

- 三步改造(对照 P474 线程版):① 文件顶部先 `monkey.patch_all()` 再 import socket;② 主协程 `while True: conn, addr = server.accept()`,每来一个连接 `gevent.spawn(working, conn)`;③ working 里 recv/send 照常写——patch 过的 recv 没数据时**让出协程**,别的连接照常被服务
- 并发效果:多个客户端同时连接、各自收发互不影响;服务端从头到尾**只有一个线程**——没有线程创建销毁的开销,没有 GIL 之争,没有线程过多导致调度崩溃的问题
- 为什么快:上万个连接大多阻塞在各自 recv 上,gevent 的事件循环只在「谁就绪了」之间切换——**等待被合并**,单线程吞吐反而高;这就是「IO 密集选协程」的落地样板
- 三版对照:多进程版(每连接一进程,隔离稳但贵)、多线程版(P474,通用够用)、协程版(单线程,海量连接)——**写法结构一模一样,换的只是工人**;这个对照是 Day40~42 并发主线的一次大汇合
- 边界与提醒:协程只适合 IO 密集,handler 里一段纯计算大循环会把整个服务端卡死(没人能让出);上生产还要处理超时、异常捕获、半链接上限这些工程细节

### 23. Day 42 - 03 IO模型简介
> 🎬 对应视频:P499

**一次 IO(以 recv 为例)分两阶段:**① 等数据就绪**(数据到内核缓冲区)、**② 拷贝数据**(内核 → 用户空间);阻塞/非阻塞/多路复用/异步四个模型的差别,全在「等的方式」和「拷贝谁来干」。**

- 前置知识:用户空间与内核空间隔离;网卡收到的数据**先进内核缓冲区**,recv 实际是「等内核有数据 → 内核把数据拷到你的变量」;你的 Python 代码跑在用户态,碰不到网卡
- 两阶段框架:阶段一**等待数据就绪**(数据从网络到达内核缓冲区),阶段二**内核拷贝到用户进程缓冲区**,此后代码才能处理 data——四个模型就按这两阶段分类记忆
- 四模型速览:**阻塞 IO**(两阶段全傻等)、**非阻塞 IO**(阶段一轮询问、阶段二阻塞)、**IO 多路复用**(一个监督员帮你看一堆 fd,就绪了再自己去拷)、**异步 IO**(连拷贝都不用你管,完事通知你)
- 同步/异步的分界线:**拷贝阶段要不要自己动手**——前三个模型拷贝都得自己 recv,都是同步家族(同步阻塞/同步非阻塞);只有异步 IO 连拷贝都不管,才是真异步
- 本集是 Day42 的地图:P500 拆阻塞、P501~502 拆非阻塞(理论+演示)、P503 拆多路复用、P504 拆 asyncio(异步),最后 P505 总结对比(结论已并入 P504 一点)

### 24. Day 42 - 04 阻塞IO模型
> 🎬 对应视频:P500

**阻塞 IO **两个阶段全程挂起**:recv 发出后先阻塞等数据、再阻塞等拷贝,期间线程什么都干不了——写法最简单、最常用,但一个线程只能伺候一个连接。**

- 流程:调用 recv → 无数据就**阻塞**(线程挂起、让出 CPU,对应三状态图的阻塞态)→ 数据到达内核缓冲区 → 内核拷贝到用户空间 → recv 返回;「等」和「拷贝」调用方全程被动
- 优点:编程模型最简单,代码顺序执行、最好理解;**默认 socket 就是阻塞的**,前面 socket 章(P432~P447)和线程版 TCP 并发(P474)全在这个模型上
- 缺点:一个线程同一时刻只能等**一个** recv;服务端单线程时一个客户端不说话,别的客户端全堵死——所以才有「每连接一线程」的补救(P474),但线程本身是资源,连接一多照样崩
- 别看不起它:阻塞等待时线程**睡死不耗 CPU**,比后面非阻塞模型的空转轮询省电;它的缺点只在「占着线程名额」和「不能一人管多个 IO」
- 改进方向(后面三集的故事线):等的时候能干别的(非阻塞轮询)→ 别自己盯、找人替你盯(select 多路复用)→ 连拷贝都不用管(异步 IO)——每个模型都是对阻塞 IO 某个痛点的回应

### 25. Day 42 - 05 非阻塞IO模型理论
> 🎬 对应视频:P501

**非阻塞 IO 把**第一阶段**改成「问一下就走」:没数据**立刻返回** BlockingIOError、不挂起;轮询间隙能干别的,但反复空问烧 CPU,第二阶段拷贝依旧自己做——所以只是「**同步非阻塞**」。**

- 开关:`sk.setblocking(False)` 一行把套接字切成非阻塞;此后 accept/recv/connect 没有好消息**不等待**,立刻抛 BlockingIOError(Windows 下是 WSAEWOULDBLOCK 错误码的映射)
- 两阶段账单:阶段一从「挂起死等」变成「**轮询询问**」(不阻塞,但要不要轮询、轮询多勤是你的事);阶段二数据就绪后的 recv 拷贝**照样自己调、照样阻塞**——所以它是同步家族
- 优点:单线程能在等 A 的间隙去伺候 B——把「等」的时间利用起来;程序从被动等变成主动查,IO 之外的事(处理别的连接、算点东西)都能插空干
- 缺点:白问一次烧一次 CPU(**忙等 busy-waiting**);连接多了轮询列表变长、响应延迟上升;还要自己维护「哪些连接还没就绪」的状态,代码复杂度上来了
- 定位:纯非阻塞轮询工程上很少直接用,它是理解「就绪通知」的垫脚石——自然引出的问题:「能不能我不问、有事你叫我?」答案就是 IO 多路复用(P503)

### 26. Day 42 - 06 非阻塞IO模型代码演示
> 🎬 对应视频:P502

**`setblocking(False)` + `try accept / except BlockingIOError` 的循环就是非阻塞轮询:没有客户端时 accept **立刻抛异常返回**,循环刷得飞快——实测亲眼看到「不阻塞」与「空转烧 CPU」一体两面。**

- 核心写法:先 `server.setblocking(False)`,循环里 `try: conn, addr = server.accept() except BlockingIOError: 干别的`——**异常不是错误**,是「暂时没消息」的信号,捕获后继续循环
- 实测现象:没有客户端连入时,1 秒内这个空循环能转几十上百万次(计数就是证据):accept 不挂起、程序始终**活着**——但也始终**占着 CPU** 干没用的事
- 扩展成单线程多连接的骨架:非阻塞 accept 拿到连接就收进列表;循环遍历列表逐个 try recv,谁就绪处理谁、没就绪跳过——单线程「看起来」同时伺候多个客户端,这就是课程演示的完整效果
- 本演示的价值:用计数器把「轮询的代价」变成肉眼可见的数字——CPU 被空转吃满;解决思路:别自己盯,让内核帮你盯(select/poll/epoll,下一集)
- 细节坑:非阻塞下 Windows/Linux 抛的都是 BlockingIOError,注意和 ConnectionResetError 等**真错误**分开处理;非阻塞 connect 的行为各平台差异更大,演示主线聚焦 accept/recv

```python
import socket, time

server = socket.socket()
server.bind(("127.0.0.1", 8080))
server.listen(5)
server.setblocking(False)       # 关键一步:关掉阻塞开关

start = time.time()
polls = 0
while time.time() - start < 1:  # 没有客户端连入时,观察 accept 的行为
    try:
        conn, addr = server.accept()   # 有连接立刻拿到
        print("客户端上线:", addr)
    except BlockingIOError:
        polls += 1               # 没消息不等待,立刻抛异常返回
server.close()
print(f"1 秒内空转轮询了 {polls} 次:非阻塞不挂起,但空转白烧 CPU")

```

*非阻塞 accept:没连接立刻抛 BlockingIOError(空转计数)*

### 27. Day 42 - 07 IO多路复用
> 🎬 对应视频:P503

**`select.select(rlist, wlist, xlist, timeout)` 把一堆套接字**交给内核监督**:任一就绪(可读/可写/异常)才返回,程序只处理就绪的——「一个人替你等一堆」,拷贝阶段仍是自己的(还是同步)。**

- 原理:把「轮询问每个连接好了没」的活**外包给内核**;select 阻塞直到监听列表里至少一个 fd 就绪,返回就绪子集;程序只处理返回的——不空转、不漏事,单线程可管成百上千连接
- 经典服务器骨架:`rlist = [server]`;循环 `readable, _, _ = select.select(rlist, [], [])` → 遍历 readable:**是 server 就 accept 新连接并入 rlist;是已连接 socket 就 recv 处理**,recv 为空则 close 并移出 rlist
- 就绪语义:监听套接字「可读」= 有新连接可 accept;连接套接字「可读」= 有数据可 recv **或对方断开**(recv 返回空);一个 select 同时看住两类动静——这就是「复用」的含义
- 三兄弟与平台:**select** 跨平台但监听数量有 FD_SETSIZE(1024)上限、每次全列表拷进内核;**poll** 去掉数量上限;**epoll**(Linux)内核事件表 + 回调,海量连接首选;Python 的 selectors 模块自动挑当前平台最优实现
- 定位:IO 多路复用**依旧同步**——就绪后还得自己 recv 拷贝;它解决的是「等的效率」,配合回调/协程才拼成完整高并发方案(asyncio 底层正是 selectors + 事件循环,下一集)

```python
import socket
import select

server = socket.socket()
server.bind(("127.0.0.1", 8080))
server.listen(5)

rlist = [server]                # 要监督「可读动静」的套接字列表
while True:
    readable, _, _ = select.select(rlist, [], [], 1)   # 有动静才返回,最多等1秒
    for sk in readable:
        if sk is server:        # 监听套接字可读 = 有新连接
            conn, addr = sk.accept()
            print("客户端上线:", addr)
            rlist.append(conn)  # 新连接也纳入监督
        else:                   # 已连接套接字可读 = 有数据(或对方断开)
            data = sk.recv(1024)
            if data:
                sk.send(data.upper())
            else:
                print("客户端下线")
                rlist.remove(sk)
                sk.close()

```

*select 同时监督监听与已连接套接字(含阻塞调用,仅语法校验)*

### 28. Day 42 - 08 asyncio模块
> 🎬 对应视频:P504~P505

**asyncio 是官方协程框架:**async def 定义协程、await 在可等处让出、事件循环调度**;`asyncio.gather` 并发跑一组任务,总耗时取决于最慢的那个;至此四模型凑齐——**asyncio 是 Python 异步 IO 的落地**。**

- 三件套:`async def task()` 定义协程函数(**调用它不执行**,只生成协程对象);`await` 是让出点,只能写在 async 函数里——等 IO(asyncio.sleep、异步网络库)时把控制权还给事件循环;`asyncio.run(main())` 启动事件循环跑入口协程
- gather 并发:`await asyncio.gather(t1(), t2(), t3())` 同时调度多个协程,结果**按传入顺序**返回;实测 2s+1s+1s 三个任务总耗时 ≈ **2s**(等最慢的)而不是 4s——单线程并发成立,对照 gevent 的 joinall
- 库的纪律:asyncio.sleep 是「让出式」等待,time.sleep 是**真阻塞、会卡死整个事件循环**——协程世界必须全链路用异步库(asyncio.open_connection、aiohttp 等);这正是 gevent 用猴子补丁解决、asyncio 用原生生态解决的问题
- P505「IO模型总结」核心结论(并入本点):按两阶段记——**阻塞IO** 等待+拷贝全傻等;**非阻塞IO** 等待变轮询(烧CPU)、拷贝自己来;**多路复用** select/epoll 替你等一堆 fd、拷贝自己来(以上皆同步);**异步IO** 等和拷贝都不用管、完事通知;高并发能力:阻塞(一线程一连接)< 非阻塞/多路复用(单线程多连接)< 异步(等待+拷贝都不占调用方)
- 现实建议:asyncio 适合 **IO 密集高并发**(爬虫、Web 服务、websocket),CPU 密集回到多进程;注意 async 会「传染」(调用它的也得 async),工程上常配套 aiohttp/httpx 等异步全家桶——这是 Day40~42 并发主线的终点,也是异步编程的起点

```python
import asyncio, time

async def task(name, seconds):
    print(f"{name} 开始", flush=True)
    await asyncio.sleep(seconds)      # 遇到 await 让出事件循环,切去跑别的协程
    print(f"{name} 结束", flush=True)
    return f"{name} 的结果"

async def main():
    start = time.time()
    results = await asyncio.gather(   # 单线程内并发调度 3 个协程
        task("协程甲", 2),
        task("协程乙", 1),
        task("协程丙", 1),
    )
    print("总耗时约", round(time.time() - start, 1), "秒")   # 2秒(最慢的),而非4秒
    print(results)                    # 结果按传入顺序返回

asyncio.run(main())                   # 启动事件循环跑 main

```

*asyncio.gather 单线程并发:总耗时取决于最慢任务*

---

**系列目录 / 工具获取方式见文末 👇**