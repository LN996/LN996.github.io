---
title: MySQL学习笔记 01:基础查询与 where 条件筛选
date: 2026-11-17 10:00:00
tags:
  - MySQL
  - 数据库
  - 查询
categories:
  - 数据库
---

> 上一篇把库表数据的增删改查走了一遍,这一篇开始攻 SELECT。
> 核心就两件事:**搞懂 SQL 的执行顺序**,**用 where 把全表数据筛成你要的样子**。

## 一、前期准备:建一张员工表

后面所有查询都基于这张 emp 表,先建好并插入测试数据:

```sql
create table emp(
    id int not null unique auto_increment,
    name varchar(20) not null,
    sex enum('male','female') not null default 'male',  # 大部分是男的
    age int(3) unsigned not null default 28,
    hire_date date not null,
    post varchar(50),
    post_comment varchar(100),
    salary double(15,2),
    office int,        # 一个部门一个屋子
    depart_id int
);
```

几点说明:

- 表名 `emp`,用于存储员工信息,后续查询操作均基于该表演示。
- `sex` 是枚举类型,默认值为 `male`,符合员工性别多数为男性的业务场景。
- `office` 对应部门办公室编号,规则为一个部门对应一个办公室。

插入测试数据(便于后面每条 SQL 都能看到效果):

```sql
insert into emp(name,sex,age,hire_date,post,salary,office,depart_id) values
('jason','male',18,'20170301','teacher',7300.33,401,1),
('tom','male',78,'20150302','teacher',1000000.31,401,1),
('kevin','male',81,'20130305','teacher',8300,401,1),
('tony','male',73,'20140701','teacher',3500,401,1),
('sank','male',48,'20101111','teacher',10000,401,1),
('哈哈','female',48,'20150311','sale',3000.13,402,2),
('呵呵','female',38,'20101101','sale',2000.35,402,2),
('jerry','female',18,'20140101','sale',2200.55,402,2);
```

## 二、查询关键字的执行顺序

### 2.1 书写顺序 ≠ 执行顺序

```sql
-- 书写顺序
select id, name from emp where id > 3;
```

实际执行顺序依次为 **from → where → select**,和书写顺序存在差异:

```
from emp       ① 先找到表
where id > 3   ② 再过滤行
select id,name ③ 最后挑字段
```

### 2.2 编写技巧

1. 先按书写顺序构思,先用 `select *` 占位。
2. 补全后续的 `from`、`where` 等语句逻辑。
3. 最后把 `*` 替换为实际需要查询的字段,降低编写难度。

> 记住这个顺序非常关键:后面 having、order by 的位置、where 里为什么不能用聚合函数,全靠它推导。

## 三、where 条件筛选

### 3.1 基础规则

where 的作用是对全表数据执行筛选操作,过滤不符合条件的记录。

### 3.2 范围匹配

查询 id 大于等于 3 且小于等于 6 的数据,两种写法等价:

```sql
select id, name, age from emp where id >= 3 and id <= 6;
select id, name from emp where id between 3 and 6;
```

查询薪资为 20000、18000、17000 的数据,两种写法等价:

```sql
select * from emp where salary = 20000 or salary = 18000 or salary = 17000;
select * from emp where salary in (20000, 18000, 17000);
```

### 3.3 模糊匹配(like)

查询员工姓名包含字母 o 的员工姓名和薪资:

```sql
select name, salary from emp where name like '%o%';
```

查询员工姓名为 4 个字符的员工姓名和薪资,两种写法均可:

```sql
select name, salary from emp where name like '____';          -- 4 个下划线,一个下划线代表一个字符
select name, salary from emp where char_length(name) = 4;
```

> `like` 里两个通配符:`%` 代表任意多个字符,`_` 代表任意一个字符。

### 3.4 反向筛选

查询 id 小于 3 或者 id 大于 6 的数据:

```sql
select * from emp where id not between 3 and 6;
```

查询薪资不在 20000、18000、17000 范围的数据:

```sql
select * from emp where salary not in (20000, 18000, 17000);
```

### 3.5 NULL 值判断

查询岗位描述为空的员工姓名和岗位名——**判断 NULL 不能用等号,必须用 is**:

```sql
-- 错误写法
select name, post from emp where post_comment = NULL;

-- 正确写法
select name, post from emp where post_comment is NULL;

-- 反过来:非空
select name, post from emp where post_comment is not NULL;
```

## 四、细节补充

| 细节 | 说明 |
| --- | --- |
| between and | 包含左右两个边界值;反向筛选用 `not between` 时会排除边界值,编写时注意范围准确性 |
| NULL 处理 | 所有判断 NULL 的场景必须用 `is NULL` 或 `is not NULL`,用等号判断永远返回空结果,不会匹配任何记录 |
| like 通配符 | `%` 匹配任意多个字符,`_` 匹配单个字符;要匹配字面的 `%` 或 `_` 需用 `\` 转义 |

---

**本系列目录**

- 00. 数据库增删改查(CRUD)大全【库·表·数据】
- 01. MySQL 基础查询与 where 条件筛选(本篇)
- 02. MySQL 分组统计与聚合函数(含 where + group by 组合)
- 03. MySQL 进阶查询(having·去重·排序·分页·多表联查·ORM)
- 04. MySQL 表关系设计(一对一·一对多·多对多)
