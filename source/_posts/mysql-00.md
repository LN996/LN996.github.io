---
title: MySQL学习笔记 00:数据库增删改查(CRUD)大全【库·表·数据】
date: 2026-11-17 09:00:00
tags:
  - MySQL
  - 数据库
  - CRUD
categories:
  - 数据库
---

> 这一篇是 MySQL 的"增删改查"总纲。后面几篇的分组、联表、表关系,全都是在 SELECT 上做花活,所以先把 **库 → 表 → 数据** 三层的 CRUD 焊死,后面学起来会顺很多。
>
> 每一条都给可直接复制运行的例子,建议边看边敲。

## 〇、先分清楚三个层级

初学者最容易混的就是"库、表、数据"三层,记住这个嵌套关系:

```
数据库(database)
  └── 表(table)
        └── 记录/数据行(row)
```

- **库** 是文件夹,**表** 是文件夹里的 Excel 文件,**数据** 是表格里的一行行内容。
- CRUD 就是 Create(增)、Retrieve(查)、Update(改)、Delete(删) 四个动作。

| 层级 | 增 | 查 | 改 | 删 |
| --- | --- | --- | --- | --- |
| 库 | `create database` | `show databases` | `alter database` | `drop database` |
| 表 | `create table` | `show tables` / `desc` | `alter table` | `drop table` |
| 数据 | `insert into` | `select` | `update` | `delete from` |

## 一、库的操作

### 1.1 增:创建数据库

```sql
-- 最简写法
create database db1;

-- 推荐写法:指定字符集,避免中文乱码(utf8mb4 才是真正的 UTF-8)
create database db1 default charset utf8mb4 collate utf8mb4_general_ci;
```

> 面试点:MySQL 里的 `utf8` 是"假 UTF-8",最多 3 字节,存不了 emoji;要用 `utf8mb4`。

### 1.2 查:查看数据库

```sql
show databases;              -- 查看所有库
show create database db1;    -- 查看某个库的创建语句(能看到字符集)
select database();           -- 查看当前正在使用哪个库
```

### 1.3 用:切换数据库

```sql
use db1;   -- 进入 db1,后续操作都在这个库里进行
```

> 进入库之后,`create table` 才是建在这个库里。不 use 就直接建表会报 `No database selected`。

### 1.4 改:修改数据库

```sql
alter database db1 default charset utf8mb4;   -- 改字符集
```

> 数据库的名字**不能改**。想改名只能新建一个库再把表迁过去。

### 1.5 删:删除数据库

```sql
drop database db1;
```

> ⚠️ 不可逆操作,库里所有表和数据全没了。生产环境删库前必须备份。

## 二、表的操作

> 操作表之前一定先 `use 库名;`

### 2.1 增:创建表

```sql
create table student(
    id int primary key auto_increment,          -- 主键,自增
    name varchar(20) not null,                  -- 姓名,非空
    age int unsigned default 18,                -- 年龄,无符号,默认18
    gender enum('male','female') default 'male',-- 枚举,只能二选一
    score decimal(5,2),                         -- 分数,共5位其中2位小数
    create_time datetime                        -- 创建时间
) engine=innodb default charset=utf8mb4;
```

常见字段类型:

| 类型 | 说明 | 例子 |
| --- | --- | --- |
| `int` | 整数 | `age int` |
| `decimal(M,D)` | 精确小数(钱必用) | `salary decimal(10,2)` |
| `float` / `double` | 浮点小数(有精度误差) | `height float` |
| `char(n)` | 定长字符串,快但费空间 | `gender char(1)` |
| `varchar(n)` | 变长字符串,省空间 | `name varchar(20)` |
| `text` | 大文本 | `content text` |
| `enum(...)` | 枚举,只能选其中一个 | `sex enum('male','female')` |
| `set(...)` | 多选 | `hobby set('篮球','足球')` |
| `date` | 日期 `2026-11-17` | `birth date` |
| `datetime` | 日期时间 `2026-11-17 15:00:00` | `create_time datetime` |

六大约束:

| 约束 | 关键字 | 作用 |
| --- | --- | --- |
| 非空 | `not null` | 该字段不能为空 |
| 唯一 | `unique` | 该字段值不能重复 |
| 主键 | `primary key` | 非空 + 唯一,一张表一个 |
| 自增 | `auto_increment` | 自动加 1,必须配合索引(一般是主键) |
| 默认 | `default` | 不填时用默认值 |
| 外键 | `foreign key ... references ...` | 关联另一张表 |

### 2.2 查:查看表

```sql
show tables;              -- 查看当前库里所有表
show create table student;-- 查看建表语句
desc student;             -- 查看表结构(describe 的缩写)
```

### 2.3 改:修改表结构(alter table)

```sql
-- 改表名
alter table student rename to stu;

-- 加字段
alter table stu add phone varchar(11);

-- 加字段到第一列 / 指定位置
alter table stu add sex char(1) first;
alter table stu add height int after name;

-- 删字段
alter table stu drop phone;

-- 改字段类型(modify 只改类型)
alter table stu modify name varchar(30) not null;

-- 改字段名 + 类型(change 要写两遍名字)
alter table stu change name stu_name varchar(30);

-- 加/删主键
alter table stu add primary key(id);
alter table stu drop primary key;

-- 加/删唯一约束
alter table stu add unique(stu_name);
alter table stu drop index stu_name;

-- 改字符集
alter table stu default charset=utf8mb4;
```

> `modify` 和 `change` 的区别:改类型用 modify,连名字一起改用 change(要写"旧名 新名 类型")。

### 2.4 删:删除表

```sql
drop table stu;
drop table if exists stu;   -- 存在才删,避免报错
```

### 2.5 复制表(面试偶尔问)

```sql
create table stu2 like student;              -- 只复制表结构,不要数据
create table stu3 as select * from student;  -- 复制表结构 + 数据(但丢主键/自增/外键等属性)
```

## 三、数据的操作(重点)

### 3.1 增:insert

```sql
-- 指定字段插入(推荐,字段和值一一对应)
insert into student(name, age, gender) values('jason', 18, 'male');

-- 全字段插入(值的顺序必须和表结构完全一致)
insert into student values(1, 'egon', 20, 'male', 99.5, now());

-- 一次插多条(比一条条插快得多)
insert into student(name, age) values
    ('tank', 18),
    ('kevin', 28),
    ('oscar', 30);
```

### 3.2 查:select(后面几篇的主角)

```sql
select * from student;                    -- 查所有字段(学习时用,生产少用)
select name, age from student;            -- 查指定字段
select name as '姓名', age '年龄' from student; -- 起别名,as 可省略但不推荐省
```

### 3.3 改:update

```sql
-- ⚠️ 一定要带 where!不然全表都被改掉
update student set age = 19 where name = 'jason';

-- 同时改多个字段
update student set age = 20, score = 100 where id = 2;

-- 在原有值基础上改
update student set age = age + 1 where id = 3;
```

> 血泪教训:`update student set age=18;` 忘了 where → 全班都 18 岁。执行更新前先写 where,再写 set。

### 3.4 删:delete

```sql
-- ⚠️ 同样要带 where
delete from student where id = 5;

-- 清空整张表(两种方式的坑不同)
delete from student;   -- 一条条删,慢,自增 id 不会从头开始(接着上次的自增)
truncate student;      -- 直接清空表,快,自增 id 归零
```

> `delete` vs `truncate`:delete 可以带 where、可以回滚;truncate 是 DDL,整表清空、自增归零、不可回滚。

## 四、一条 SQL 的书写与执行顺序

这个顺序贯穿后面所有查询文章,先记住:

```sql
-- 书写顺序
select  字段
from    表
where   条件
group by 字段
having  分组后条件
order by 字段
limit   条数;
```

实际执行顺序是:

```
from → where → group by → having → select → order by → limit
```

> 所以 **where 里不能用聚合函数**(此时还没分组算出来),而 having 可以。这个坑后面第 02、03 篇会反复用到。

## 五、易错点速查

| 坑 | 正确做法 |
| --- | --- |
| 中文乱码 | 建库建表都指定 `utf8mb4` |
| `update`/`delete` 忘写 where | 先写 where 再写 set,全表操作用 truncate |
| `float` 存钱丢精度 | 用 `decimal` |
| `char` 和 `varchar` 选错 | 定长短字段用 char,变长用 varchar |
| 自增字段不是主键报错 | `auto_increment` 必须配合 key(主键/唯一) |
| 建外键关联失败 | 先建被关联表、先插被关联数据;两边字段类型必须一致 |
| `utf8` 存不了 emoji | 用 `utf8mb4` |

---

**本系列目录**

- 00. 数据库增删改查(CRUD)大全【库·表·数据】(本篇)
- 01. MySQL 基础查询与 where 条件筛选
- 02. MySQL 分组统计与聚合函数(含 where + group by 组合)
- 03. MySQL 进阶查询(having·去重·排序·分页·多表联查·ORM)
- 04. MySQL 表关系设计(一对一·一对多·多对多)
