---
title: 网络编程
date: 2026-11-05 09:00:00
tags:
  - Python
  - 网络
categories:
  - 网络编程
---

> 我的学习笔记,边学边记,持续修订。最后更新:2026-11。

## 📖 网络编程


### 1. 网络基础(IP、端口、子网掩码)

**网络通信三要素:**IP 定位主机、端口定位程序、协议约定数据格式**;子网掩码用来区分 IP 的网络位与主机位。**

- 局域网:交换机把多台电脑连成一个内网;广域网:路由器把不同的网连接起来,就是互联网
- IP 地址:标识网络中的一台主机,如 192.168.1.10;`127.0.0.1` 是**本机回环地址**,永远代表自己,常用于本机测试
- 端口:范围 **0~65535**,标识主机上的一个应用程序;0~1023 是知名端口(80 HTTP、443 HTTPS、3306 MySQL),自写程序避开
- 子网掩码:如 255.255.255.0,与 IP 做按位与运算,得到网络位,用来判断两台机器是否**在同一网段**
- MAC 地址:网卡的物理地址,用于局域网内定位设备;发送数据实际是 IP 找主机、MAC 找网卡、端口找程序

### 2. 网络分层模型(OSI七层与TCP/IP五层)

**OSI 分**七层**;实际教学常用 TCP/IP **五层**:物理层、数据链路层、网络层、传输层、应用层,`socket` 工作在传输层与应用层之间。**

- 物理层:传输电信号(比特流),如网线、光纤
- 数据链路层:以太网协议 + MAC 地址,负责**相邻设备**之间的数据帧传输
- 网络层:IP 协议,负责**主机到主机**的寻址和路由
- 传输层:TCP / UDP,负责**端口到端口(应用之间)**的通信
- 应用层:HTTP、FTP、SMTP 等,约定数据的内容格式
- socket 本身不是协议,是操作系统提供的**应用层与传输层之间的抽象接口**,用它就能收发数据

### 3. TCP 与 UDP 及握手挥手

****TCP 面向连接、可靠、流式**,像打电话;**UDP 无连接、不可靠、数据报**,像寄快递。三次握手建连、四次挥手断开。**

- 三次握手:客户端发 SYN → 服务端回 SYN+ACK → 客户端再回 ACK,目的是**确认双方收发能力都正常**
- 四次挥手:FIN → ACK → FIN → ACK;因为 TCP 是**双向通信**,两个方向要分别关闭,服务端收到 FIN 后可能还有数据没发完,所以 ACK 和 FIN 分开发
- TCP 可靠的机制:确认应答、超时重传、按序重组
- UDP:不用握手直接 `sendto`,速度快、开销小,但不保证送达、不保证顺序
- 场景:网页、文件传输、远程登录用 TCP;DNS 解析、视频直播、即时消息常用 UDP

### 4. socket TCP 编程流程

**服务端五步:`socket → bind → listen → accept → recv/send`,客户端两步:`socket → connect`,之后进入**通信循环**。**

- `socket.socket()` 默认参数就是 AF_INET + SOCK_STREAM,即 **TCP**;`bind(("ip", 端口))` 绑定;`listen(n)` 监听,n 是等待队列大小
- `conn, addr = server.accept()` **阻塞**等待客户端,conn 是与该客户端一对一通信的套接字,addr 是客户端地址
- 客户端用 `client.connect(("服务器IP", 端口))` 主动发起连接
- 收发的都是 **bytes**:`conn.recv(1024)` 收(参数是最多收多少字节),`conn.send(b"...")` 发,str 与 bytes 之间用 encode / decode 转换
- 客户端正常断开后,服务端 `recv` 会拿到**空 bytes(b"")**,可以据此判断下线、退出通信循环
- 两个循环要分清:**连接循环**(不断接新客户端)套在**通信循环**(和同一个客户端反复收发)外面

```python
import socket

server = socket.socket()            # 1.创建套接字
server.bind(("127.0.0.1", 8000))    # 2.绑定 IP 和端口
server.listen(5)                    # 3.监听
while True:                         # 连接循环:不断接新客户端
    conn, addr = server.accept()    # 4.阻塞等待连接
    while True:                     # 通信循环
        data = conn.recv(1024)
        if not data:
            break                   # 客户端已断开
        print(data.decode("utf-8"))
        conn.send(data.upper())     # 5.收发数据(bytes)
    conn.close()
```

*TCP 服务端模板(连接循环 + 通信循环)*

### 5. 黏包问题与 struct 自定义报头

**黏包的根源是 **TCP 流式传输 + 收发缓冲区**导致数据没有边界;解决思路:**用 struct 打包报头,先发数据长度,再发数据**。**

- 现象:连续 send 多条小数据,接收端一次 recv 可能把几条粘在一起;或一条大数据一次收不全
- 根源:①发送端——多条小数据间隔短,会被缓冲区**合并**后一起发出;②接收端——网络传输慢于 CPU 处理,数据在接收缓冲区堆积,没来得及逐条取
- UDP **不会黏包**:一次 sendto 对应一次 recvfrom,数据报有边界(但报文太长会被截断丢失)
- 解决流程:发送端 `struct.pack("i", len(data))` 打出 4 字节报头先发,再发数据;接收端先 recv 4 字节,`struct.unpack("i", head)[0]` 算出长度,再按长度精准 recv
- 经典案例:**远程执行命令**——`subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)` 执行命令,把 stdout/stderr 的结果按报头协议回传给客户端

```python
import socket, struct, subprocess

server = socket.socket()
server.bind(("127.0.0.1", 8001))
server.listen(5)
conn, addr = server.accept()
while True:
    cmd = conn.recv(1024).decode("utf-8")
    if not cmd:
        break
    res = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    out = res.stdout.read() + res.stderr.read()
    conn.send(struct.pack("i", len(out)))   # 先发 4 字节报头(数据长度)
    conn.send(out)                          # 再发真实数据

conn.close()
server.close()
```

*struct 自定义报头解决黏包(远程执行命令)*

### 6. UDP 编程与 socketserver 并发

**UDP 用 `SOCK_DGRAM` 创建套接字,收发用 `recvfrom / sendto`;`socketserver` 模块封装好服务端流程,**每个连接开一个线程**实现并发。**

- UDP 服务端:`s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)` + bind 即可,**没有 listen / accept**
- UDP 收发:`data, addr = s.recvfrom(1024)` 收到数据和对方地址,回信 `s.sendto(data, addr)`,客户端也不需要 connect
- socketserver:继承 `BaseRequestHandler` 重写 `handle(self)` 方法写业务逻辑,`ThreadingTCPServer((ip, port), 类).serve_forever()` 启动
- socketserver 里 `self.request` 相当于手写时的 conn;Threading 版本**每来一个连接就开一个线程**,互不阻塞
- 并发方案对比:多进程——稳定但开销大;多线程——共享数据、切换快;协程——单线程内切换,IO 密集场景资源最省

```python
import socketserver

class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(1024)   # self.request 相当于 conn
            if not data:
                break
            self.request.send(data.upper())

server = socketserver.ThreadingTCPServer(("127.0.0.1", 8002), MyServer)
server.serve_forever()   # 每个客户端连接分配一个线程,支持并发
```

*socketserver 实现并发服务端*

### 7. C/S 与 B/S 架构

**网络程序分 **C/S(需安装专用客户端)** 与 **B/S(浏览器即客户端)** 两大架构;B/S 本质是客户端被统一成浏览器的特殊 C/S。**

- C/S = Client/Server:客户端 + 服务端,如 QQ、微信、网游客户端;交互体验好、能调用本地资源,但每个平台都要开发安装包,升级要重新发版
- B/S = Browser/Server:浏览器就是客户端,只需开发服务端;免安装、跨平台、升级只要改服务端,但受浏览器能力限制,服务端压力更大
- B/S 并没有脱离 C/S:**浏览器本身就是一个客户端程序**,只是大家共用同一个标准客户端,它把'连谁、发什么'都交给了网址和网页
- 课程主线:socket 阶段写的是通用 C/S;后面 Web 阶段(HTML、HTTP、Django/Flask)写的都是 B/S
- 两种架构通信本质一样:请求-响应模型,数据都走完整的网络协议栈,所以 socket、TCP/UDP 的知识两边通用

### 8. 以太网、IP 与 ARP 协议:一次数据是怎么送达的

**一次跨网发送靠三层接力:**以太网协议用 MAC 管相邻设备、IP 协议管跨网段寻路、ARP 协议负责把 IP 解析成 MAC**。**

- 以太网协议:数据链路层的帧 = 头(目的 MAC + 源 MAC + 上层协议类型)+ 数据(通常装的是 IP 包)+ 尾部校验;数据部分有长度上限(MTU),超过要先在 IP 层分片
- MAC 地址是网卡的物理地址(48 位);**以太网帧只负责相邻设备之间的一跳**——每经过一个路由器,帧的源/目的 MAC 都换成这一跳的地址,交换机只按 MAC 查表转发、不改帧
- IP 协议:IP 头里最重要的是源 IP、目的 IP 和 **TTL**(每过一个路由器减 1,减到 0 就丢弃,防止数据包在网络里永远打转)
- **跨网段时 IP 地址全程不变,MAC 地址一跳一换**;同网段则直接把帧发到对方 MAC
- ARP 协议:把 IP 解析成 MAC——缓存里没有就**广播** ARP 请求('谁是 x.x.x.x,请回应'),对方**单播**回应自己的 MAC;目标是外网 IP 时,ARP 解析的是**网关**的 MAC,把包先交给路由器转发
- 完整链路串一遍:应用数据 → TCP 加端口信息 → IP 加源/目的地址 → 以太网加 MAC → 变成电信号;接收方再从下往上逐层拆包还原

### 9. TCP 报文与握手挥手的状态详解

**TCP 头核心字段:**源/目的端口、序号 seq、确认号 ack、标志位(SYN/ACK/FIN/RST)**;握手挥手的每一步对应一个状态,主动关闭方最后要等 **2MSL**。**

- TCP 报文头关键字段:源端口/目的端口(各 16 位)、seq(本次发送数据的第一个字节的编号)、ack(期望对方下一个字节的编号)、标志位 SYN(请求建连)、FIN(请求断开)、ACK(确认号有效)、RST(强制重置)
- 三次握手的状态:客户端 CLOSED →发 SYN→ **SYN_SENT** →收到 SYN+ACK 回 ACK→ **ESTABLISHED**;服务端 LISTEN →收 SYN→ **SYN_RCVD** →收 ACK→ ESTABLISHED
- 四次挥手的状态(主动方):ESTABLISHED →发 FIN→ FIN_WAIT_1 →收 ACK→ FIN_WAIT_2 →收对方 FIN 回 ACK→ **TIME_WAIT** →等 2MSL→ CLOSED;被动方:ESTABLISHED → CLOSE_WAIT →发 FIN→ LAST_ACK → CLOSED
- **TIME_WAIT 要等 2MSL(两倍报文最大生存时间)**:①保证最后一个 ACK 丢失后还能在对方重传 FIN 时补发;②让这条连接的旧报文在网络中消亡,不影响之后复用该端口的新连接
- 为什么握手三次、挥手四次:握手时服务端的 SYN+ACK 可以合并成一步发;挥手时被动方收到 FIN 后**可能还有数据没发完**,只能先 ACK,等数据发完再单独发 FIN

### 10. 半链接池与 listen 的 backlog

**`listen(n)` 的 n 就是**等待队列(俗称半链接池)的大小**:已完成握手但还没被 accept 的连接先在这里排队,排满后新客户端的连接会受影响。**

- 三次握手由操作系统内核完成:**connect 成功 ≠ 服务端已经 accept**;握手完成的连接先进队列等服务端来取,accept() 每次从队头取一个
- `listen(n)` 里的 n 限定这个等待队列的长度;服务端一直不 accept,队列堆满后,新客户端的 connect 会长时间卡住甚至被拒绝
- 验证方法:服务端 listen(2) 后不写 accept,连续开 3 个以上客户端 connect——能马上连上的最多 2 个左右,其余要等很久(不同系统的具体行为略有差异)
- 严格说 Linux 内核分**半链接队列**(收到 SYN、还没握完手,防 SYN 洪泛攻击)和**全链接队列**(握手完成、等 accept),教学里常把 listen 的等待队列统称半链接池
- 工程意义:单线程服务端处理一个客户端时,其他客户端先靠队列暂存;队列太小会拒客、太大让排队者久等——真正的并发要靠 socketserver、线程池等方案

### 11. Nagle 算法与 TCP 收发缓冲区

**TCP 为合并小包设计了 **Nagle 算法**:小数据先攒在发送缓冲区,凑够一批或收到 ACK 才发出——这是发送端黏包的直接根源;接收端缓冲区来不及取则造成接收端黏包。**

- 收发缓冲区:send 不是把数据直接甩到网络,而是先拷进内核的**发送缓冲区**;recv 也是从**接收缓冲区**里取数据——缓冲区就是黏包问题的物理载体
- Nagle 算法:一条 TCP 连接上**最多只允许一个未被确认的小分组**在途中,后续小数据会先攒在发送缓冲区,等上一个分组的 ACK 回来(或攒够一批)再一起发——用延迟换网络利用率
- 后果:两次紧挨着的 send,可能被 Nagle 合并成一次网络传输,接收端一次 recv 就把两条数据收在了一起
- 关闭 Nagle:`sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)` 可禁用 Nagle 让小包立即发出(实时性场景常用),但 TCP 流式传输**没有边界**,该黏包还是黏包,报头协议不能省
- UDP 没有这套机制:一次 sendto 就是一个独立数据报,边界清晰,所以 UDP 不黏包(但报文太长会被截断丢失)

### 12. 终极大招:struct + json 双层报头传输文件

**先用 struct 发**字典报头的长度**,再发 json 字典报头(文件名、大小、md5),最后发真实数据——三层收发顺序严格对应,理论上可以传任意大小的文件。**

- 进化:报头只含数据长度,够传字符串;要传文件还得告诉对方**文件名、文件大小、md5 校验值**——把这些信息打包成 json 字典当报头
- 发送端三步:① `struct.pack("i", len(head_bytes))` 发 4 字节报头长度;② 发字典报头(json.dumps 后 encode 的 bytes);③ 循环读文件 `f.read(4096)` 分段 send 直到发完
- 接收端三步:① 先 recv 4 字节,unpack 得到**报头长度**;② 按报头长度 recv 出 json 字典,decode + loads 拿到文件名和大小;③ 循环 recv 并拼接,直到收满 filesize 字节,写文件
- 为什么两层:报头本身也是数据,接收端必须先知道**报头多长**才能精准 recv——struct 解决报头的黏包,json 解决报头的内容描述,各司其职
- 按 filesize 循环接收是关键:recv(1024) 不保证一次收满,要 `while len(received) < filesize` 累计,收多少写多少

### 13. 阿里云服务器:把服务端部署到公网

**把 socket 服务端跑在云服务器上,**bind 0.0.0.0** 监听所有网卡,再在云平台**安全组放行端口**,本地客户端连服务器公网 IP 即可真正走互联网通信。**

- 本机自测用 127.0.0.1:数据不出网卡;要让别人连上,服务端必须跑在一台**有公网 IP 的机器**上,阿里云 ECS 等云服务器是最常用的选择
- 服务端 bind 要写 `("0.0.0.0", 端口)`:0.0.0.0 表示监听本机**所有网卡**;写 127.0.0.1 只有本机能连,写内网 IP 外网进不来
- 云平台**安全组/防火墙**默认只放行 22(ssh)等少量端口:自选端口(如 8000)要在控制台安全组里添加入方向规则,否则客户端 connect 直接超时——新手部署失败大多是这一步
- 操作流程:`ssh root@公网IP` 登录 → 用 scp / git 把代码传上去 → `python3 server.py` 运行;断开 ssh 还想继续跑,用 `nohup python3 server.py &` 或 tmux/screen
- 客户端把 connect 的地址从 127.0.0.1 换成**服务器公网 IP**,数据就真正经过互联网了;socket 代码一行不用改,只改 IP





- 覆盖范围:Day34~37 共 23 个内容小节(P421~P448),上节课复习、今日内容、答疑等行政小节不收录;每集一个知识点,summary 是该集核心结论,details 是该集的概念、原理、代码要点与坑点
- 内容主线:**Day34~35 打理论地基**(CS/BS 架构 → 五层协议 → 以太网/ip/ARP → TCP 三次握手四次挥手 → UDP → socket)→ **Day36 动手写套接字**(简单通信 → 通信循环 → 修 bug → 链接循环 → 半链接池 → UDP 版)→ **Day37 解决工程问题**(远程命令与黏包 → struct 报头 → socketserver 并发 → 部署云服务器)
- 使用方法:看视频遇到不懂的,按集数标题(如 Day36-10 链接循环)在本章搜索;代码片段都可直接复制到本机跑——**先启动服务端、再启动客户端**,本机测试地址用 127.0.0.1

### 2. Day34-06 CS与BS架构以及网络介绍

**软件架构分 **C/S(客户端/服务端)** 与 **B/S(浏览器/服务端)**,B/S 本质是特殊的 C/S;网络编程的目标就是让**不同计算机上的程序互相通信**,靠物理连接介质 + 互联网通信协议实现。**

- C/S 架构:用户要安装专门的客户端软件,如 QQ、微信、网游客户端;优点是能充分利用本地资源、性能强,缺点是每次升级都要重新下载安装、维护麻烦
- B/S 架构:浏览器充当客户端,打开网址就能用,如淘宝、知乎;优点是零安装、跨平台、升级只需更新服务端,缺点是受浏览器能力限制、交互体验弱一些
- B/S 本质上也属于 C/S:**浏览器本身就是一款客户端软件**,所以 B/S 是 C/S 的特例;现实中没有绝对的优劣,选型看业务(重交互选 C/S,广传播选 B/S)
- 两大角色:任何网络程序都分**服务端**(一直运行、被动等待别人来连)与**客户端**(主动发起连接的一方);必须先有服务端,客户端才连得上
- 网络介绍:单机上的程序谈不上通信,要让数据跨计算机流动,必须有**物理连接介质**(网线、光纤、路由器)+ **互联网通信协议**(双方都听得懂的语言),这套"介质 + 协议"就是互联网的地基

### 3. Day34-07 互联网通信协议的工作原理

**网络通信遵循 **OSI 七层(教学中常用五层)**模型:发数据自上而下**逐层加报头封装**,收数据自下而上**逐层拆包**,每层各司其职、靠协议配合。**

- 协议的本质:一整套**约定**——报文长什么样、先说什么后说什么,让不同厂商、不同系统的机器互相听得懂;一份协议数据 = **报头(元信息)+ 数据**两部分
- 五层模型(自上而下):**应用层**(产生数据,如 HTTP、自定义协议)→ **传输层**(TCP/UDP,加源端口/目标端口)→ **网络层**(IP 协议,加源/目标 IP 地址)→ **数据链路层**(以太网协议,加源/目标 MAC 地址)→ **物理层**(把数据变成电信号/光信号发出去)
- OSI 七层 = 把五层的应用层再细分成**应用层、表示层、会话层**三层;讲原理用五层足够,面试常问七层,能对上即可
- 发送方**封装**(自上而下逐层加报头,像套娃)→ 物理层传输 → 接收方**解封装**(自下而上逐层剥报头),最终拿到原始数据;每一层的报头只有对应层才看得懂、负责处理
- 分层的好处:**解耦**——每层只管自己的职责,某一层换协议不影响其他层(比如 HTTP 不关心底下走的是网线还是 WiFi),出现问题也好定位是哪一层的锅

### 4. Day34-08 以太网协议、ip协议、ARP协议

**数据链路层用**以太网协议**、靠 **MAC 地址**在局域网内**广播**传帧;网络层用 **ip 协议**划分子网、定位主机;**ARP 协议**负责"已知 ip 求 MAC"。**

- 以太网协议(数据链路层):规定一组电信号为一个**帧(frame)**,帧 = 报头 + 数据;报头里是**源 MAC、目标 MAC**(各 6 字节),MAC 地址共 48 位、网卡出厂时全球唯一
- 早期以太网靠**广播**通信:同一局域网内,帧发给所有人,不是目标 MAC 的机器收到就丢弃;广播范围一大规模就爆炸("广播风暴"),所以才需要 ip 协议来分层划片
- ip 协议(网络层):IPv4 地址 **32 位**、点分十进制表示(如 192.168.1.10);把源/目标 ip 加进数据包,全世界的网络靠它跨网段转发
- **子网掩码**判断两台机器是否同一子网:双方 ip 分别与子网掩码做**按位与**运算,结果相同 = 同网段;同一子网可以广播直达,不同子网必须交给**网关/路由器**一层层转发
- ARP 协议:已知对方 ip、求对方 MAC——在局域网内发 ARP **广播**(谁的 ip 是这个,请回话),目标机器单播回应自己的 MAC,结果会缓存起来(arp -a 可查看);跨网段时 ARP 求的是**网关**的 MAC,把帧先发给网关

### 5. Day35-03 tcp协议上

**传输层用**端口**标识一台机器上的具体程序,**ip + 端口**才能唯一定位一次通信;**TCP 面向连接、可靠传输、字节流**,是 socket 编程的主角。**

- 端口(port):0~65535 的数字,标识一台计算机上的**应用程序**;0~1024 多为知名服务保留(HTTP 80、HTTPS 443、SSH 22、FTP 21),自己写程序用大端口,且不能和本机已占用的冲突
- ip 地址找到**哪台机器**,端口找到**机器上的哪个程序**,ip + 端口合起来才能定位一次通信的两端——这就是后面 bind/connect 都要传 ("ip", 端口) 元组的原因
- TCP 三大特点:**面向连接**(通信前先握手建立连接)、**可靠**(不丢、不重、不乱序)、**流式协议**(数据像水流一样连续、没有消息边界——黏包问题的根源);另外是全双工,建立连接后双方都能随时收发
- TCP 报头关键字段:源端口、目标端口、**序号(seq)**、**确认号(ack)**、标志位(SYN/ACK/FIN 等);可靠传输正是靠"序号 + 确认应答 + 超时重传"这套机制实现的
- 与 UDP 的对比先立个框架:UDP 无连接、不可靠、数据报、支持一对多;详细对比与适用场景见 Day35-11,UDP 套接字编程见 Day36-12

### 6. Day35-04 tcp协议下

**TCP 用**三次握手**建立连接(让双方都确认彼此的收发能力),用**四次挥手**断开连接(主动方要 TIME_WAIT 等 2MSL);可靠是有代价的。**

- 三次握手:客户端发 **SYN** → 服务端回 **SYN+ACK** → 客户端再回 **ACK**,连接建立;握手过程中双方交换各自的初始序号,为后续可靠传输做铺垫
- 为什么恰好三次:一次不行(客户端单方面表态),两次不够(服务端无法确认"客户端能收到自己的消息"),四次浪费;三次刚好让**双方都确认了:自己能发能收、对方也能发能收**
- 四次挥手:主动方发 **FIN** → 对方回 **ACK**(此时对方可能还有数据没发完,所以 ACK 和 FIN 要分开,这也是为什么是四次而不是三次)→ 对方发完数据后发 **FIN** → 主动方回 **ACK**,进入 **TIME_WAIT** 状态等 2MSL 才真正关闭
- TIME_WAIT 的意义:① 最后一个 ACK 若丢失,对方重发的 FIN 还能被响应 ② 让本连接的旧报文在网络中自然消亡,避免干扰之后复用同端口的新连接
- 可靠性手段(了解):确认应答 + 超时重传、序号去重与排序、**滑动窗口**流量控制;攻击面:**SYN 洪水攻击**用大量假 SYN 占满服务端的半连接队列,让正常用户连不上(呼应 Day36-11 半链接池)

### 7. Day35-06 应用层与socket介绍

**应用层协议要由**程序开发者自己约定**(HTTP、FTP 只是前人约定好的例子);**socket 是应用层与传输层之间的抽象层**,把复杂的 TCP/IP 协议族封装成几个简单函数。**

- 物理层、数据链路层、网络层、传输层都由**操作系统内核 + 网卡硬件**替你实现了,**应用层必须开发者自己定协议**:先发什么、后发什么、数据怎么解析,完全由程序约定
- 常见应用层协议都是约定:HTTP 约定了"请求报文 = 请求头 + 空行 + 请求体",FTP 约定了文件传输指令格式;学会**自定义应用层协议**是后面解决黏包的关键(Day37-04)
- socket(套接字)= **ip + 端口**,是网络通信的"端点";socket 模块把下面几层的所有细节(组包、握手、重传、路由)全部封装,开发者只调 socket/bind/listen/accept/connect/send/recv 这几个函数
- socket 起源于 UNIX "一切皆文件"的思想:对套接字读写就像读写文件一样;套接字分**文件套接字 AF_UNIX**(同一台机器的进程间通信)与**网络套接字 AF_INET**(跨主机通信,网络编程只用它)
- 反过来想 socket 的价值:没有它,你得自己填 TCP 报头、算校验和、管确认重传;有了它,一行 connect() 底层就自动完成三次握手

### 8. Day35-11 其他协议补充

**传输层除了 TCP 还有 **UDP**(无连接、不可靠、数据报);应用层常见协议 **DNS/HTTP/HTTPS/FTP/SMTP** 各司其职,记住常用**知名端口**即可。**

- UDP 特点:**无连接**(发之前不握手,拿起就发)、**不可靠**(不确认、不重传,丢了就丢了)、**数据报协议**(一条消息一个独立包,有边界、不黏包)、效率高、支持一对多(广播/组播);适合直播、语音、DNS 查询、游戏心跳这类"快比全更重要"的场景
- DNS 协议:把域名解析成 ip 的服务,默认走 53 端口;浏览器访问网站前一般先问 DNS 拿到 ip,才能建立 TCP 连接
- 常见应用层协议与知名端口(建议记住):**HTTP 80、HTTPS 443、FTP 21、SSH 22、Telnet 23、SMTP 25(发邮件)、DNS 53**;配环境/开防火墙时天天要用
- 再了解两个:ICMP 是 ping 命令用的协议(探测主机是否可达),DHCP 用于入网时自动分配 ip 地址
- 重要性排序:TCP、UDP、HTTP 必须熟练,其余混个脸熟即可;写 Python 网络程序时,真正打交道的就是 socket 这一层,协议知识用来理解底层发生了什么

### 9. Day36-02 储备知识

**动手写套接字前必须储备四件事:**str 与 bytes 的编解码、recv(n) 的真实含义、127.0.0.1 与端口占用问题、服务端/客户端谁先启动**。**

- 网络上传输的是**字节(bytes)**:str 必须 encode("utf-8") 才能发,收到的 bytes 必须 decode("utf-8") 才能看;两端编码不一致就会乱码或报错(错误编码细节见 Day36-08)
- `recv(1024)` 的 1024 指**本次最多收 1024 个字节**,不是"必须收满";对方一次发 3000 字节,你 recv(1024) 只能拿到开头一段,剩下的还躺在接收缓冲区里(黏包问题的伏笔)
- `127.0.0.1` 是**本机回环地址**:数据不出网卡、自己发给自己,单机测试服务端 + 客户端全靠它;要局域网测试就用本机真实 ip(ipconfig/ifconfig 查看);`0.0.0.0` 表示绑定本机所有网卡(部署到服务器时用)
- 端口占用:服务端刚关就重启,可能报 **Address already in use**(旧连接还在 TIME_WAIT);解决办法是换端口,或 `server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)` 允许复用
- 启动顺序:**先启动服务端、再启动客户端**;反过来客户端 connect 时没人监听,会直接报 **ConnectionRefusedError**(拒绝连接)

### 10. Day36-03 套接字介绍

**套接字分**文件套接字(AF_UNIX)**与**网络套接字(AF_INET)**;网络套接字又分**流式 SOCK_STREAM(TCP)**与**数据报 SOCK_DGRAM(UDP)**,`socket.socket()` 默认参数就是 TCP。**

- 两个家族(第一个参数):`socket.AF_UNIX` 基于文件系统,用于**同一台机器**上进程间通信;`socket.AF_INET`(IPv4)基于网络,**写网络程序只用它**
- 两种类型(第二个参数):`SOCK_STREAM` 流式套接字 = **TCP**(可靠、字节流);`SOCK_DGRAM` 数据报套接字 = **UDP**(不可靠、有消息边界)
- `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` 的**默认参数**就是 AF_INET + SOCK_STREAM,所以 `socket.socket()` 一行创建的就是 TCP 套接字;要 UDP 得显式写 `socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`
- 服务端方法链:`bind()` 绑地址 → `listen()` 监听 → `accept()` 接连接(**返回 conn 和 addr**)→ `recv()`/`send()` 收发 → `close()` 关闭
- 客户端方法链:`connect()` 连服务端 → `send()`/`recv()` 收发 → `close()`;注意数据收发走的是 **conn**(服务端侧)/客户端自己的套接字,不是 server 本身,server 只负责"接客"

### 11. Day36-04 基于tcp协议的套接字通信流程介绍

**TCP 服务端固定五步 **socket→bind→listen→accept→recv/send**,客户端两步 **socket→connect→recv/send**;三次握手发生在 connect 与 accept 之间,由内核自动完成。**

- 服务端流程:① `socket.socket()` 买电话机 ② `bind(("127.0.0.1", 8080))` 给电话装卡(绑 ip + 端口) ③ `listen(5)` 开机等待 ④ `conn, addr = server.accept()` 拿起听筒(阻塞) ⑤ 用 conn 收发数据,完事 close
- 客户端流程:① `socket.socket()` ② `connect(("127.0.0.1", 8080))` 拨号(**此行触发三次握手**) ③ `send`/`recv` 收发 ④ `close()` 挂断
- `accept()` 返回两个值:**conn** 是与这个客户端一对一的通信套接字(以后收发都走它),**addr** 是客户端的 ("ip", 端口) 元组
- 三次握手由底层自动完成:客户端 connect 发起、服务端 accept 返回时连接已经建好;四次挥手发生在任一方 close 或连接断开时——**代码里看不见握手,但要知道它发生了**
- 两个必须知道的报错:先启动客户端 → **ConnectionRefusedError**(没人监听);服务端没 bind 端口就 listen → 客户端永远找不到你

### 12. Day36-05 基于tcp协议的简单套接字通信

**最小可跑的 TCP"一问一答"程序:服务端 socket→bind→listen→accept→recv→send,客户端 socket→connect→send→recv;先启动服务端,再启动客户端。**

- 运行顺序与效果:先跑 server.py(卡在 accept 等人),再跑 client.py,双方各收发一次就结束;这是后面一切版本的原型
- 收发的只能是 **bytes**:str 用 encode 变字节再发,bytes 用 decode 变回字符串再看;两边编码一致(这里统一 utf-8)才不会乱码
- `conn.recv(1024)` 表示最多收 1024 字节;此时程序只通信**一轮**就退出了,想持续聊天要加循环(下一节通信循环)
- 可以观察的现象:服务端 accept 之前客户端就能 connect 成功(握手由内核完成,连接在队列里排队,呼应 Day36-11 半链接池);只跑客户端 → ConnectionRefusedError
- 这个版本还不健壮:客户端中途退出,服务端要么报错要么卡住——Day36-08、09 两节专门修这些 bug

```python
# ===== 服务端 server.py =====
import socket

server = socket.socket()                 # 1.创建套接字(默认 TCP)
server.bind(("127.0.0.1", 8080))         # 2.绑定 ip 和端口
server.listen(5)                         # 3.监听(半连接池大小)
conn, addr = server.accept()             # 4.阻塞等客户端连接
data = conn.recv(1024)                   # 5.收(bytes)
print("收到客户端:", data.decode("utf-8"))
conn.send(b"hello client")               # 6.发(bytes)
conn.close()
server.close()

# ===== 客户端 client.py =====
import socket

client = socket.socket()                 # 1.创建套接字
client.connect(("127.0.0.1", 8080))      # 2.连接服务端(触发三次握手)
client.send(b"hello server")             # 3.发
data = client.recv(1024)                 # 4.收
print("收到服务端:", data.decode("utf-8"))
client.close()
```

*基于 TCP 的简单套接字通信(先启动服务端,再启动客户端)*

### 13. Day36-07 通信循环

**在 accept 之后、双方各自的收发逻辑外面套一层 **while True**,就把"一问一答"变成"持续聊天"——这就是**通信循环**。**

- 通信循环 = 与**同一个客户端**反复收发的循环,套在 `conn.recv`/`conn.send` 外面;服务端和客户端两边都要加,缺一边就"单方聊天"
- 每轮的节奏要错开:服务端 recv(等客户端说)→ send(回话),客户端 send(说话)→ recv(等回复);**不能双方同时 recv**,否则都阻塞、互相干等
- send 的必须是 bytes:`msg.encode("utf-8")`,直接 send 字符串会报 **TypeError: a bytes-like object is required**
- 此时的退出方式只有客户端 Ctrl+C 强制断开——服务端会卡死或报错,这正是下一节 bug修正 要解决的问题
- 一个客户端聊着,第二个客户端连上来也只能**排队**:accept 在通信循环外面,要等当前连接断开后才能回到 accept 接下一个(链接循环 Day36-10 才解决)

```python
# ===== 服务端(核心部分,创建/绑定/监听同上) =====
conn, addr = server.accept()             # 等客户端
while True:                              # 通信循环:和同一个客户端反复收发
    data = conn.recv(1024)               # 收客户端的话
    print("客户端说:", data.decode("utf-8"))
    msg = input("服务端说>>: ").strip()
    conn.send(msg.encode("utf-8"))

# ===== 客户端(核心部分) =====
client = socket.socket()
client.connect(("127.0.0.1", 8080))
while True:
    msg = input("客户端说>>: ").strip()
    client.send(msg.encode("utf-8"))
    data = client.recv(1024)             # 等服务端回复
    print("服务端说:", data.decode("utf-8"))
```

*通信循环:accept 之后双方各加一层 while True*

### 14. Day36-08 bug修正1

**两个高频 bug:**① 客户端发空消息 → 服务端 recv 永远收不到,双方互相等待"卡死";② 两端编码不一致 → 中文乱码或 UnicodeDecodeError**。修复:空消息不发 + 两端统一 utf-8。**

- 现象一:客户端直接回车,send 的是 **b""**,而 TCP **不发送空数据段**——服务端的 recv 收不到任何东西、继续阻塞;客户端却已经进入下一轮等服务端回复 → 双方互等,程序看起来"死机"
- 修复一:客户端发送前判空——`if not msg: continue`;经验法则:**空消息永远不要 send**,这是自己程序能避免的坑
- 现象二:客户端 `msg.encode("gbk")` 发中文,服务端 `data.decode("utf-8")` 来解 → 轻则乱码,重则抛 **UnicodeDecodeError**(gbk 一个汉字 2 字节、utf-8 一个汉字 3 字节,用错解码方案字节就对不上)
- 修复二:收发两端**约定同一种编码**,程序内部统一用 utf-8;唯一例外是 Windows 命令行的执行结果(subprocess 输出)本身是 gbk,解它才用 gbk(Day37-02 会遇到)
- 本质认识:TCP 只负责搬运字节、**不解释内容**——怎么编码、消息怎么断句(黏包)全是应用层自己的事,协议要自己定

```python
# ===== 客户端通信循环(带修复) =====
# 现象1:直接回车发空消息 → send(b'') → 服务端 recv 永远收不到,双方"卡死"
# 现象2:若这里用 gbk 编码、服务端用 utf-8 解码 → 中文乱码或 UnicodeDecodeError
while True:
    msg = input(">>: ").strip()
    if not msg:                          # 修复1:空消息不发,直接下一轮
        continue
    client.send(msg.encode("utf-8"))     # 修复2:两端统一 utf-8
    data = client.recv(1024)
    print("服务端说:", data.decode("utf-8"))
```

*bug修正1:空消息卡死与中文乱码*

### 15. Day36-09 bug修正2

**第三个 bug:客户端**断开连接**——Windows 下服务端 recv 抛 **ConnectionResetError** 直接崩掉,Linux 下 recv 永远返回空 bytes 造成死循环。修复:**判空 break + try/except**,让服务端活得下来。**

- 现象一(Windows 常见):客户端被强杀/异常退出,服务端正在 `conn.recv` 时抛出 **ConnectionResetError([WinError 10054] 远方主机强迫关闭了一个现有的连接)**,整个服务端程序崩溃
- 现象二(Linux 常见):客户端正常断开后,服务端的 recv **不再阻塞、每次都返回空 bytes b""**,代码没判断就死循环打印空行
- 关键语义:**TCP 连接被对方正常关闭时,recv 返回空 bytes b""(不报错、不阻塞)**——这是判断"对方下线了"的标准信号;异常断开才抛 ConnectionResetError
- 修复:`if not data: break` 处理正常断开;`except ConnectionResetError: break` 兜住异常断开;两者都只是**结束与这个客户端的通信循环**,服务端进程本身不崩
- 修完这版,服务端面对客户端"正常走"和"暴毙"都能从容处理,为 Day36-10 链接循环(接下一个客户端)打好基础

```python
# ===== 服务端通信循环的健壮版 =====
while True:
    try:
        data = conn.recv(1024)
        if not data:                     # 客户端正常断开:recv 返回空 bytes(Linux 常见)
            break
        print("客户端说:", data.decode("utf-8"))
        conn.send(data.upper())
    except ConnectionResetError:         # 客户端异常断开(Windows 常见)
        break                            # 只结束和这个客户端的通信,服务端不崩
conn.close()
```

*bug修正2:客户端断开的两种现象与统一修复*

### 16. Day36-10 链接循环

**把 `accept` 放进**外层 while True** 就是**链接循环**:一个客户端断开后,服务端回头接下一个;最终结构 = **链接循环(外)套通信循环(内)**。**

- 两层循环的分工:外层 while True 负责**不断 accept 新客户端**(链接循环);内层 while True 负责与当前客户端反复收发(通信循环);`conn.close()` 放在两层循环之间,只关当前连接
- 完整流转:客户端 A 连上 → 通信循环服务 A → A 断开(判空或异常 break)→ close 掉 A 的 conn → 回到 accept → 等客户端 B……服务端从此不再"服务完一个就死"
- `server` 与 `conn` 的生命周期不同:**server 创建一个就够**(整个程序期间不关),**conn 一客一个、用完即关**;打印 addr 可以看到每个客户端的上线
- 这依然是**串行**服务:同一时刻只服务一个客户端,第二个连上了也要排队等第一个断开;想同时服务多个客户端,要用多线程/多进程,Day37-06 的 socketserver 就是现成方案
- 客户端退出建议:输入 q 时主动 `client.close()` 再退出,比强杀优雅——服务端能收到空 bytes、走正常 break 分支,日志也干净

```python
import socket

server = socket.socket()
server.bind(("127.0.0.1", 8080))
server.listen(5)
while True:                              # 链接循环:不断接新客户端
    conn, addr = server.accept()
    print("新客户端上线:", addr)
    while True:                          # 通信循环:与当前客户端反复通信
        try:
            data = conn.recv(1024)
            if not data:                 # 客户端正常断开
                break
            print(addr, "说:", data.decode("utf-8"))
            conn.send(data.upper())
        except ConnectionResetError:     # 客户端异常断开
            break
    conn.close()                         # 只关当前连接,回到 accept 等下一个
server.close()
```

*链接循环(外层)套通信循环(内层)*

### 17. Day36-11 半链接池

**`listen(n)` 里的 n 是**半链接池(未处理连接的等待队列)的大小**,不是最大连接数;SYN 洪水攻击正是靠塞满半链接池让正常用户连不上。**

- 概念:客户端 connect 发起三次握手后、还没被服务端 accept 取走的连接,由**内核**放进一个等待队列;`listen(n)` 的 n 就是这个队列的容量,形象叫法"半链接池"
- 实验现象:listen(2) 时同时开很多个客户端,只有**正在 accept 处理的一个 + 队列里排队的 n 个**能 connect 成功,再多的客户端 connect 会一直卡住(连不上也拒不掉);服务端 accept 取走一个,才腾出位置给后来者
- 为什么叫"半"链接:三次握手只完成一部分(收到 SYN 还没握完)的连接叫半连接;Linux 内核实际维护半连接队列与全连接队列两段,握手完成的连接等待 accept(细节了解即可)
- SYN 洪水攻击(DoS/DDoS 经典手法):攻击者大量伪造 SYN 却不回第三次握手,半链接池被垃圾连接占满 → **正常用户再也连不进来**;所以服务暴露公网要做防护
- 写程序的经验:演示用 n = 5 就够;生产上高并发绝不能只靠调大 backlog,要靠并发模型(多线程、多进程、IO 多路复用)

### 18. Day36-12 基于udp协议的套接字通信

**UDP 套接字 = `socket(AF_INET, SOCK_DGRAM)`:**没有 listen/accept/connect**,直接 `sendto(数据, 地址)` / `recvfrom(1024)`,一条消息就是一条消息、天然不黏包。**

- 流程与 TCP 的差异:UDP **无连接**,所以服务端不需要 listen 和 accept、客户端不需要 connect;服务端 `socket(AF_INET, SOCK_DGRAM)` → `bind` → 循环 recvfrom/sendto 就能干活
- `data, addr = server.recvfrom(1024)`:UDP 每收一条消息都**自带发送方地址 addr**;回复必须指名道姓 `server.sendto(回复, addr)`,因为没有"连接"帮你记住对方是谁
- UDP 是**数据报**协议:sendto 一次 = 一条独立消息,recvfrom 一次收一条,**消息边界保留、不黏包**;但单条消息超过 recvfrom 的 n 会被**截断**(多余部分直接丢掉)
- UDP 不可靠:不握手、不确认、不重传,可能丢包、可能乱序;实验:客户端先 sendto、服务端后启动,之前那条消息不会补投——丢了就是丢了,换来的是快和轻
- 适用场景与坑:直播、语音、游戏心跳、DNS 查询;代码上 encode/decode 与 TCP 完全相同,唯一区别就是 SOCK_DGRAM 和 sendto/recvfrom;服务端**必须 bind**,否则收不到消息

```python
# ===== UDP 服务端 =====
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 数据报套接字
server.bind(("127.0.0.1", 8080))
while True:
    data, addr = server.recvfrom(1024)   # 收消息 + 对方地址
    print(addr, "说:", data.decode("utf-8"))
    server.sendto(data.upper(), addr)    # 回消息必须指定发给谁

# ===== UDP 客户端 =====
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    msg = input(">>: ").strip()
    if not msg:
        continue
    client.sendto(msg.encode("utf-8"), ("127.0.0.1", 8080))  # 无需 connect
    data, addr = client.recvfrom(1024)
    print("服务端说:", data.decode("utf-8"))
```

*基于 UDP 协议的套接字通信(无连接,sendto/recvfrom)*

### 19. Day37-02 远程执行命令程序与粘包问题介绍

**用 **subprocess** 执行客户端发来的命令并回传结果,就是一个远程执行命令程序;但结果超过 recv(1024) 会**收不全**,先发长度再发数据又会**黏包**——两个坑都源于 TCP 字节流没有边界。**

- 服务端思路:recv 拿到命令字符串 → `subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)` 执行 → `obj.stdout.read() + obj.stderr.read()` 把正确输出和报错都拿到 → send 回客户端
- 编码细节:Windows 下命令结果的编码是 **gbk**,客户端要 `data.decode("gbk")` 才不乱码/不报错;自己程序里写的消息仍然统一 utf-8,两者别搞混
- 坑一(收不全):执行 `dir /s` 这类命令,结果可能有几万字节,一次 `recv(1024)` 只拿到开头一截,**剩余字节还躺在接收缓冲区里**;下一条命令一发,recv 先收到的是上次的残留 → 结果串台
- 坑二(黏包):服务端先 send 长度、紧接着 send 结果,两条小数据间隔极短,TCP 会把它们**合成一段**发出去,客户端一次 recv 收到"长度和结果黏在一起"的数据,没法解析
- 结论与出路:根源 = **TCP 是字节流、没有消息边界** + 接收方不知道该收多少字节;解决思路 = 收发双方约定"先说长度、再发数据",下一节开始实现

```python
# ===== 服务端 =====
import socket, subprocess

server = socket.socket()
server.bind(("127.0.0.1", 8080))
server.listen(5)
conn, addr = server.accept()
while True:
    cmd = conn.recv(1024).decode("utf-8")
    if not cmd:
        break
    obj = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = obj.stdout.read() + obj.stderr.read()   # 正确输出 + 错误输出
    conn.send(res)

# ===== 客户端 =====
import socket

client = socket.socket()
client.connect(("127.0.0.1", 8080))
while True:
    cmd = input("请输入命令>>: ").strip()
    if not cmd:
        continue
    client.send(cmd.encode("utf-8"))
    data = client.recv(1024)             # 坑:结果超过 1024 只收到一小部分
    print(data.decode("gbk"))            # Windows 命令结果是 gbk 编码
```

*远程执行命令(存在收不全与黏包问题的原始版)*

### 20. Day37-03 tcp协议nagle算法介绍与udp介绍

**黏包的两大成因:**发送端 Nagle 算法攒小包**、**接收端不及时取导致数据在缓冲区堆叠**,本质都是 TCP 字节流不保留消息边界;UDP 是数据报协议,**永不黏包**(但会丢包)。**

- Nagle 算法:为提高网络利用率,TCP 发送端会把**多个小的发送请求攒成一个大包**再发(等上一包被确认或攒够一定量);于是连续 send 三次小数据,对方可能一次 recv 就全收到了
- 接收端视角:应用层没及时 recv,数据先堆在**接收缓冲区**;`recv(n)` 只是从缓冲区搬走 n 个字节,**不区分这些字节来自几次 send**——两次 send 一次 recv,自然黏成一条
- 所以黏包只发生在 **TCP(流式协议)**上:它保证字节按序到达,但**不保留 send 的次数和边界**;两条消息是分开收到还是黏着收到,取决于缓冲区状态,行为不稳定、必须靠协议解决
- UDP 不黏包:每条消息独立打包、有明确边界,recvfrom 一次收一条,发几次收几次;代价是不可靠(丢包不补)且单个数据报不能太大(理论上限 64KB,实践要远小于此)
- 顺着想就明白:解决黏包 = **应用层自己造边界**(先收长度、再按长度收),而不是去关 Nagle——就算关了,接收缓冲区照样能把两次 send 的数据黏在一起

### 21. Day37-04 自定义协议解决粘包问题

**自定义应用层协议解黏包:发送方**先发数据长度**(并等对方确认),接收方**先收长度、再循环收够指定字节数**;长度已知,字节流就被切出了边界。**

- 协议内容(双方约定好就行):第一条消息 = 真实数据的**长度**(字符串形式),第二条消息 = 真实数据;接收方收到长度后回一个确认(如 b"ready"),把两次 send 隔开,避免"长度"和"数据"黏在一起
- 接收方必须**循环收**:`while len(res) < data_len: res += client.recv(1024)`——大数据一次 recv 收不完,必须收够指定字节数为止;这是解决"收不全"的关键动作
- 这就是**应用层自定义协议**:TCP 只管搬字节,"消息怎么切分"由我们自己约定;HTTP 报文头里的 Content-Length 就是同一个思路的工业版
- 局限:长度用 str 发送本身仍是变长数据,靠确认应答隔开不够优雅;更标准的做法是用 **struct 把长度打成固定 4 字节**(下一节终极大招)
- 修复验证:再执行 dir /s 这类大结果命令,能完整收全;连续执行多条命令也不会串台、不会把上一条的残留当新结果

```python
# ===== 服务端 =====
res = obj.stdout.read() + obj.stderr.read()      # 命令结果(bytes)
conn.send(str(len(res)).encode("utf-8"))         # 1.先发数据长度
conn.recv(1024)                                  # 2.等客户端确认,隔开两次 send
conn.send(res)                                   # 3.再发真实数据

# ===== 客户端 =====
data_len = int(client.recv(1024).decode("utf-8"))  # 1.先收长度
client.send(b"ready")                              # 2.回确认
res = b""
while len(res) < data_len:                         # 3.循环收,直到收够
    res += client.recv(1024)
print(res.decode("gbk"))
```

*自定义协议:先发长度,再循环收数据*

### 22. Day37-05 解决粘包问题终极大招

**终极大招 = **struct 固定 4 字节报头 + json 报头**:先发 4 字节的"报头长度",再发 json 报头(描述数据元信息),最后发真实数据;三段式收发,任意大的数据都能完整收。**

- 三步发送:① `struct.pack("i", len(head_json))` 把报头长度压成**固定 4 字节**(变长问题变定长) ② 发报头 `head_json = json.dumps({...}).encode()` ③ 发真实数据
- 三步接收:① `recv(4)` 收定长报头,`struct.unpack("i", ...)[0]` 解出报头长度——固定收 4 字节,这一步永远不黏不缺 ② 按长度收报头、`json.loads` 解析(报头很小,一次 recv 即可收全) ③ 按报头里的 size **循环收**真实数据直到收够
- 报头里放什么自己定:数据大小 size、命令/文件名、md5 校验值……json 能描述任意结构,比"只发一个数字的长度"灵活得多;struct 的 "i" 表示 4 字节整数
- 完整演示:用三段式改造远程执行命令程序,任意长度的命令结果都能一次收全、不串台;同样的套路直接套在**文件传输**上——先收报头拿到文件名和大小,再循环把字节写进文件
- 精髓一句话:**定长的部分先收**(4 字节报头长度),**不定长的部分靠报头里的 size 循环收**——记住这句,黏包问题通杀

```python
import socket, struct, json, subprocess

# ===== 服务端(发送方) =====
obj = subprocess.Popen(cmd, shell=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
res = obj.stdout.read() + obj.stderr.read()
head_dic = {"cmd": cmd, "size": len(res)}            # 报头:描述真实数据
head_json = json.dumps(head_dic).encode("utf-8")
conn.send(struct.pack("i", len(head_json)))          # ① 4 字节定长:报头长度
conn.send(head_json)                                 # ② 报头(json)
conn.send(res)                                       # ③ 真实数据

# ===== 客户端(接收方) =====
head_len = struct.unpack("i", client.recv(4))[0]     # ① 先收固定 4 字节
head_dic = json.loads(client.recv(head_len).decode("utf-8"))  # ② 再收报头
total, res = head_dic["size"], b""
while len(res) < total:                              # ③ 按 size 循环收真实数据
    res += client.recv(1024)
print(res.decode("gbk"))
```

*struct + json 三段式:黏包终极解决方案*

### 23. Day37-06 socketserver模块

**socketserver 把"链接循环 + 并发"封装好了:自定义类继承 **BaseRequestHandler**、服务逻辑写进 **handle** 方法,用 **ThreadingTCPServer** 起服务——一个客户端一个线程,serve_forever() 常驻。**

- 三步用法:① 写类继承 `socketserver.BaseRequestHandler`,把服务逻辑写进 **handle(self)**:其中 `self.request` 相当于 conn、`self.client_address` 相当于 addr ② `ThreadingTCPServer(("127.0.0.1", 8080), MyHandler)` 实例化 ③ `s.serve_forever()` 无限循环接客
- 并发与串行:`TCPServer` 是**串行**的,同一时刻只服务一个客户端;`ThreadingTCPServer` 为**每个客户端开一个线程**并发处理,客户端代码完全不用改
- handle 里该有的还是要有:通信循环、判空 break、try/except ConnectionResetError——前面修的 bug 一个不少;socketserver 只帮你管"接入 + 并发",**不管"怎么聊"**
- 原理:serve_forever 内部就是帮你做了 accept 的链接循环,每来一个连接就起一个线程去调 handle;本质 = 链接循环 + 多线程的封装,Day36 手写的两层循环就是它的"手搓版"
- 改造实战:把远程执行命令程序的服务端换成 socketserver 后,多个客户端可以同时连上、各跑各的命令互不干扰;课程先手写再引库,正是为了看清它替你封装掉了什么

```python
import socketserver

class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):                        # self.request 相当于 conn
        while True:
            try:
                data = self.request.recv(1024)
                if not data:                 # 客户端正常断开
                    break
                print(self.client_address, "说:", data.decode("utf-8"))
                self.request.send(data.upper())
            except ConnectionResetError:     # 客户端异常断开
                break

if __name__ == "__main__":
    # s = socketserver.TCPServer(("127.0.0.1", 8080), MyHandler)          # 串行版
    s = socketserver.ThreadingTCPServer(("127.0.0.1", 8080), MyHandler)  # 并发版
    s.serve_forever()                        # 一个客户端一个线程
```

*socketserver 并发服务端(客户端代码与之前完全相同)*

### 24. Day37-07 阿里云服务器的使用

**把 socket 程序部署到阿里云 ECS:**买服务器 → 安全组放行端口 → ssh 远程登录 → 服务端 bind("0.0.0.0", 端口)**,客户端连公网 ip,全世界就都能访问你的程序了。**

- 云服务器是什么:机房里一台 24 小时开机的 Linux 虚拟机(阿里云叫 ECS);购买时选操作系统(如 CentOS/Ubuntu),拿到**公网 ip** 和 root 密码,从此程序不再依赖你自己的电脑开机
- **安全组**是云平台层面的防火墙:想让人连 8080 端口,必须先在控制台的**安全组里添加入方向规则放行该端口**——初学者部署后"连不上/一直超时",十有八九是忘开安全组
- 远程操作:Windows 用 xshell 或自带的 ssh 命令登录(`ssh root@公网ip`),把 server.py 上传到服务器,`python3 server.py` 跑起来;常用 Linux 命令(cd/ls/vim 等)这一集会顺带演示
- 关键一行:服务端要 `bind(("0.0.0.0", 8080))`,表示监听本机**所有网卡**;如果 bind("127.0.0.1"),只有服务器自己能连,公网永远访问不通
- 客户端只需把连接地址换成 `("公网ip", 8080)`;这就是"部署上线"的最小体验——流程和后面 Web 阶段上线 Django 项目完全同理

---
