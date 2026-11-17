---
title: MySQL 数据库
date: 2026-11-09 09:00:00
tags:
  - MySQL
  - 数据库
categories:
  - 数据库
---

> 我的学习笔记,边学边记,持续修订。最后更新:2026-11。

## 📖 MySQL基础与进阶


### 1. 库表操作与常用数据类型

**用 `create/drop/alter` 管理库和表;字符串**定长用 char、变长用 varchar**,区别是空间和速度的取舍。**

- 库操作:`create database db1 charset utf8mb4;`、`drop database db1;`、`show databases;`、`use db1;`
- 表操作:`create table t(id int, name varchar(16));`、`drop table t;`、`show tables;`、`desc t;` 查看表结构
- 改表:`alter table t add 列名 类型;` 加列、`alter table t drop 列名;` 删列、`alter table t modify 列名 新类型;` 改类型
- 常用类型:`int`/`bigint` 整数、`float`/`double` 小数、`datetime` 日期时间、`enum('男','女')` 枚举单选
- **varchar 与 char**:char(10) 定长,不足 10 个字符用空格补齐,存取快但费空间;varchar(10) 变长,按实际长度存,省空间、稍慢;括号里的 n 都是**字符数**不是字节数

```sql
create database school charset utf8mb4;
create table student(
    id int primary key auto_increment,
    name varchar(16),
    gender enum('男','女'),
    birthday datetime
);
alter table student add age int;
desc student;
```

*建库建表与修改表结构*

### 2. 约束与外键级联

**约束限制列的取值:**primary key 唯一且非空**、`auto_increment` 自增、`foreign key` 建立表间关系并可级联更新删除。**

- `primary key` 主键:唯一 + 非空,一张表只能有一个,常和 `auto_increment`(自增)搭配使用
- `not null` 非空、`unique` 唯一(允许 NULL)、`default 值` 默认值,建表时写在字段类型后面
- `foreign key(从表列) references 主表(列)`:从表该列的值必须能在主表里找到,否则插入报错
- 级联:`on update cascade` 主表更新、从表跟着更新;`on delete cascade` 主表删除、从表对应行**一起删除**(会连带删数据,慎用)
- 表关系:一对多在“多”的一方建外键;多对多建一张中间表,拆成两个一对多

```sql
create table dept(
    id int primary key auto_increment,
    name varchar(16) not null unique
);
create table emp(
    id int primary key auto_increment,
    name varchar(16) not null,
    salary int default 0,
    dept_id int,
    foreign key(dept_id) references dept(id)
    on update cascade on delete cascade
);
```

*外键与级联更新删除*

### 3. 增删改查与查询执行顺序

**增删改记牢 `insert/update/delete`;select 的关键字按 **from → where → group by → having → select → distinct → order by → limit** 的顺序执行。**

- 增:`insert into t(列1,列2) values(值1,值2),(值1,值2);` 一次可以插多行
- 改/删:`update t set 列=值 where 条件;`、`delete from t where 条件;`——**不写 where 会波及全表**,动手前先想清楚
- 执行顺序:**from → where → group by → having → select → distinct → order by → limit**;where 在分组前执行,所以 where 里不能用聚合函数,也不能用 select 起的别名
- 聚合函数:`count(*)` 数行数、`count(列)` 不统计该列为 NULL 的行,还有 `sum/avg/max/min`
- `group by` 分组后,select 里只能出现**分组字段和聚合函数**;过滤组要用 `having`(where 过滤的是行)
- `distinct` 去重、`order by 列 desc/asc` 排序、`limit 5` 取前 5 条、`limit 5,5` 跳过 5 条再取 5 条(分页)

```sql
select gender, count(*) as cnt, avg(salary) as avg_sal
from emp
where salary > 1000      -- 分组前过滤行
group by gender
having count(*) >= 2     -- 分组后过滤组
order by cnt desc        -- 排序(可以用别名)
limit 2;                 -- 只取前 2 条
```

*分组聚合完整示例*

### 4. 多表连接与子查询

****inner join 只留两表都匹配的行,left join 保留左表全部**;右表匹配不上的列补 NULL;子查询把一条 select 的结果当条件用。**

- 不带连接条件的多表查询是**笛卡尔积**(两表行数相乘),连表必须写 `on` 连接条件
- `inner join ... on`:只有两表都匹配上的行才保留
- `left join ... on`:左表全部保留,右表匹配不上的位置补 **NULL**;`right join` 与之相反
- 经典题:找没有部门的员工 → `select e.* from emp e left join dept d on e.dept_id=d.id where d.id is null;`
- 子查询:内层 select 的结果给外层当条件,如 `where dept_id in (select id from dept where name='技术部')`

```sql
select e.name as emp_name, d.name as dept_name
from emp as e
left join dept as d on e.dept_id = d.id;
-- 左表 emp 全部保留,没有部门的员工 dept_name 显示 NULL
```

*left join 连表示例*

### 5. pymysql 与事务

**pymysql 增删改后**必须 `conn.commit()`** 才生效;查询参数用 **`%s` 占位传参**防 SQL 注入;事务靠 `commit / rollback` 控制。**

- 连接:`pymysql.connect(host=..., port=3306, user=..., password=..., database=..., charset='utf8mb4')`,记得指定编码
- `cursor = conn.cursor()`,`cursor.execute(sql, 参数)` 返回受影响行数;`fetchone()` 取一条、`fetchall()` 取全部(元组套元组)、`fetchmany(n)` 取 n 条
- **SQL 注入**:把用户输入直接拼进 SQL,可被 `' or 1=1 --` 之类的输入绕过登录;正确做法是 `execute(sql, [参数])` 传参,pymysql 会自动转义
- 增删改必须 `conn.commit()` 才真正写入(pymysql 默认开启事务);查询语句不需要 commit
- 事务 **ACID**:原子性(要么全成功要么全失败)、一致性、隔离性、持久性;`conn.rollback()` 可以撤销尚未提交的修改

```python
import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306,
                       user="root", password="123456",
                       database="school", charset="utf8mb4")
cursor = conn.cursor()

# ✅ 参数化传参,pymysql 会转义,防 SQL 注入
name = "' or 1=1 --"
cursor.execute("select * from user where name=%s and pwd=%s", [name, "123"])
print(cursor.fetchall())

# ❌ 危险写法:把用户输入直接拼进 SQL
# sql = "select * from user where name='%s' and pwd='%s'" % (name, pwd)

# 增删改必须 commit 才真正写入
cursor.execute("update user set age=%s where id=%s", [20, 1])
conn.commit()
cursor.close()
conn.close()
```

*pymysql 参数化与提交*

### 6. 索引:原理、最左前缀与失效

**索引是**用空间换时间**的有序数据结构,InnoDB 用 **B+树**;联合索引遵循**最左前缀原则**,对列做运算、`like '%x'` 会让索引失效。**

- 常见索引:主键索引(建表自带)、唯一索引、普通索引、联合索引(多列合建)
- `create index idx_name on emp(name);` 建索引、`show index from emp;` 查看已有索引
- **B+树**:非叶子节点只存索引,数据全部在叶子节点且叶子节点之间有链表相连;树很矮,磁盘 IO 次数少,所以查询快
- **最左前缀原则**:联合索引 (a,b,c) 必须从 a 开始连续命中才走索引:`where a=1 and b=2` ✅,`where b=2` ❌
- 索引失效场景:对索引列做**运算或函数**(`where id+1=10`)、like **以 % 开头**(`like '%x'`)、**类型不匹配**(字符串列传数字)等
- 索引不是越多越好:占磁盘空间,而且每次增删改都要维护索引,写入会变慢

```sql
create index idx_salary on emp(salary);
create unique index idx_name on emp(name);
create index idx_name_salary on emp(name, salary);  -- 联合索引

-- ✅ 从最左列 name 开始,能走索引
select * from emp where name='alex' and salary > 3000;
-- ❌ 对列做运算,失效
select * from emp where salary + 1 > 3000;
-- ❌ like 以 % 开头,失效
select * from emp where name like '%x';
```

*索引创建与失效场景*

### 7. 存储引擎:InnoDB 与 MyISAM

**存储引擎决定表的存取方式:**InnoDB 支持事务、行级锁、外键,5.5 起是默认引擎;MyISAM 不支持事务、只有表级锁**,胜在读快、文件小。**

- 存储引擎是'表数据的存取实现',建表时按表指定:`create table t(id int) engine=InnoDB;`;`show engines;` 查看全部;**MySQL 5.5 起默认 InnoDB**
- InnoDB:支持**事务**、**行级锁**(并发写不互相挡)、外键,崩溃后可恢复,适合订单、账户等核心表;5.x 下一张表对应 .frm(表结构)+ .ibd(数据+索引)两个文件
- MyISAM:不支持事务和外键,只到**表级锁**(一人写、全表等),但结构简单、纯读速度快,适合读多写少的场景;一张表对应 .frm(结构)/.MYD(数据)/.MYI(索引)三个文件
- `show create table t\G` 能看到表的引擎和字符集;`alter table t engine=MyISAM;` 可以切换引擎(会重建表,大表慎用)
- 一句话选型:要事务、要高并发写 → InnoDB;纯读、兼容老系统 → MyISAM;新项目无脑 InnoDB

```sql
show engines;                          -- 查看支持的存储引擎
create table t1(id int) engine=InnoDB; -- 默认:事务/行锁/外键
create table t2(id int) engine=MyISAM; -- 无事务:表级锁
show create table t1;                  -- 查看引擎与字符集
alter table t2 engine=InnoDB;          -- 修改存储引擎
```

*存储引擎的查看与指定*

### 8. 建表完整语法与字段类型详解

**建表语法 `create table 表名(字段 类型[(宽度)] 约束,...) charset=xx engine=xx;`——**整型宽度只管显示、金额用 decimal、常用 datetime、enum 单选 set 多选**。**

- 完整语法:`create table 表名(字段名 类型[(宽度)] [约束...], ...) charset=utf8mb4 engine=InnoDB;`;宽度可省略,约束可以叠加多个
- 整型(tinyint/int/bigint):**宽度只是显示宽度**,配合 zerofill 不足位左补 0,不影响能存的数值范围;`unsigned` 无符号、范围翻倍(tinyint:-128~127 → 0~255)
- 浮点:float/double 是近似值、有精度误差;**decimal(m,d) 是定点小数**(m 总位数、d 小数位)没有误差,**金额字段必用**,如 decimal(8,2)
- 日期时间:date 只有日期、time 只有时间、**datetime 年月日时分秒(范围到 9999 年,最常用)**;timestamp 也带时间但受时区影响、上限 2038 年
- 枚举与集合:`enum('男','女')` **单选**,只能取列表中的值;`set('唱','跳','rap')` **多选**,存 '唱,rap' 这样的逗号组合
- 严格模式:5.7+ 默认开启,插入超长字符串、超范围数字、非法枚举值会**直接报错**;非严格模式则悄悄截断或改成最接近的值、埋下脏数据;`show variables like '%sql_mode%';` 查看

```sql
create table t(
    id int unsigned auto_increment primary key,
    sno int(6) zerofill,             -- 显示宽度:42 存成 000042
    price decimal(8,2) not null,     -- 金额:定点无误差
    birth date,                      -- 只有日期
    login_at datetime,               -- 年月日时分秒
    gender enum('男','女') default '男',
    hobbies set('篮球','足球','音乐')   -- 多选:'篮球,音乐'
) charset=utf8mb4 engine=InnoDB;
```

*建表完整语法与类型综合示例*

### 9. 修改表进阶与复制表

**改表:`rename` 改表名、`change` 改列名、`add ... after/first` 控制位置;复制表:**`like` 只复制结构(含主键索引)、`select *` 连数据复制但不带主键索引**。**

- 改表名:`alter table t rename to t2;`;改列名要带新类型:`alter table t change 旧名 新名 类型;`——**change 改名,modify 只改类型不改名**
- 控制新列位置:`alter table t add age int after name;` 加在 name 后面,`add age int first;` 放到第一列
- 复制结构:`create table t2 like t;` 得到一张**空表**,但字段类型、主键、索引、自增等完整结构都会复制过来
- 复制数据:`create table t2 as select * from t;` **连数据一起复制**,但只有字段和默认值,**主键、索引不会带过去**
- 实用组合:想'结构+数据'都要,先 `like` 建出结构,再 `insert into t2 select * from t;` 灌数据

```sql
alter table stu rename to student;                -- 改表名
alter table student change name sname varchar(16); -- 改列名
alter table student add tel char(11) after sname;  -- 指定新列位置

create table stu_bak like student;                 -- 只复制结构(空表)
create table stu_copy as select * from student;    -- 结构+数据,但无主键索引
insert into stu_bak select * from student;         -- 往空结构里灌数据
```

*修改表与两种复制方式*

### 10. SQL 查询练习思路:拆题五步法

**复杂查询别硬写,按 **'选表 → 过滤 → 分组聚合 → 连接/子查询 → 排序分页'** 拆步骤;先想清楚结果长什么样,再倒推 SQL。**

- 第 1 步选表:结果里需要的字段涉及哪几张表;第 2 步过滤:哪些行不要(写 where)——最好先在纸上画出'最终结果有几列、大概几行'
- 题干出现'每个/各/按…统计'→ 一定 group by;出现'最高/平均/总数'→ 用聚合函数;对'组'再筛选(如人数超过 2 的组)→ 用 having
- 涉及两张表 → 选 join 类型:两表都要有效用 inner;要保留某一方全量(典型:找'没有xx'的记录)用 left join + `where 右表.列 is null`
- 连表还是子查询:**结果要展示另一张表的列 → 连表;只用另一张表的值当条件 → 子查询**
- 收尾三件套:distinct 去重、order by 排序、limit 分页;写完按执行顺序自检:from → where → group by → having → select → order by → limit
- 验算技巧:拿一两个具体值代入走一遍(如'假如 gender=男'),看每一步结果对不对;复杂题先把内层子查询单独跑通,再套外层

### 11. 数据库由来、重要概念与 MySQL 安装管理

**文件存数据的种种不便催生了**数据库管理系统**;MySQL 是 **C/S 架构**——先启动服务端 mysqld,再用客户端 mysql 命令连接;忘记密码可以用 `--skip-grant-tables` 跳过授权表免密进入后重置。**

- 为什么需要数据库:全用文件保存数据的弊端——路径不统一、格式五花八门、多程序同时读写容易冲突也不安全,于是出现了统一管理数据的数据库管理系统(DBMS)
- SQL(结构化查询语言)是操作关系型数据库的**通用语言**,MySQL、Oracle 等都遵循它;MySQL 采用 C/S 架构:服务端 **mysqld** 真正管理数据,客户端 **mysql** 负责发指令
- 重要概念对照:database(库)≈ 文件夹、table(表)≈ Excel 文件、row(记录)≈ 一行数据、column(字段)≈ 一列;库下建表、表里存记录
- 连接服务端:`mysql -h 127.0.0.1 -P 3306 -u root -p`(本机可省略 -h;引号里的密码回车后再输入)
- Windows 服务化:把 bin 目录加入环境变量后,`mysqld --install` 注册系统服务、`net start mysql` 启动、`net stop mysql` 停止,不必每次手动跑 mysqld
- 修改密码:知道旧密码时用 `set password = password('新密码');`(8.0 用 `alter user 'root'@'localhost' identified by '新密码';`)
- **忘记密码**:先以 `mysqld --skip-grant-tables` 启动(跳过授权表、免密),连上后 update mysql.user 表重置密码,再 `flush privileges;` 生效
- 配置文件 my.ini(Windows)/ my.cnf(Linux):`[mysqld]` 下是服务端配置、`[client]` 下是客户端配置,常用来统一字符集(如 utf8mb4),改完要重启服务端才生效

```sql
-- 忘记 root 密码:先 mysqld --skip-grant-tables 启动服务端,免密登录后执行
-- MySQL 5.7 写法(5.6 的字段名是 password,8.0 用 alter user)
update mysql.user set authentication_string=password('newpwd123')
where user='root';
flush privileges;   -- 刷新授权,让新密码立即生效
```

*跳过授权表重置密码*

### 12. where 进阶:正则匹配 regexp

**MySQL 支持 `where 列 regexp '模式'` 做正则匹配:`^` 开头、`$` 结尾、`.` 任意一个字符、`[abc]` 取其一;比 like 的 % _ 更灵活。**

- `where name regexp '^a'`:匹配以 a 开头的值;like 'a%' 也能做前后缀,但复杂模式(开头+中间+结尾组合)用 regexp 更直观
- 常用符号:`^` 开头、`$` 结尾、`.` 任意一个字符、`[abc]` 之中的一个、`[a-z]` 范围、`*` 前面的字符出现 0 次或多次、`|` 或
- `select 'alex' regexp '^a';` 直接返回 1(匹配)/0(不匹配),写业务 SQL 前可以先用 select 验证模式
- regexp 默认**不区分大小写**,要区分大小写写成 `regexp binary '^A'`
- 选型记忆:简单包含/前后缀用 like(`'%x%'`),有结构规则的匹配(如'以 a 开头以 n 结尾')用 regexp

```sql
select 'alex' regexp '^a';          -- 1:以 a 开头
select 'alex' regexp '^(a|b)';      -- 1:以 a 或 b 开头
select 'alex' regexp '^a.l$';       -- 0:模式只匹配 3 个字符,alex 是 4 个

select * from emp where name regexp '^a.*n$';  -- 以 a 开头、n 结尾的员工
select * from emp where name like '%x%';       -- 等价的简单写法:包含 x
```

*regexp 正则匹配示例*

### 13. navicat:数据库图形化管理工具

**navicat 是最常用的 MySQL 图形化客户端:建连接后**点鼠标就能建库建表改数据**,还能可视化写查询、导出/导入 SQL 文件;学习阶段建议先手写 SQL,再用工具核对。**

- navicat 是跨平台的数据库图形化客户端(收费软件,同类还有免费的 heidiSQL、datagrip 等);本质和命令行敲 mysql 一样,都是把 SQL 发给服务端执行
- 新建连接:填主机(本机 127.0.0.1)、端口 3306、用户名 root 和密码,连上后左侧能看到服务器上所有的库
- 常用操作:右键库 → 新建表/设计表(可视化改字段、加索引,背后生成的就是 create/alter 语句)、双击表直接编辑行数据、新建查询窗口写 SQL 执行
- 「转储 SQL 文件」把库/表的结构和数据导出成 .sql 文件(可当备份、发给别人);「运行 SQL 文件」把别人给的 .sql 导入到自己的库里
- 设计表界面看到的对象 DDL(反引号包字段名、AUTO_INCREMENT、ENGINE=InnoDB 等)就是 show create table 的内容,看懂它对理解建表语法很有帮助
- 提醒:图形工具是为了提效,学习阶段要先把 SQL 手写熟练,别养成只会点鼠标的习惯

```sql
-- navicat「对象定义/DDL」里看到的,就是这类标准建表语句(show create table emp 的输出)
-- CREATE TABLE `emp` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `name` varchar(16) DEFAULT NULL,
--   `dept_id` int(11) DEFAULT NULL,
--   PRIMARY KEY (`id`),
--   CONSTRAINT `emp_dept` FOREIGN KEY (dept_id) REFERENCES `dept` (id)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
show create table emp;
```

*navicat 里看到的表 DDL*

### 14. 视图、触发器、存储过程、函数与流程控制

**视图是**复用查询的虚拟表**、触发器是对表做增删改时**自动执行**的钩子、存储过程把一段 SQL **封装起来用 call 调用**、流程控制(if/while)写在它们的 begin...end 里;实际开发中这些常被程序代码替代,但要能讲清概念和写法。**

- 视图:`create view 视图名 as select ...;` 把一条常用查询存成虚拟表,之后 `select * from 视图名` 直接查;真实数据仍在原表,**改视图里的数据就是改原表**;用途是复用与简化 SQL,但视图多了难维护,开发中不建议大量创建
- 触发器:`create trigger 名 trigger时机( before/after 增/删/改 ) on 表 for each row begin ... end`;触发时机如 after insert(插入之后自动执行);`new.列` 引用新值、`old.列` 引用旧值,适合自动记日志;缺点是逻辑藏在数据库里、不好排查,实际项目用得少
- 存储过程:`create procedure 名(in 参数 类型) begin ... end`,用 `call 名(实参)` 调用,相当于'存在数据库里的函数';参数分 in(传入)/ out(传出)/ inout;好处是 SQL 复用、少网络往返,现在更多把这类逻辑写在程序/ORM 里
- 函数:内置函数在 select 里直接用——`now()` 当前时间、`date_format(now(), '%Y-%m-%d')` 格式化日期、`concat(a,b)` 拼接字符串、`char_length()` 字符数与 `length()` 字节数;也可以自定义函数
- 流程控制:`if 条件 then ... else ... end if`、`while ... do ... end while`、`repeat/loop` 等,写在存储过程、函数、触发器的 begin...end 内部使用

```sql
-- 视图:把常用查询存成虚拟表
create view v_emp_dept as
select e.name as emp_name, d.name as dept_name
from emp as e left join dept as d on e.dept_id = d.id;
select * from v_emp_dept;

-- 触发器:往 emp 插入数据后,自动往日志表记一条
delimiter //
create trigger tri_emp_log after insert on emp
for each row
begin
    insert into emp_log(emp_id, action, at_time)
    values (new.id, 'insert', now());
end//
delimiter ;

-- 存储过程:封装一段 SQL,call 调用
delimiter //
create procedure p_top_emp(in n int)
begin
    select name, salary from emp order by salary desc limit n;
end//
delimiter ;
call p_top_emp(3);
```

*视图/触发器/存储过程示例*

## 📖 Redis 与 MongoDB


### 1. Redis 简介:为什么快
**Redis 是基于**内存**的 key-value 数据库,**单线程**执行命令,读写极快,最常用来做**缓存**。**

- Redis 是**内存数据库**,数据以 key-value 形式存储,最常用作缓存,也做计数器、排行榜等
- **单线程**执行命令(6.0 后网络 IO 部分多线程,但命令执行仍是单线程),没有线程切换和锁竞争的开销
- 为什么快:**纯内存操作** + 单线程无锁竞争 + IO 多路复用 + 高效的数据结构
- 基础命令:`set name alex`、`get name`、`del name`;`keys *` 会遍历所有键,键多时会阻塞,生产环境慎用
- 默认 16 个库(db0~db15),`select 0` 切换;value 有五大类型(见下一知识点)

### 2. 五大类型与常用命令
**value 的五大类型:**string、hash、list、set、zset**;命令前缀有规律——h 开头是 hash,l 开头是 list,s 开头是 set,z 开头是 zset。**

- **string**:最基础的类型,`set`/`get`,`incr` 自增(做计数器)、`decr` 自减
- **hash**:一个 key 存多个字段,像对象:`hset user:1 name alex`、`hget user:1 name`、`hgetall user:1`
- **list**:双向列表,`lpush` 左插 / `rpush` 右插、`lrange key 0 -1` 取全部,可做简单队列
- **set**:无序、**元素不重复**,`sadd` 添加、`smembers` 查看全部,天然去重
- **zset**:带分数的有序集合,`zadd rank 100 alex`、`zrange rank 0 -1`,做**排行榜**首选

```sql
set name alex          # string 写入
get name               # alex
incr count             # string 自增(计数器)
hset user:1 name alex  # hash 写字段
hget user:1 name       # alex
hgetall user:1         # 取整个对象
lpush list1 a          # list 从左插
rpush list1 b          # 从右插
lrange list1 0 -1      # 取全部
sadd tags a b a        # set 自动去重
smembers tags          # 只剩 a、b
zadd rank 100 alex     # zset 带分数
zrange rank 0 -1       # 排行榜取值
```

*Redis 五大类型常用命令*

### 3. 过期时间与持久化
**`expire` 设过期秒数、`TTL` 查剩余时间;持久化两种方案:**RDB 快照**(快、可能丢数据)和 **AOF 日志**(全、文件大)。**

- `expire key 60`:60 秒后自动删除;`ttl key` 查剩余秒数,**-1 表示永不过期、-2 表示 key 不存在(或已过期)**
- `persist key` 移除过期时间,变回永不过期
- **RDB(快照)**:定时把整个内存数据 dump 成文件,文件小、恢复快,但**最后一次快照之后的数据会丢**
- **AOF(日志)**:每条写命令都追加记录进日志文件,丢数据少,但文件大、恢复慢
- 两种方式可以同时开启;Redis 重启后靠持久化文件恢复内存数据

```sql
set token abc123
expire token 60    # 60 秒后自动删除
ttl token          # 查剩余秒数
persist token      # 取消过期时间
```

*过期时间操作*

### 4. python 操作 redis
**用 redis-py:`r = redis.Redis(host, port)`,**方法名和命令同名**(`r.set()`、`r.get()`),返回值默认是 **bytes**。**

- 安装:`pip install redis`;连接:`r = redis.Redis(host='127.0.0.1', port=6379, db=0)`
- 方法与命令同名:`r.set('name','alex')`、`r.get('name')`、`r.incr('count')`、`r.expire('name', 60)`
- 默认返回 **bytes**(如 b'alex'),连接时加 `decode_responses=True` 直接得到字符串
- 其他类型同理:`r.hset/hget/hgetall`、`r.lpush/r.lrange`、`r.sadd/smembers`、`r.zadd/zrange`
- 生产环境常用**连接池** `redis.ConnectionPool(...)` 复用连接,避免频繁建连

```python
import redis

# decode_responses=True:取出来直接是 str,否则是 bytes
r = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True)

r.set("name", "alex")
r.expire("name", 60)              # 60 秒过期
print(r.get("name"))              # alex

r.hset("user:1", "age", 18)
print(r.hgetall("user:1"))        # {'age': '18'}

r.zadd("rank", {"alex": 100, "bob": 90})
print(r.zrange("rank", 0, -1, withscores=True))
```

*redis-py 基本操作*

### 5. MongoDB 概念与 pymongo
**MongoDB 是**文档型**数据库,结构为 **database → collection → document**,文档是 BSON 格式、自带唯一 `_id`,python 里用 **pymongo** 操作。**

- 和 MySQL 对照:**database 对应库、collection(集合)对应表、document(文档)对应行**;文档格式是 BSON(二进制的 JSON)
- 每条文档自动生成唯一的 **_id**(默认 ObjectId 类型),不用自己设计主键
- pymongo 三步:`client = MongoClient(host, 27017)` → `db = client['school']` → `col = db['student']`
- 增:`insert_one({})` / `insert_many([{}, {}])`;查:`find_one({})` 返回一条文档、`find({})` 返回**游标**(可 for 遍历)
- 条件用字典加操作符:`{'age': {'$gt': 18}}` 大于、`$gte` ≥、`$lt` <、`$in` 在列表中
- 改:`update_one(条件, {'$set': {'age': 20}})`;删:`delete_one(条件)` / `delete_many(条件)`

```python
from pymongo import MongoClient

client = MongoClient("127.0.0.1", 27017)
col = client["school"]["student"]     # 库.集合

# 增
col.insert_one({"name": "alex", "age": 18, "gender": "男"})
# 查:find_one 一条,find 全部(游标,可 for 遍历)
print(col.find_one({"name": "alex"}))
for doc in col.find({"age": {"$gt": 16}}):
    print(doc)
# 改:$set 指定要修改的字段
col.update_one({"name": "alex"}, {"$set": {"age": 20}})
# 删
col.delete_one({"name": "alex"})
```

*pymongo 增删改查*

### 6. MySQL、Redis、MongoDB 选型对比
****MySQL 存核心数据(要事务、要持久),Redis 做缓存(要快、可过期),MongoDB 存灵活文档(字段多变)**;三者互补,不是替代关系。**

- MySQL:关系型,表结构固定,支持事务和多表连查,适合**订单、账户、资金**等核心数据
- Redis:内存 key-value,读写最快、可设过期,适合**缓存、验证码、排行榜、计数器**
- MongoDB:文档型,BSON 结构灵活、无固定表结构,适合**日志、评论、商品详情**等字段不固定的数据
- 典型架构:请求先查 Redis 缓存,没有再查 MySQL,查到后回写 Redis,减轻数据库压力
- 一句话选型:**要事务强一致找 MySQL,要速度找 Redis,要结构灵活找 MongoDB**

### 7. Redis 持久化细节:RDB 与 AOF 深入对比
**RDB 靠 **bgsave fork 子进程做全量快照**,AOF 靠**逐条追加写命令**并按 `appendfsync` 策略刷盘,文件大了还有 **AOF 重写**;两者可同时开启。**

- RDB 的触发:配置 `save 900 1`(900 秒内至少 1 次修改就触发)、手动 `save`(**阻塞主线程,生产禁用**)与 `bgsave`(fork 子进程做快照,不阻塞)
- RDB 优:全量二进制文件紧凑、**恢复最快**;劣:两次快照之间的数据宕机就丢,不适合数据完整性要求高的场景
- AOF 刷盘策略 `appendfsync`:**always 每条命令都刷(最安全、最慢)**、**everysec 每秒刷一次(默认,最多丢约 1 秒)**、no 交给操作系统(最快、最不安全)
- AOF 文件越写越大 → **AOF 重写**:按当前内存数据生成最小命令集,`bgrewriteaof` 触发(同样 fork 子进程),重写期间新写入照常追加,不丢数据
- **Redis 4.0+ 支持混合持久化**:AOF 重写时先写入 RDB 格式的全量数据、之后追加增量命令,兼顾恢复速度与数据安全
- 选型:能容忍丢一点数据、追求恢复速度 → 只开 RDB;数据重要 → 开 AOF;生产环境一般**两者同时开**

```sql
# redis.conf 关键配置
save 900 1                # 900 秒内 1 次修改触发 RDB
save 300 10               # 300 秒内 10 次修改触发 RDB
appendonly yes            # 开启 AOF
appendfsync everysec      # 每秒刷盘,最多丢约 1 秒数据

# 命令行手动触发
# bgsave          后台做 RDB 快照,不阻塞
# bgrewriteaof    后台重写 AOF,压缩文件
```

*持久化相关配置与命令*

### 8. Redis 事务与管道 pipeline
**`multi → 命令入队 → exec` 保证命令**连续执行不被插队**,但不保证原子性、不回滚;**pipeline 把多条命令攒起来一次发送**,省掉逐条往返的网络开销。**

- 事务三步:`multi` 开启 → 后续命令只入队不执行 → `exec` 一次性顺序执行;`discard` 可中途放弃整个队列
- 两类错误要分清:**入队时**就发现命令不存在/参数错 → exec 时**整个事务都不执行**;**执行时**某条命令操作类型不对(如对 string 做 lpush)→ 只有它失败,**其他命令照常执行、不回滚**
- 所以 Redis 事务**不保证原子性**、没有回滚;'要么全成功要么全失败'的强一致需求要靠业务层或 Lua 脚本兜底
- `watch key` 是乐观锁:exec 之前 key 被别的客户端改过,事务自动放弃执行,适合'先查再改'的竞态场景
- **管道 pipeline**:客户端把一批命令一次性发给服务端、再统一收结果,把 N 次网络往返(RTT)压成 1 次,批量写入性能大幅提升;它只负责'攒着发',和事务的'不被插队'是两回事,redis-py 的 `pipeline()` 默认连事务一起打包
- 注意:事务/管道都**不能替代锁**;高并发下'读-改-写'的竞态要用 watch 或 Lua 保证

```python
import redis

r = redis.Redis(decode_responses=True)

# 管道:一批命令一次发送、统一收结果
pipe = r.pipeline()
pipe.set("k1", "v1")          # 命令先在客户端排队
pipe.incr("num")              # num 不存在,自增后为 1
pipe.hset("user:1", "name", "alex")
ret = pipe.execute()          # 一次提交,返回每条命令的结果列表
print(ret)                    # [True, 1, 1]

# transaction=False 就是纯管道:只省网络开销,不打包 MULTI/EXEC
fast = r.pipeline(transaction=False)
```

*redis-py pipeline 批量提交*

### 9. MongoDB 聚合管道 aggregate 简介
**aggregate 让文档流过一串 stage:**`$match` 过滤 → `$group` 分组统计 → `$sort`/`$limit` 收尾**,与 SQL 的 where、group by、order by 一一对应。**

- 聚合管道:上一个阶段的输出就是下一个阶段的输入,像流水线;`col.aggregate([...阶段列表...])` 返回游标
- `$match`:过滤文档,条件写法与 find 完全一样(**先 match 再 group,能少处理大量数据**)
- `$group`:`_id` 指定分组依据(如 `'$gender'`),配合累加器统计——`$sum: 1` 计数、`$avg`/`$max`/`$min`/`$sum` 求均值与最值
- `$project` 挑选/重命名字段(1 保留 0 剔除)、`$sort` 排序(1 升 -1 降)、`$limit`/`$skip` 截取
- 对照 SQL:$match = where、$group = group by、$project = select 挑列、$sort = order by、$limit = limit
- 复杂统计(如按分组算平均再取前三)在 MongoDB 里就是一条 pipeline;聚合是 MongoDB 做数据分析的核心工具

```python
from pymongo import MongoClient

col = MongoClient()["school"]["student"]

# 等价 SQL:select gender, count(*) cnt, avg(age) avg_age
#          from student where age >= 18
#          group by gender order by cnt desc limit 5
pipeline = [
    {"$match": {"age": {"$gte": 18}}},              # 1.先过滤
    {"$group": {"_id": "$gender",                   # 2.按 gender 分组
                "cnt": {"$sum": 1},                 #    计数
                "avg_age": {"$avg": "$age"}}},      #    平均年龄
    {"$sort": {"cnt": -1}},                         # 3.按人数降序
    {"$limit": 5},
]
for row in col.aggregate(pipeline):
    print(row)   # {'_id': '男', 'cnt': 3, 'avg_age': 20.5}
```

*aggregate 分组统计*

## 📖 课后作业（MySQL）


### 1. 作业清单与完成顺序

**数据库阶段两次大作业：**Day44 库表约束作业**（建学生表+外键级联）→ **Day48 pymysql 作业**（参数化增删改查）。**

- Day44：建 student/cls 表，练主键自增、唯一、默认值、外键级联
- Day48：用 pymysql 写增删改查，重点练 **%s 参数化**防 SQL 注入
- 做完到「题库练习」筛 MySQL 章节的题自测

---
