---
title: MySQL学习笔记 03:进阶查询(having·去重·排序·分页·多表联查·ORM)
date: 2026-11-17 12:00:00
tags:
  - MySQL
  - 数据库
  - 多表查询
categories:
  - 数据库
---

> 这一篇把 SELECT 剩下的招式补齐:having(分组后再筛)、distinct(去重)、order by(排序)、limit(分页),然后进入多表联查和 ORM 的概念。
> 理论不多,全是能直接跑的例子。

## 一、having 分组筛选

### 1.1 基础规则

having 的语法和 where 一致,区别是:

- **where 在分组之前执行过滤**
- **having 在分组之后执行过滤**
- having 可以直接使用聚合函数作为筛选条件

### 1.2 语法示例

需求:统计各部门年龄在 30 岁以上的员工平均工资,并且只保留平均薪资大于 10000 的部门。

```sql
select post, avg(salary)
from emp
where age > 30
group by post
having avg(salary) > 10000;
```

拆解一下:

```
where age > 30          -- ① 分组前:先筛掉 30 岁以下的
group by post           -- ② 按部门分组
avg(salary)             -- ③ 算出每个部门的平均薪资
having avg(salary)>...  -- ④ 分组后:保留平均值 > 10000 的部门
```

> having 里能用 `avg(salary)` 而 where 里不能,根本原因就是执行顺序:where 执行时分组还没发生。

## 二、distinct 去重

### 2.1 核心规则

- 必须是**完全一样**的数据才可以去重。
- 存在主键等唯一标识字段时,无法完成去重(因为 id 不同)。

### 2.2 示例说明

存在以下三条数据:

```python
[
    {'id': 1, 'name': 'jason', 'age': 18},
    {'id': 2, 'name': 'jason', 'age': 18},
    {'id': 3, 'name': 'egon',  'age': 18},
]
```

- 若按 `id, name, age` 去重 → 三条都不同(id 不一样),去不掉。
- 若只按 `name, age` 去重 → jason 那条重复被去掉,剩 2 条。

### 2.3 语法示例

查询 emp 表中去重后的 id 和 age:

```sql
select distinct id, age from emp;
```

查询 emp 表中去重后的 age:

```sql
select distinct age from emp;
```

> distinct 需放在查询字段最左侧;多字段去重时,所有字段值完全一致才会被判定为重复。

## 三、order by 排序

### 3.1 基础规则

```sql
select * from emp order by age;        -- 默认升序
select * from emp order by age asc;    -- asc 可省略
select * from emp order by age desc;   -- desc 降序
```

### 3.2 多字段排序

当第一个排序字段值相同时,可指定第二个字段的排序规则:

```sql
select * from emp order by age desc, salary asc;
```

含义:先按 age 降序排列,如果 age 相同,再按 salary 升序排列。

### 3.3 综合查询示例

需求:统计各部门年龄在 10 岁以上的员工平均工资,保留平均薪资大于 1000 的部门,然后对平均工资降序排序。

```sql
select post, avg(salary)
from emp
where age > 10
group by post
having avg(salary) > 1000
order by avg(salary) desc;
```

> 这条把 where / group by / having / order by 全串起来了,正好复习上一篇的执行顺序。

## 四、limit 分页

### 4.1 核心规则

limit 用于限制查询结果的展示条数,主要用于数据过多时的分页处理。

- **单参数**:`limit 条数`,表示从第一条数据开始展示指定条数。
- **双参数**:`limit 起始位置, 条数`,起始位置从 0 开始计数。

### 4.2 语法示例

只展示 emp 表的三条数据:

```sql
select * from emp limit 3;
```

展示 emp 表第 1 到第 5 条数据:

```sql
select * from emp limit 0, 5;
```

展示 emp 表第 6 到第 10 条数据:

```sql
select * from emp limit 5, 5;
```

> 分页公式:第 n 页、每页 m 条 → `limit (n-1)*m, m`。

## 五、ORM 对象关系映射

### 5.1 核心逻辑

ORM 即对象关系映射(Object Relational Mapping),作用是让不懂 SQL 语句的开发者也可以用面向对象的方式操作数据库。

核心映射关系:

| 数据库概念 | Python 概念 |
| --- | --- |
| 表 | 类 |
| 一条条数据(记录) | 对象 |
| 字段对应的值 | 对象的属性 |

### 5.2 操作映射规则

- 编写类的操作 → 对应创建数据库表
- 用类生成对象的操作 → 对应创建表中数据
- 访问对象属性的操作 → 对应获取数据字段对应的值

设计目的是减轻 Python 程序员的压力,仅需掌握 Python 面向对象知识即可操作 MySQL。常见的 ORM 框架有 SQLAlchemy、Django ORM 等。

## 六、多表操作

### 6.1 前期表准备

创建部门表 dep:

```sql
create table dep(
    id int,
    name varchar(20)
);
```

创建员工表 emp(id 为主键且自增,sex 为枚举类型、非空、默认 male):

```sql
create table emp(
    id int primary key auto_increment,
    name varchar(20),
    sex enum('male','female') not null default 'male',
    age int,
    dep_id int
);
```

### 6.2 测试数据插入

向部门表 dep 插入测试数据:

```sql
insert into dep values
(200,'技术'),
(201,'人力资源'),
(202,'销售'),
(203,'运营');
```

向员工表 emp 插入测试数据:

```sql
insert into emp(name,sex,age,dep_id) values
('jason','male',18,200),
('egon','female',48,201),
('kevin','male',18,201),
('nick','male',28,202),
('owen','male',18,203),
('jerry','female',18,204);
```

### 6.3 联表查询语法

MySQL 支持四种联表查询方式:

| 联表类型 | 作用 | 语法示例 |
| --- | --- | --- |
| 内连接 inner join | 只拼接两张表中公有的数据部分 | `select * from emp inner join dep on emp.dep_id = dep.id;` |
| 左连接 left join | 展示左表所有数据,没有对应项的字段用 NULL 填充 | `select * from emp left join dep on emp.dep_id = dep.id;` |
| 右连接 right join | 展示右表所有数据,没有对应项的字段用 NULL 填充 | `select * from emp right join dep on emp.dep_id = dep.id;` |
| 全连接 union | 展示左右两表所有的数据 | `select * from emp left join dep on emp.dep_id = dep.id union select * from emp right join dep on emp.dep_id = dep.id;` |

```sql
-- 内连接:只保留两表能匹配上的行
select * from emp inner join dep on emp.dep_id = dep.id;

-- 左连接:保留 emp 全部行,dep 匹配不到补 NULL
select * from emp left join dep on emp.dep_id = dep.id;

-- 右连接:保留 dep 全部行
select * from emp right join dep on emp.dep_id = dep.id;

-- 全连接:左连接的结果 UNION 右连接的结果
select * from emp left  join dep on emp.dep_id = dep.id
union
select * from emp right join dep on emp.dep_id = dep.id;
```

> 注意上面 emp 里 jerry 的 `dep_id=204` 在 dep 表中不存在——内连接会丢掉这条,左连接会保留它(dep 字段为 NULL),这就是几种 join 最直观的区别。

## 七、细节补充

| 细节 | 说明 |
| --- | --- |
| 执行顺序 | from → where → group by → having → select → order by → limit |
| 去重注意 | distinct 放在查询字段最左侧,多字段去重需所有字段值完全一致 |
| 联表场景 | 数据量大时优先用内连接;需保留某张表全部数据时用左/右连接;全连接性能较低,谨慎使用 |

---

**本系列目录**

- 00. 数据库增删改查(CRUD)大全【库·表·数据】
- 01. MySQL 基础查询与 where 条件筛选
- 02. MySQL 分组统计与聚合函数(含 where + group by 组合)
- 03. MySQL 进阶查询(having·去重·排序·分页·多表联查·ORM)(本篇)
- 04. MySQL 表关系设计(一对一·一对多·多对多)
