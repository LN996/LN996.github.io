---
title: MySQL学习笔记 02:分组统计与聚合函数(含 where + group by 组合)
date: 2026-11-17 11:00:00
tags:
  - MySQL
  - 数据库
  - 分组统计
categories:
  - 数据库
---

> group by 是 MySQL 里最容易踩坑的一块:什么时候能 select `*`、什么时候必须配聚合函数、where 和 having 到底放哪——这一篇一次讲清。
> 测试数据沿用上一篇的 emp 表。

## 一、group by 分组

### 1.1 应用场景

分组适用于需要**按类别统计**的场景,常见包括:统计男女比例、部门平均薪资、部门秃头率、国家之间的数据统计等。

> 分组后的最小操作单位是"组",不能直接操作组内的单个数据。

### 1.2 触发场景

当查询需求中出现"**每个**""**平均**""**最高**""**最低**"等关键词时,基本就要用分组语法了。

### 1.3 严格模式(重要)

未开启严格模式时,`select * from emp group by post;` 可正常执行,返回每个组的第一条数据,但**不符合分组规范**,结果没有意义。

开启严格模式后,上述语句会直接报错,默认只能获取分组的依据字段,其他字段需要借助聚合函数实现。

开启严格模式的语句:

```sql
set global sql_mode = 'strict_trans_tables,only_full_group_by';
```

严格模式下按岗位分组的基础查询语句:

```sql
select post from emp group by post;
```

> 生产环境建议强制开启 `only_full_group_by`,避免分组查询产生非预期结果。

## 二、聚合函数

### 2.1 基本用法

可以通过聚合函数获取分组后的统计数据。字段可以通过 `as` 关键字起别名,`as` 也可以省略,但不推荐——省略后语义不明确。

获取每个部门的最高薪资:

```sql
select post, max(salary) from emp group by post;
select post as '部门', max(salary) as '最高薪资' from emp group by post;
select post '部门', max(salary) '最高薪资' from emp group by post;  -- as 省略写法,不推荐
```

获取每个部门的最低薪资:

```sql
select post, min(salary) from emp group by post;
```

获取每个部门的平均薪资:

```sql
select post, avg(salary) from emp group by post;
```

获取每个部门的工资总和:

```sql
select post, sum(salary) from emp group by post;
```

获取每个部门的人数——可统计任意非空字段实现计数:

```sql
select post, count(id) from emp group by post;
select post, count(salary) from emp group by post;
select post, count(age) from emp group by post;
```

常用聚合函数一览:

| 函数 | 作用 |
| --- | --- |
| `max(字段)` | 最大值 |
| `min(字段)` | 最小值 |
| `avg(字段)` | 平均值 |
| `sum(字段)` | 求和 |
| `count(字段)` | 计数(统计非空值) |

### 2.2 不分组时的聚合

不指定分组时,默认将**整张表作为一个组**进行聚合计算:

```sql
select max(salary) from emp;   -- 全表最高薪资
select count(id) from emp;     -- 全表人数
```

## 三、group_concat 分组字段拼接

### 3.1 基本用法

使用 `group_concat` 函数可以获取分组后的其他字段值,还支持拼接操作。

查询分组后的部门名称和每个部门下所有的员工姓名:

```sql
select post, group_concat(name) from emp group by post;
```

### 3.2 拼接操作

拼接自定义后缀:

```sql
select post, group_concat(name, '_DSB') from emp group by post;
```

拼接多个字段和分隔符:

```sql
select post, group_concat(name, ':', salary) from emp group by post;
```

### 3.3 不分组时的拼接用 concat

不分组时的字段拼接使用 `concat` 函数:

```sql
select concat('NAME:', name), concat('SAL:', salary) from emp;
```

> 区分:`group_concat` 用于分组后组内字段拼接;`concat` 用于普通行内字段拼接,二者使用场景不可混淆。

## 四、where + group by 组合实战

### 4.1 需求:统计 30 岁以上员工各岗位的平均薪资

**先过滤后分组**是 MySQL 分组统计的核心逻辑。

第一步,筛选所有年龄大于 30 岁的员工:

```sql
select * from emp where age > 30;
```

第二步,对筛选结果按岗位分组:

```sql
select post, avg(salary) from emp where age > 30 group by post;
```

### 4.2 组合使用规范

- where 和 group by 同时出现时,**group by 必须放在 where 的后面**。
- where 先对整体数据进行过滤,之后再执行分组操作。
- **where 的筛选条件不能使用聚合函数**。示例错误语句:

```sql
-- 错误:where 阶段还没分组,算不出 max(salary)
select id, name, age from emp where max(salary) > 3000;
```

### 4.3 示例数据(30 岁以上员工)

| id | name | sex | age | hire_date | post | post_comment | salary | office | depart_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | tom | male | 78 | 2015-03-02 | teacher | NULL | 1000000.31 | 401 | 1 |
| 3 | kevin | male | 81 | 2013-03-05 | teacher | NULL | 8300.00 | 401 | 1 |
| 4 | tony | male | 73 | 2014-07-01 | teacher | NULL | 3500.00 | 401 | 1 |
| 8 | sank | male | 48 | 2010-11-11 | teacher | NULL | 10000.00 | 401 | 1 |
| 9 | 哈哈 | female | 48 | 2015-03-11 | sale | NULL | 3000.13 | 402 | 2 |
| 10 | 呵呵 | female | 38 | 2010-11-01 | sale | NULL | 2000.35 | 402 | 2 |

## 五、细节补充

| 细节 | 说明 |
| --- | --- |
| 分组严格模式 | 开启 `only_full_group_by` 可避免分组查询的非预期结果,生产环境建议强制开启 |
| 聚合函数位置 | where 之后才能用聚合函数;分组统计的字段放 select,条件放 having(见下一篇) |
| 先过滤后分组 | 遇到"需先过滤再聚合"的需求,优先用 where + group by 组合,不要用 having 代替过滤逻辑 |
| 顺序校验 | 写分组查询时先检查 where 和 group by 的顺序是否正确,避免语法报错影响查询效率 |

---

**本系列目录**

- 00. 数据库增删改查(CRUD)大全【库·表·数据】
- 01. MySQL 基础查询与 where 条件筛选
- 02. MySQL 分组统计与聚合函数(含 where + group by 组合)(本篇)
- 03. MySQL 进阶查询(having·去重·排序·分页·多表联查·ORM)
- 04. MySQL 表关系设计(一对一·一对多·多对多)
