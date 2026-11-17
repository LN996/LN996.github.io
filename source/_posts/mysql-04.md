---
title: MySQL学习笔记 04:表关系设计(一对一·一对多·多对多)
date: 2026-11-17 13:00:00
tags:
  - MySQL
  - 数据库
  - 表关系
  - 外键
categories:
  - 数据库
---

> 表关系是设计数据库的核心。判断方法永远是"**站在两张表的角度各看一遍**",不要只看一边就下结论。
> 这一篇把一对一、一对多、多对多三种关系一次讲透,建表代码全部可直接复制。

## 一、先记住判断口诀

判断两张表的关系,必须**双向验证**:

> A 表的一条记录能不能对应 B 表的多条? B 表的一条记录能不能对应 A 表的多条?
>
> - 只有一边能 → **一对多**
> - 两边都能 → **多对多**
> - 两边都不能 → **一对一**(或者根本没关系)

## 二、一对多

### 2.1 关系判断

以员工表(emp)和部门表(dep)为例:

- 站在**员工表**视角:一个员工无法对应部门表中的多个部门 → 该方向不成立。
- 站在**部门表**视角:一个部门可以对应员工表中的多个员工 → 该方向成立。

结论:单向一对多成立,二者属于**一对多**关系。部门是"一"的一方,员工是"多"的一方。

### 2.2 示例表结构

员工表(emp)——通过外键 `dep_id` 关联部门表的 id:

| id | emp_name | emp_gender | dep_id |
| --- | --- | --- | --- |
| 1 | jason | male | 1 |
| 2 | egon | female | 2 |
| 3 | tank | male | 2 |
| 4 | kevin | male | 3 |
| 5 | oscar | female | 3 |
| 6 | sena | female | 4 |

部门表(dep)——id 字段作为被关联的主键:

| id | dep_name | dep_desc |
| --- | --- | --- |
| 1 | 外交部 | 漂泊游荡 |
| 2 | 教学部 | 教书育人 |
| 3 | 技术部 | 技术能力有限部门 |

### 2.3 建表代码

先创建被关联的部门表,再创建关联方员工表:

```sql
create table dep(
    id int primary key auto_increment,
    dep_name char(16),
    dep_desc char(32)
);

create table emp(
    id int primary key auto_increment,
    name char(16),
    gender enum('male','female','others') default 'male',
    dep_id int,
    foreign key(dep_id) references dep(id)
    on update cascade   # 同步更新
    on delete cascade   # 同步删除
);
```

### 2.4 数据插入

先插部门表,再插员工表(保证外键指向的部门 id 存在):

```sql
insert into dep(dep_name,dep_desc) values
('sb教学部','教书育人'),
('外交部','多人外交'),
('nb技术部','技术能力有限部门');

insert into emp(name,dep_id) values
('jason',2),
('egon',1),
('tank',1),
('kevin',3);
```

### 2.5 级联操作

| 操作 | 效果 |
| --- | --- |
| `on update cascade` | 部门表 id 更新时,员工表中关联的 dep_id 同步更新 |
| `on delete cascade` | 部门表某条记录删除时,员工表中关联该部门的所有记录同步删除 |

## 三、多对多

### 3.1 关系判定

以书籍表(book)和作者表(author)为例:

- 从书籍表视角:一本书可对应多个作者 → 一对多。
- 从作者表视角:一个作者可撰写多本书 → 一对多。

两张表互为双向一对多关系时,整体就是**多对多**关系。

示例数据:

| 表 | 字段 | 示例内容 |
| --- | --- | --- |
| 书籍表 book | id | 1、2、3、4 |
| 书籍表 book | title | python入门到放弃、葵花宝典、前端基础、水浒传 |
| 书籍表 book | price | 21000、6666、999、123.23 |
| 作者表 author | id | 1、2 |
| 作者表 author | name | jason、egon |
| 作者表 author | age | 18、84 |

### 3.2 设计规则

- 直接在两张原始表中创建外键关联,**无法实现**多对多关系。
- 多对多关系需要额外创建**第三张关系表**,专门存储两张原始表的数据关联。
- 关系表不存储业务核心数据,仅用于维护两张原始表的映射关系。

### 3.3 建表代码(重点:正文没写全,从截图转录)

关系表 book2author 包含 id、author_id、book_id 三个字段,author_id 关联作者表、book_id 关联书籍表,均设置同步更新、同步删除:

```sql
create table author(
    id int primary key auto_increment,
    name varchar(32),
    age int
);

create table book(
    id int primary key auto_increment,
    title varchar(32),
    price int
);

create table book2author(
    id int primary key auto_increment,
    author_id int,
    book_id int,
    foreign key(author_id) references author(id)
    on update cascade   # 同步更新
    on delete cascade,  # 同步删除
    foreign key(book_id) references book(id)
    on update cascade   # 同步更新
    on delete cascade   # 同步删除
);
```

> 注意:一个关系表里有两个 `foreign key`,第一个外键约束末尾要加逗号 `,` 和第二个隔开——这是新手最常漏的地方。

## 四、一对一

### 4.1 适用场景

当单表字段过多,且每次查询仅使用部分字段时,可将表拆分为两张,提升查询效率。

- 用户表存储高频查询字段:id、name、age
- 用户详情表存储低频查询字段:id、addr、phone、hobby、email 等

### 4.2 关系判断

- 从用户表视角:一个用户不能对应多个用户详情。
- 从详情表视角:一个详情不能属于多个用户。

当双向一对多关系均不成立时,两张表为一对一关系(也可能是根本没有关联)。

### 4.3 建表代码

外键字段可建立在任意一张表中,推荐建立在查询频率更高的表内。外键字段需添加 **unique 约束**,保证一对一关联的唯一性:

```sql
create table authordetail(
    id int primary key auto_increment,
    phone int,
    addr varchar(64)
);

create table author(
    id int primary key auto_increment,
    name varchar(32),
    age int,
    authordetail_id int unique,
    foreign key(authordetail_id) references authordetail(id)
    on update cascade   # 同步更新
    on delete cascade   # 同步删除
);
```

> 一对多 vs 一对一建表的唯一区别:一对一的外键字段多了 `unique`,把"多"限制成了"一"。

## 五、避坑提醒

| 坑 | 说明 |
| --- | --- |
| 表创建顺序 | 必须先创建被关联表(如 dep),再创建关联表(如 emp),否则外键约束创建失败 |
| 数据插入顺序 | 必须先给被关联表插数据,再给关联表插数据,避免外键指向不存在的记录 |
| 外键字段类型 | 关联表的外键字段类型必须与被关联表的主键字段类型**完全一致**,否则外键创建失败 |
| 级联删除风险 | 开启 `on delete cascade` 后,删除一方数据会同步删除关联数据,生产环境需谨慎并做好备份 |
| 多对多中间表 | 一定要建第三张关系表,且两个外键之间别忘逗号 |
| 一对一 unique | 外键字段不加 unique 会退化成一对多 |

---

**本系列目录**

- 00. 数据库增删改查(CRUD)大全【库·表·数据】
- 01. MySQL 基础查询与 where 条件筛选
- 02. MySQL 分组统计与聚合函数(含 where + group by 组合)
- 03. MySQL 进阶查询(having·去重·排序·分页·多表联查·ORM)
- 04. MySQL 表关系设计(一对一·一对多·多对多)(本篇)
