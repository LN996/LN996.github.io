---
title: 前端三件套
date: 2026-11-10 09:00:00
tags:
  - 前端
  - HTML
  - CSS
  - JavaScript
categories:
  - Python学习笔记
---
> 本文是「Python全栈学习中心」系列笔记之一,配套可刷题的本地工具(获取方式见文末)。

---

## 📖 HTML

> 🎬 对应课程:前端阶段(HTML文档结构、常用标签、表单、表格)

### 1. HTML文档结构
> 🎬 对应视频:P587~P588

**页面骨架 = **<!DOCTYPE html> 声明 + `html` 根标签**,`head` 里放给浏览器看的配置,`body` 里放给用户看的内容。**

- `<!DOCTYPE html>` 声明这是 HTML5 文档,必须写在文件第一行
- `<head>` 内是配置信息:`<meta charset="UTF-8">` 声明编码防止中文乱码,`<title>` 是浏览器标签页上显示的标题
- `<body>` 内是页面可见内容:文字、图片、链接、表单都写在这里
- 标签一般成对出现如 `<p></p>`,自闭合标签如 `<img>`、`<input>`、`<br>` 除外
- HTML 注释写 `<!-- 注释内容 -->`,浏览器不执行

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>我的第一个页面</title>
</head>
<body>
    <h1>hello world</h1>
</body>
</html>
```

*HTML5 基本骨架*

### 2. 标签分类:块级 / 行内 / 行内块
> 🎬 对应视频:P590

**块级元素**独占一行、可设宽高**;行内元素**不独占一行、宽高无效**;行内块**不独占一行但可设宽高**。**

- 块级:`div`、`p`、`h1~h6`、`ul/li`、`table` 等,独占一行,默认宽度撑满父级
- 行内:`span`、`a` 等,排在同一行,设置 width/height **不生效**
- 行内块:`input`、`img`(默认表现)等,既和别的元素排一行,又能设置宽高
- 块级里可以嵌套行内和其他块级;`p` 里不要套块级标签(浏览器会自动断开标签)
- 通过 CSS 的 display 属性可以让三者互相转换

```html
<div>我是块级,独占一行</div>
<span>我是行内,</span><span>能和别的行内排一行</span>
<input type="text" placeholder="行内块:同行显示,还能设宽高">
```

*三类标签的排列区别*

### 3. a 标签与 img 标签
> 🎬 对应视频:P593

**`a` 用 **href** 指定跳转地址、**target="_blank"** 新窗口打开、`href="#锚点"` 页内跳转;`img` 用 **src** 指定图片,`alt` 是加载失败的替代文字,`title` 是悬停提示。**

- `<a href="https://www.baidu.com">百度</a>`:href 放跳转地址,标签内容是被点击的文字
- target="_blank" 在**新标签页**打开;不写默认在当前页跳转
- 锚点跳转:给目标元素加 `id="top"`,再写 `<a href="#top">回到顶部</a>`
- img:`src` 指定图片路径,`alt` 是图片加载失败时显示的文字,`title` 是鼠标悬停时的提示文字
- `<a href="#">` 是空链接占位写法,点击后会回到页面顶部

```html
<a href="https://www.python.org" target="_blank">新窗口打开Python官网</a>
<a href="#top">回到顶部</a>
<div id="top">页面开头</div>
<img src="logo.png" alt="站点Logo加载失败" title="我是Logo">
```

### 4. 列表与表格
> 🎬 对应视频:P594、P598

**列表分**无序 `ul`** 和**有序 `ol`**,子项都是 `li`;表格用 `table > tr > td`,表头用 `th`,`rowspan` 纵向合并、`colspan` 横向合并单元格。**

- 无序列表 `<ul><li>...</li></ul>` 前面默认实心圆点;有序列表 `<ol><li>...</li></ol>` 默认数字编号
- 表格结构:`<table>` 里一行一个 `<tr>`,行内一个单元格 `<td>`,表头单元格用 `<th>`(默认加粗居中)
- `rowspan="2"`:当前单元格**向下**占两行,下一行就要少写一个 td
- `colspan="2"`:当前单元格**向右**占两列,同一行要少写一个 td
- table 常用属性:border 边框、cellpadding 内容与边框的距离、cellspacing 单元格间距

```html
<table border="1">
    <tr>
        <th>姓名</th><th colspan="2">联系方式</th>
    </tr>
    <tr>
        <td rowspan="2">alex</td><td>电话</td><td>13800000000</td>
    </tr>
    <tr>
        <td>QQ</td><td>12345678</td>
    </tr>
</table>
```

*rowspan/colspan 合并单元格*

### 5. 表单与表单控件
> 🎬 对应视频:P599

**`<form action="提交地址" method="提交方式">` 包住控件,**radio 同 name 互斥**、checkbox 可多选,`label` 的 for 对应控件 id 可以点击聚焦。**

- form:`action` 指定数据提交到哪个地址,`method` 用 get(参数拼在 URL 后)或 post(数据放请求体)
- input 常用 type:text 文本框、password 密码框、radio 单选、checkbox 多选、file 上传文件、submit 提交按钮
- 一组 radio 的 **name 必须相同**才能单选互斥;checkbox 同 name 提交时是 name=v1&name=v2 的形式
- 控件必须有 **name 属性**才会被提交,提交的值取自 value
- `<label for="user">用户名</label>`:点击文字会聚焦到 `id="user"` 的控件,radio 套上 label 更好点
- 下拉框 `<select name="city"><option value="bj">北京</option></select>`;大段文本用 `<textarea>`

```html
<form action="/register" method="post">
    <p>用户名:<input type="text" name="user"></p>
    <p>密码:<input type="password" name="pwd"></p>
    <p>
        <input type="radio" name="sex" value="m" id="m"><label for="m">男</label>
        <input type="radio" name="sex" value="f" id="f"><label for="f">女</label>
    </p>
    <p>城市:
        <select name="city">
            <option value="bj">北京</option>
            <option value="sh">上海</option>
        </select>
    </p>
    <input type="submit" value="注册">
</form>
```

*注册表单示例*

### 6. 语义化标签与特殊字符转义
> 🎬 对应视频:P590、P591

**语义化标签(header/nav/main/footer)让结构清晰利于 SEO;`&lt;` 显示 `<`、`&gt;` 显示 `>`、`&nbsp;` 显示**空格**、`&amp;` 显示 `&`。**

- 常用语义化标签:header 页头、nav 导航、main 主体、footer 页脚、section 区块
- 语义化的好处:代码可读性高,搜索引擎更容易理解页面结构(利于 SEO)
- HTML 中直接写 < 会被当成标签开头,想显示必须写转义 `&lt;` 和 `&gt;`
- `&nbsp;` 表示一个空格(HTML 默认把连续空格折叠成一个);`&amp;` 用来显示 & 本身
- 版权符号 `&copy;` 显示 ©

```html
<header>页头</header>
<nav>导航栏</nav>
<main>主体内容</main>
<footer>页脚</footer>
<p>3 &lt; 5 &amp;&amp; 5 &gt; 3</p>
<p>版权所有 &copy; 2026</p>
```

### 7. head 内常用标签详解
> 🎬 对应视频:P589

**`<head>` 是**给浏览器看的配置区**:`<meta>` 元信息、`<title>` 标签页标题、`<style>` 内嵌样式、`<link>` 引外部资源、`<script>` 引 JS 都写在这里,页面上不直接显示。**

- `<meta charset="UTF-8">` 声明编码;`<meta name="keywords" content="...">` 和 `<meta name="description" content="...">` 写关键词和页面描述,供搜索引擎收录(SEO)
- `<meta http-equiv="refresh" content="3;url=https://www.xxx.com">`:3 秒后自动跳转到目标页面(老网页常见的自动跳转写法)
- `<title>` 显示在浏览器标签页、收藏夹和搜索结果里,是 head 中唯一用户能"看到"的标签
- `<style>` 写内嵌 CSS;`<link rel="stylesheet" href="xx.css">` 引外部 CSS;`<script src="xx.js"></script>` 引外部 JS(script 必须写成双标签,不能自闭合)
- head 内的标签用户基本看不到,作用是告诉浏览器"怎么解析这个页面":编码、标题、样式、脚本

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="keywords" content="Python,教程">
    <meta name="description" content="Python 入门教程网站">
    <title>首页</title>
    <link rel="stylesheet" href="style.css">
    <script src="app.js"></script>
</head>
<body></body>
</html>
```

*head 内五个常用标签*

### 8. 更多特殊符号与 emoji
> 🎬 对应视频:P591

**除了 `&lt;` `&gt;`,常用实体还有:**`&quot;` 双引号、`&reg;` 注册商标、`&times;` 乘号、`&deg;` 度**;emoji 在 UTF-8 页面可以直接写,也可以用 `&#码点;` 数字实体。**

- 常用符号实体:`&quot;` 双引号、`&reg;` 注册商标 ®、`&times;` 乘号 ×、`&divide;` 除号 ÷、`&deg;` 度 °、`&yen;` 人民币 ¥
- HTML 实体两种写法:带名字的 `&nbsp;`,和数字码点形式 `&#160;`(十进制),两者效果相同
- emoji 就是普通 Unicode 字符:文档是 UTF-8 编码时,可以直接把 😀 写进 HTML 源码
- 也可以用数字实体写 emoji:`&#128512;` 渲染出来就是 😀,适合不方便直接输入的符号
- 什么时候必须转义:要显示的字符会被浏览器当成代码(< > &)时必须写实体;普通文字和 emoji 不转义也能正常显示

```html
<p>5 &times; 4 = 20,20 &divide; 4 = 5</p>
<p>今天气温 25&deg;C,售价 100 &yen;</p>
<p>开心 &#128512;,直接写也可以:😀</p>
```

### 9. div 与 span:布局思想
> 🎬 对应视频:P592

****div 是块级"容器",负责把页面切成头部/内容/底部等大区域;span 是行内"范围",负责圈住一行文字里的局部**;两者默认无样式,是布局思想的载体。**

- div 本身没有任何样式(无边框、无间距),独占一行,是纯粹的"区域容器",网页骨架基本靠 div 嵌套搭建
- 经典布局:一个大 div 包住整页,里面再切出头部区、导航区、主体区、页脚区,每块一个 div 配合 class 命名
- span 不换行、无样式,用来在一行文字里圈出局部做处理,如把某个词标红:`<span class="hl">重点</span>`
- div 对应"块级占位"、span 对应"行内圈字",这对组合让结构与样式分离:HTML 搭结构,CSS 管外观
- 语义化标签 header/nav/main/footer 本质上是"带语义的 div",布局思路完全一样

```html
<div class="page">
    <div class="header">头部区域</div>
    <div class="content">
        主体内容,<span class="hl">重点词标红</span>就是用 span 圈出来的
    </div>
    <div class="footer">底部区域</div>
</div>
```

*div 划区域 + span 圈局部*

### 10. body 常用文本标签
> 🎬 对应视频:P590

****标题 h1~h6、段落 p、加粗 strong、斜体 em、删除线 del、换行 br、水平线 hr** 是 body 里最常用的文本标签:标题段落独占一行是块级,br 负责强制换行。**

- h1~h6 从大到小共六级标题,独占一行自带加粗;一个页面建议只用一次 h1,搜索引擎把它当页面主标题(利于 SEO)
- p 是段落标签,自带上下外边距,段落之间有空行效果;strong 语义是"重要内容",b 只是纯样式加粗,推荐用 strong
- em 表示强调(默认斜体),i 是纯样式斜体;del 显示删除线,常用于"原价 99 现价 59"这类对比
- br 是强制换行的行内自闭合标签;hr 是水平分割线的块级自闭合标签,两者都不需要结束标签
- HTML 会把源码里的连续空格、换行折叠成一个空格:想真正换行,要么换用块级标签分段,要么写 <br>

```html
<h1>一级标题,一个页面只出现一次</h1>
<h2>二级标题</h2>
<p>这是一个段落,<strong>重点加粗</strong>,<em>强调倾斜</em>,<del>划掉不要</del>。</p>
<p>第一行文字<br>br 之后的第二行文字</p>
<hr>
```

*h/p/strong/em/br/hr 常用文本标签*

### 11. GET 与 POST 提交方式对比
> 🎬 对应视频:P599

**form 的 method 两种取值:**GET 把数据拼在 URL 后面、可见且有长度限制;POST 把数据放请求体、不显示在地址栏**。敏感数据、上传文件必须用 POST。**

- GET 提交后地址栏形如 /login?user=alex&pwd=123:参数以 ? 拼在 action 后、多个参数用 & 相连,密码直接暴露在 URL 里
- GET 受 URL 长度限制(几 KB),会被浏览器缓存、能被收藏成书签;POST 理论上没有大小限制
- POST 的数据放在**请求体**中,地址栏看不到,相对安全:登录密码、身份证号等敏感信息一律 POST
- **上传文件必须 POST + enctype="multipart/form-data"**,GET 根本带不了文件内容
- 语义区别:GET 是"要数据"(刷新重发无警告),POST 是"交数据"(刷新会提示重复提交),所以查询用 GET、增删改用 POST

```html
<!-- GET:数据拼在 URL 后,适合搜索、筛选 -->
<form action="/search" method="get">
    <input type="text" name="kw">
    <input type="submit" value="搜索">
</form>
<!-- POST:数据放请求体,适合注册、登录、上传 -->
<form action="/register" method="post" enctype="multipart/form-data">
    <input type="password" name="pwd">
    <input type="file" name="avatar">
    <input type="submit" value="注册">
</form>
```

*GET 与 POST 的典型使用场景*

## 📖 CSS

> 🎬 对应课程:前端阶段(选择器、盒子模型、浮动、定位、flex)

### 1. CSS引入方式与注释
> 🎬 对应视频:P601

**CSS 有**三种引入方式:行内式 style 属性、内嵌式 `<style>` 标签、外链式 `<link>` 标签**,注释只有 `/* */` 一种。**

- 行内式:`<p style="color: red;">`,只作用于当前标签,权重最高(1000),尽量少用
- 内嵌式:写在 `<head>` 里的 `<style>` 标签中,只作用于当前页面
- 外链式:`<link rel="stylesheet" href="style.css">`,结构与样式分离,**最推荐**
- CSS 注释只有 `/* 注释 */`,没有 // 这种单行注释

```html
<link rel="stylesheet" href="style.css">  <!-- 外链式 -->
<style>
    /* 内嵌式 */
    p { color: red; }
</style>
<p style="color: blue;">行内式,权重最高</p>
```

### 2. 选择器与优先级
> 🎬 对应视频:P602~P604、P607、P610

**基础选择器:标签 / 类(`.`)/ id(`#`)/ 通用(`*`);后代用**空格**、子代用 `>`、群组用**逗号**、交集连写;权重 **行内1000 > id100 > class10 > 标签1,!important 最高**。**

- 标签选择器 `p{}` 命中所有 p;类选择器 `.active{}` 命中 class 含 active 的元素,最常用
- id 选择器 `#top{}` 命中唯一元素,同一个 id 在一个页面里只该出现一次
- 后代选择器 `.box p{}` 选中 box 里**所有层级**的 p;子代选择器 `.box > p{}` 只选**直接子级** p
- 群组选择器 `h1, p{}` 用逗号同时选中多个;交集选择器 `p.active{}` 连写,既是 p 又有 active 类
- 伪类 `:hover` 鼠标悬停、`:first-child` 第一个子元素;伪元素 `::after` 在元素内容后面插入内容
- 权重从高到低:!important > 行内样式(1000) > id(100) > class/伪类(10) > 标签(1);权重相同时后写的覆盖先写的

```html
<style>
    p { color: gray; }          /* 标签 权重 1 */
    .active { color: red; }     /* 类   权重 10 */
    #top { color: blue; }       /* id   权重 100,最终生效 */
</style>
<p id="top" class="active">我是蓝色</p>
```

*选择器权重比较*

### 3. 盒子模型
> 🎬 对应视频:P617

**盒子 = **content + padding + border + margin**;默认标准盒模型 width 只含 content,`box-sizing: border-box` 让 width 包含 padding 和 border。**

- padding 内边距:内容与边框的距离,**会把盒子撑大**;margin 外边距:盒子与盒子之间的距离
- 标准盒模型(默认 content-box):实际占宽 = width + padding×2 + border×2
- IE盒模型:设置 `box-sizing: border-box` 后,width 已经包含 content + padding + border,布局更可控
- **margin 塌陷(合并)**:上下相邻元素的 margin 会合并取较大值;嵌套时子元素的 margin-top 会把父元素一起带下去
- margin 可以为负值,padding 不允许负值;`margin: 0 auto` 让块级盒子水平居中

```css
.box {
    width: 200px;            /* content-box 下实际宽 = 200 + 10*2 + 5*2 = 230px */
    padding: 10px;
    border: 5px solid #000;
    box-sizing: border-box;  /* 加上后 200px 已包含 padding 和 border */
    margin: 0 auto;          /* 水平居中 */
}
```

*盒子模型与box-sizing*

### 4. display 与三种隐藏方式
> 🎬 对应视频:P616、P626

**display 控制显示模式:block 独占一行、inline 行内、inline-block 行内块、none 隐藏;三种隐藏:**none 不占位、visibility:hidden 占位不可见、opacity:0 占位透明但可交互**。**

- display:block 转块级(独占一行可设宽高);inline 转行内(宽高失效);inline-block 行内块(同行显示又可设宽高)
- display:none:元素**彻底消失不占位**;visibility:hidden:看不见但**占着原来的位置**
- opacity:0:完全透明但占位,而且**还能响应点击等交互**;visibility:hidden 不能交互
- display:none 的显示/隐藏切换会触发重排(reflow),visibility 和 opacity 只触发重绘,切换更流畅

```css
.a { display: none; }       /* 不占位 */
.b { visibility: hidden; }  /* 占位,不可见 */
.c { opacity: 0; }          /* 占位,透明,可点击 */
span.btn { display: inline-block; width: 80px; height: 30px; } /* 行内块可设宽高 */
```

### 5. 浮动与清除浮动
> 🎬 对应视频:P618、P621

**`float: left/right` 让元素脱离文档流去排队,会导致**父级高度塌陷**;清除浮动常用 `clear: both`、父级 `overflow: hidden`(触发BFC)或 `::after` 伪元素。**

- 浮动最初用于文字环绕图片,后来大量用于横向布局;浮动元素**不占文档流的位置**
- 父元素没设高度、子元素又全部浮动时,父元素高度变成 0,这就是**父级塌陷**
- 方法一:在浮动元素后面加一个设置 `clear: both` 的元素(隔墙法)
- 方法二:父元素设置 `overflow: hidden`,触发 BFC 后父元素会把浮动的子元素包住
- 方法三:给父元素加 `::after` 伪元素设置 clear:both(经典 clearfix 写法,最常用)

```css
.clearfix::after {
    content: "";
    display: block;
    clear: both;
}
.left { float: left; width: 200px; height: 100px; }
```

*clearfix 清除浮动*

### 6. position 定位与 flex 布局
> 🎬 对应视频:P623~P624

**position:relative **不脱标**、absolute **相对最近的定位祖先脱标**、fixed **相对视口脱标**;flex 用 `display: flex` + `justify-content`(主轴)+ `align-items`(交叉轴)。**

- static 是默认值;relative 相对**自己原来的位置**偏移,不脱标,原位置仍保留
- absolute 脱离文档流,相对**最近的 position 非 static 的祖先**定位,找不到就一直向上找到浏览器窗口
- fixed 脱离文档流,相对**浏览器可视区域**定位,页面滚动它也不动,常用于返回顶部按钮
- flex:`display: flex` 后子元素默认**沿主轴(水平方向)排列**;justify-content 常用值 flex-start / center / space-between / space-around
- align-items 控制交叉轴(垂直方向)对齐,center 垂直居中最常用;子元素设置 `flex: 1` 平分剩余空间

```css
.container {
    display: flex;
    justify-content: space-between; /* 主轴:两端对齐 */
    align-items: center;            /* 交叉轴:垂直居中 */
}
.item { flex: 1; }  /* 子元素平分剩余空间 */
.top-btn { position: fixed; right: 20px; bottom: 20px; } /* 固定在视口右下角 */
```

### 7. 字体属性与文字属性
> 🎬 对应视频:P611~P613

**字体三件套:**font-family 字体、font-size 大小、font-weight 加粗**;文字排版:**color 颜色、text-align 水平对齐、line-height 行高、text-decoration 装饰线**。**

- `font-family: "Microsoft YaHei", sans-serif;` 逗号分隔多个字体依次兜底;`font-size` 常用 px 单位
- `font-weight` 常用 normal(400)/bold(700),也可以直接写数字 100~900,数值越大越粗
- `text-align: left/center/right` 让**容器内的文字水平对齐**;让盒子自身居中是 `margin: 0 auto`,两者别混
- `line-height: 50px` 配合 `height: 50px` 可以让**单行文字垂直居中**(行高等于盒高)
- `text-decoration: none` 去掉 a 标签默认下划线;`text-indent: 2em` 首行缩进两个字符

```css
p {
    font-family: "Microsoft YaHei", sans-serif;
    font-size: 16px;
    font-weight: bold;      /* 700 */
    color: #333;
    text-align: center;     /* 文字水平居中 */
    line-height: 50px;      /* 行高50px,配合height让单行文字垂直居中 */
    text-decoration: none;
    text-indent: 2em;       /* 首行缩进2字符 */
}
```

*常用字体/文字属性*

### 8. 背景与边框
> 🎬 对应视频:P614~P615

**背景图片**默认平铺铺满**,可用 `background: 颜色 url() no-repeat center/cover` 一次性设置;边框三要素**宽度 样式 颜色**,样式常用 solid/dashed/dotted,`border-radius` 做圆角。**

- `background-color` 颜色三种写法:英文单词、`#ff0000` 十六进制、`rgba(255,0,0,.5)`(a 控制透明度)
- `background-image: url(bg.png)` 默认**平铺重复**铺满容器;`background-repeat: no-repeat` 取消平铺
- `background-position: center top` 定位图片;`background-size: cover` 等比放大铺满容器(多余部分裁剪),`contain` 完整显示(可能留白)
- `border: 1px solid #ddd;` 按**宽度、样式、颜色**顺序写;dashed 虚线、dotted 点线;也可拆成 border-width/style/color 分别设置
- `border-radius: 10px` 圆角,设成 `50%` 可把正方形变成圆;清除边框写 `border: none` 或 `border: 0`

```css
.banner {
    width: 600px;
    height: 300px;
    background: #f5f5f5 url(banner.png) no-repeat center/cover;
}
.card {
    border: 1px dashed #999;   /* 虚线边框 */
    border-radius: 8px;
}
```

*背景与边框常用写法*

### 9. 溢出属性 overflow 与文字省略
> 🎬 对应视频:P622

**overflow 管"内容装不下怎么办":**visible 溢出照常显示(默认)、hidden 裁掉、scroll 一直有滚动条、auto 装不下才出滚动条**;单行文字省略号三件套:overflow hidden + white-space nowrap + text-overflow ellipsis。**

- `visible`(默认):超出部分原样显示在盒子外面;`hidden`:超出部分**直接裁掉**,不显示滚动条
- `scroll`:不管装不装得下,**横竖滚动条都显示**;`auto`:装得下不显示,装不下才自动出现
- hidden 的隐藏是"裁剪":下拉菜单、绝对定位超出父容器的部分都会被一起裁掉,使用前要想清楚层级
- 单行文字省略三件套(缺一不可):`overflow: hidden; white-space: nowrap; text-overflow: ellipsis;`,且盒子要有固定宽度
- 多行省略的简单思路:固定高度 + overflow hidden;精确控制可用 -webkit-line-clamp(需要 webkit 内核支持)

```css
.title {
    width: 200px;              /* 必须有固定宽度 */
    overflow: hidden;
    white-space: nowrap;       /* 不换行 */
    text-overflow: ellipsis;   /* 超出显示省略号 */
}
```

*单行文字超出显示省略号*

### 10. z-index 层级与模态框案例
> 🎬 对应视频:P625

****z-index 只有配合定位(position 非 static)才生效**,数值大的盖住数值小的;模态框 = 页面内容(1)+ 全屏半透明遮罩(99)+ 居中弹窗(999)三层叠加。**

- 元素重叠时默认后写的盖住先写的;给定位元素设置 `z-index: 数字` 改变上下顺序,数字越大越靠上
- z-index 对**没有设置 position 的普通元素无效**;absolute/fixed/relative 元素之间才能比较层级
- 模态框三层结构:页面内容(z-index:1)→ 遮罩层(fixed 铺满全屏、半透明黑底,z-index:99)→ 弹窗盒子(fixed 居中,z-index:999)
- 遮罩层和弹窗是两个独立的兄弟元素:点击弹窗不会触发遮罩的事件,所以"点遮罩关闭、点弹窗不关"靠分别绑定事件实现
- 显示/隐藏用 display:none 与 block 切换(jQuery 里就是 .show()/.hide()),配合 z-index 层级完成弹出效果

```css
.content { position: relative; z-index: 1; }
.shade {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, .4);   /* 半透明黑色遮罩 */
    z-index: 99;
}
.modal {
    position: fixed; left: 50%; top: 50%;
    transform: translate(-50%, -50%);
    width: 300px; height: 200px; background: #fff;
    z-index: 999;   /* 弹窗在最上层 */
}
```

*模态框三层结构与 z-index*

### 11. 伪类与伪元素详解
> 🎬 对应视频:P608~P609

**伪类用**单冒号**表示元素的"状态":`:hover` 悬停、`:focus` 聚焦、`:first-child` 第一个子元素;伪元素用**双冒号**创建"虚拟节点":`::before/::after` 必须写 content 才会渲染。**

- a 链接四态::link 未访问、:visited 已访问、:hover 悬停、:active 按下,必须按 LVHA 顺序书写,乱序会相互覆盖
- 表单相关::focus 获得焦点的输入框(做高亮边框)、:checked 被选中的 radio/checkbox、:disabled 禁用的控件
- 结构伪类::first-child 第一个子元素、:last-child 最后一个、:nth-child(2) 第 2 个、:nth-child(odd/even) 奇偶行,隔行变色全靠它
- ::before 在内容**前**插入、::after 在内容**后**插入,必须写 content(哪怕 content: "")才显示,默认是行内元素
- 伪元素经典应用:clearfix 清浮动、给段落加装饰性图标、自定义序号;CSS3 规定伪元素用双冒号,旧的 :before 写法仍兼容

```css
/* 链接四态:按 LVHA 顺序 */
a:link { color: blue; }
a:visited { color: purple; }
a:hover { color: red; }
a:active { color: orange; }

/* 伪元素:content 必须写 */
.tip::before { content: "提示:"; color: #999; }
input:focus { border-color: #409eff; }   /* 聚焦高亮 */
li:nth-child(even) { background: #f5f5f5; }  /* 隔行变色 */
```

*伪类四态、结构伪类与 ::before*

### 12. 文档流与脱离文档流
> 🎬 对应视频:P618、P623~P624

**标准文档流:块级**纵向排列**、行内横向排列。**float、position:absolute、position:fixed 三种方式会脱离文档流**,relative 不脱标;脱离后不再占据原位置,父级也"看不见"它。**

- 文档流是浏览器默认的排版规则:从上到下、从左到右,块级独占一行、行内挨着排,一行放不下自动换行
- 三种脱离文档流的方式:浮动 float、绝对定位 absolute、固定定位 fixed;relative 只是"看着移走",原位置保留,属于不脱标
- 浮动脱流但**不脱文字流**:旁边的文字会绕着浮动元素排,这就是"文字环绕图片"效果的实现原理
- absolute/fixed 是完全脱流:后面的元素会顶上来占据原来的位置,文字也不环绕,元素之间可以随意重叠
- 脱流元素**不再撑开父元素的高度**(父级塌陷的根源);定位元素发生重叠时要靠 z-index 决定谁在上面

```css
.box1 { float: left; }        /* 脱流不脱文字流,文字环绕它 */
.box2 { position: absolute; }  /* 完全脱流,不占位置,可重叠 */
.box3 { position: relative; left: 20px; }  /* 不脱标,原位置保留 */
```

*三种脱流方式与 relative 对比*

### 13. 透明度 opacity 与 rgba
> 🎬 对应视频:P626

**opacity 取值 **0~1**,作用于**整个元素连同所有子元素**;rgba 的第四位 alpha 只让**当前这一层颜色**半透明,内容不受影响。做遮罩用 rgba,慎用 opacity。**

- opacity: 1 不透明、0.5 半透明、0 完全透明;取值是 0~1 的小数,没有单位,写成 50 无效
- opacity 有"连坐"效果:父元素设 0.5,里面的文字、图片整体跟着透明,子元素自己再设 opacity: 1 也救不回来
- rgba(0,0,0,.4) 只影响这一条声明对应的颜色(背景或文字),盒子整体不透明,里面的内容依然清晰
- 模态框遮罩标准写法:遮罩背景用 rgba 半透明、弹窗内容放遮罩外面,保证文字清楚;整层 opacity 会把内容一起变虚
- opacity: 0 与 visibility: hidden 一样"占位不可见",但 opacity:0 的元素**仍可点击、可触发事件**;配合 transition 可做淡入淡出

```css
.mask {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, .4);  /* 推荐:只有遮罩背景半透明 */
}
.mask2 {
    opacity: 0.4;                 /* 整个元素连同内容一起透明,慎用 */
    transition: opacity .3s;      /* 配合过渡做淡入淡出 */
}
```

*rgba 做遮罩 vs opacity 整体透明*

## 📖 JavaScript 与 jQuery

> 🎬 对应课程:前端阶段(JS基础、DOM/BOM、ES6、jQuery、Bootstrap)

### 1. JS基础:变量与数据类型
> 🎬 对应视频:P628~P629、P632~P638

**声明变量用 **var(函数作用域)、let(块级作用域)、const(常量)**;基本类型 number/string/boolean/null/undefined,用 `typeof` 检测类型。**

- var:函数作用域、可重复声明、存在变量提升;let/const(ES6):块级作用域,同一作用域不可重复声明
- const 声明时必须赋值且**不能重新赋值**,但对象的属性仍然可以修改
- 基本类型:number(不分整型浮点型)、string、boolean、null(空值)、undefined(声明了没赋值);引用类型:object(数组、函数也算)
- `typeof null` 返回 "object"(历史遗留 bug),`typeof undefined` 返回 "undefined",`typeof 数组` 也返回 "object"
- null 一般是主动赋的“空值”,undefined 表示“还没赋值”

```js
var a = 10;          // 函数作用域
let b = 20;          // 块级作用域
const c = 30;        // 常量,不能重新赋值
console.log(typeof a);         // "number"
console.log(typeof null);      // "object"
console.log(typeof [1, 2]);    // "object"
```

### 2. 运算与流程控制
> 🎬 对应视频:P639~P640

****== 会隐式转换类型,=== 既比值又比类型**;`1 + "1"` 得 "11"(字符串拼接);条件分支用 if,简单判断用三元 `条件 ? 值1 : 值2`。**

- `"5" == 5` → true(== 把字符串转成数字再比);`"5" === 5` → false(类型不同直接 false)
- `+` 遇到字符串就是拼接:`1 + "1" = "11"`;`-` 会强制转数字:`1 - "1" = 0`
- 假值只有:`0`、`""`、`null`、`undefined`、`NaN`,其余都为真
- JS 代码块用大括号 `{}` 包裹(不像 Python 用缩进)
- 三元表达式:`var max = a > b ? a : b;`

```js
console.log("5" == 5);   // true
console.log("5" === 5);  // false
console.log(1 + "1");    // "11"
console.log(1 - "1");    // 0
var score = 85;
var level = score >= 60 ? "及格" : "不及格";  // 及格
```

### 3. 函数与数组方法
> 🎬 对应视频:P641~P642

**函数用 function 声明或箭头函数 `=>`(箭头函数**没有自己的 this**);数组方法:`push/pop` 尾部增删、`forEach` 遍历、`map` 映射、`filter` 过滤。**

- 函数声明 `function add(x, y) { return x + y; }`;函数是对象,可以赋值给变量、当参数传递
- 箭头函数 `(x, y) => x + y`:单个表达式可省略 return 和大括号;它的 this 由**定义的位置**决定
- `push(4)` 尾部加、`pop()` 尾部删、`unshift/shift` 头部加删,这些方法都会**改变原数组**
- `forEach` 只遍历不返回;`map` 对每个元素加工后**返回新数组**;`filter` 按条件筛选**返回新数组**,两者都不改原数组
- 对象字面量 `var obj = { name: "alex", age: 18 };`,取值 `obj.name` 或 `obj["name"]`

```js
var arr = [1, 2, 3, 4];
var doubled = arr.map(function (v) { return v * 2; });      // [2, 4, 6, 8]
var odds = arr.filter(function (v) { return v % 2 === 1; }); // [1, 3]
var add = (x, y) => x + y;   // 箭头函数
console.log(doubled, odds, add(1, 2));
```

### 4. DOM操作与事件
> 🎬 对应视频:P654~P658、P661~P662

**`document.getElementById` / `querySelector` 获取元素,**innerText 当纯文本、innerHTML 当 HTML 解析**,`classList` 操作类名,`addEventListener` 绑定事件,冒泡用 `e.stopPropagation()` 阻止。**

- `document.getElementById("box")` 按 id 取单个元素;`document.querySelector(".box p")` 支持 CSS 选择器,返回第一个匹配
- innerText:按**纯文本**读写;innerHTML:会**解析 HTML 标签**(插入用户输入有 XSS 风险,要小心)
- 改行内样式 `box.style.color = "red"`;操作类名 `box.classList.add/remove/toggle("active")`
- 创建节点 `document.createElement("div")`,插入父元素 `parent.appendChild(el)`
- 事件绑定:`el.onclick = fn` 同一事件只能绑一个;`el.addEventListener("click", fn)` 可以绑多个
- 事件冒泡:子元素触发事件会**逐层向父元素传播**;`e.stopPropagation()` 阻止冒泡,`e.preventDefault()` 阻止默认行为(比如 a 标签跳转)

```js
var box = document.getElementById("box");
box.innerText = "<b>这是文本</b>";   // 标签原样显示出来
box.innerHTML = "<b>加粗</b>";       // 标签被解析,文字加粗
box.classList.add("active");
box.addEventListener("click", function (e) {
    e.stopPropagation();  // 阻止事件冒泡到父元素
});
```

### 5. BOM 与定时器
> 🎬 对应视频:P649~P653

**BOM 操作浏览器,核心对象是 `window`;`setTimeout` **只执行一次**、`setInterval` **循环执行**,分别用 `clearTimeout` / `clearInterval` 清除。**

- window 是浏览器的全局对象,全局变量和函数都是它的属性,调用时可以省略 window.
- `window.alert()` 弹警告框、`confirm()` 确认框返回 true/false、`prompt()` 输入框返回输入内容
- `setTimeout(fn, 3000)`:3000 毫秒后执行**一次**;`setInterval(fn, 2000)`:每隔 2000 毫秒执行**一次,反复执行**
- 定时器会返回一个 id,用 `clearTimeout(id)` / `clearInterval(id)` 取消;轮播图切换前先 clearInterval,否则定时器叠加会越切越快
- `window.location.href` 可以读取当前地址,赋值则跳转页面

```js
var t = setTimeout(function () {
    console.log("3秒后只执行一次");
}, 3000);
clearTimeout(t);  // 取消

var n = 0;
var s = setInterval(function () {
    n++;
    if (n >= 5) clearInterval(s);  // 执行5次后停止
    console.log(n);
}, 1000);
```

### 6. ES6、jQuery 与 Bootstrap 栅格
> 🎬 对应视频:P663~P666、P689

**ES6:模板字符串用**反引号**包裹、`${}` 嵌变量,解构赋值,扩展运算符;jQuery 用 `$` 选择器 + **链式操作**;Bootstrap 栅格一行 **12 列**,`col-md-N` 指定占几列。**

- 模板字符串:反引号包裹,`${name}` 直接嵌变量,还支持换行
- 解构赋值:`var { name, age } = obj;` 按属性名取、`var [a, b] = arr;` 按位置取;扩展运算符 `...arr` 展开数组,`[...a, ...b]` 合并
- jQuery:`$("p")` 选中所有 p、`$("#box")` 选中 id;方法返回 jQuery 对象所以能**链式调用**,如 `$("#box").addClass("on").css("color", "red")`
- `$("li").each(function (i, el) {...})` 遍历元素;`$.ajax({ url, type, data, success })` 发送异步请求
- Bootstrap 栅格:`.container > .row > .col-md-N`,一行固定 **12 列**,N 表示占几列,超过 12 自动换行

```js
var obj = { name: "alex", age: 18 };
console.log(`我叫${obj.name},今年${obj.age}岁`);

$.ajax({
    url: "/api/user",
    type: "get",
    data: { id: 1 },
    success: function (res) {
        console.log(res);
    }
});
```

*ES6模板字符串与$.ajax*

### 7. jQuery 筛选器与筛选方法
> 🎬 对应视频:P667~P670

**基本筛选器 `:first` `:eq(2)` `:odd` 在**选中结果里再挑下标**;筛选方法 `.first()/.eq()/.parent()/.children()/.siblings()/.next()/.prev()` 从**当前对象出发找亲戚**。**

- 基本筛选器:`:first` 第一个、`:last` 最后一个、`:eq(2)` 下标为 2、`:even` 偶数下标(0,2…)、`:odd` 奇数下标(1,3…)
- 其他筛选器:`:not(选择器)` 排除、`:contains("文字")` 按文本选;表单筛选器 `:checked`、`:selected`、`:input` 很常用
- 筛选方法:`.first()/.last()/.eq(n)` 取某一个;`.filter(选择器)` 在结果里再过滤;`.not(选择器)` 排除
- 找亲戚:`.parent()` 父元素、`.children()` 直接子元素、`.find(选择器)` 所有后代里找、`.siblings()` 所有兄弟(**不含自己**)、`.next()/.prev()` 相邻元素
- `$("li").eq(2)` 等价于 `$("li:eq(2)")`,方法写法可以接变量、更适合链式调用;`.hasClass("x")` 判断类名是否存在,返回 true/false(不是 jQuery 对象,不能再链式)

```js
$("li:first").css("color", "red");          // 第一个 li
$("li:odd").css("background", "#eee");      // 下标 1,3,5…
$("#box").children("p").addClass("on");     // 直接子元素 p
$(".item").siblings().hide();               // 兄弟隐藏,自己不动
$("#box").find("a").attr("target", "_blank");
```

### 8. jQuery 文档处理(取值与节点增删)
> 🎬 对应视频:P675~P676

**取值三兄弟:**`.html()` 带 HTML、`.text()` 纯文本、`.val()` 表单值**;节点操作:**append/prepend 插到内部末尾/开头、remove 连自己删、empty 只清内部、clone 克隆**。**

- `.html()` 读写 innerHTML(标签被解析成真标签);`.text()` 读写纯文本(标签原样显示);`.val()` 读写 input/select/textarea 的值
- `A.append(B)`:B 插到 **A 内部末尾**;`B.appendTo(A)` 效果一样只是主宾互换;`prepend/prependTo` 插到内部开头
- `A.before(B)` / `A.after(B)`:把 B 插到 A 的**外面**、兄弟位置(前面/后面)
- `.remove()`:元素**连同内容、事件一起删掉**;`.empty()`:只清空内部子元素,**保留自己**;做"添加行/删除行"功能常用
- `.clone()` 克隆节点但**默认不复制事件**,`.clone(true)` 连事件一起复制;新节点插入前要先创建:`$("<li>新项</li>")`

```js
$("#tip").html("<b>加粗</b>");    // 标签被解析
$("#tip").text("<b>加粗</b>");    // 标签原样显示
var $li = $("<li>新项</li>");
$("ul").append($li);              // 插到 ul 内部末尾
$li.appendTo("ul");               // 等价写法
$("ul li:first").remove();        // 删除第一个 li
$("ul").empty();                  // 清空 ul 内容,ul 还在
```

### 9. jQuery 事件绑定与事件委托
> 🎬 对应视频:P677~P679、P682~P684

**统一用 **`.on("事件名", fn)` 绑事件**(可绑多个互不覆盖),`.off()` 解绑;**事件委托:`$(父).on("click", "子选择器", fn)`**,动态新增的子元素也能触发;`return false` 同时阻止冒泡和默认行为。**

- `$("li").on("click", fn)`:同一元素可绑多个同名事件依次执行;简化写法 `$("li").click(fn)` 效果相同
- **事件委托**:事件绑在**稳定存在的父元素**上,第二个参数指定真正点击的子元素;之后动态 append 进来的 li 不用重新绑定也能响应
- 阻止冒泡 `e.stopPropagation()`;阻止默认行为(a 跳转、form 提交)`e.preventDefault()`;**`return false` 两个都阻止**
- `.off("click")` 解绑事件;`.one("click", fn)` 绑定后**只触发一次**自动解绑
- `.trigger("click")` 自动触发事件;`.hover(fn1, fn2)` 相当于 mouseenter 和 mouseleave 各绑一个

```js
$("#add").on("click", function () {
    $("ul").append("<li>新列表项</li>");   // 新 li 也能响应下面的委托事件
});
$("ul").on("click", "li", function () {   // 事件委托:绑在父元素 ul 上
    $(this).toggleClass("on");
});
$("a.delete").on("click", function () {
    return false;   // 既阻止跳转又阻止冒泡
});
```

*动态列表的事件委托*

### 10. Bootstrap 常用组件(导航栏/按钮/表单/模态框)
> 🎬 对应视频:P688、P692~P693、P695~P698

**Bootstrap 是"套 class 就能用"的样式库:**.navbar 导航栏、.btn btn-primary 按钮、.form-control 表单控件、.modal 模态框(配合 data-toggle 触发)**,小图标用 glyphicon 字体图标。**

- 导航栏:`<nav class="navbar navbar-default">` 外壳 + `.container` 容器 + `.navbar-header`,换 `navbar-inverse` 得到黑底反色导航
- 按钮:`.btn` 基类 + `.btn-primary`(蓝)/`.btn-success`(绿)/`.btn-danger`(红)定颜色;`.btn-group` 把一组按钮拼在一起
- 表单:`.form-group` 包住 label 和 input,`.form-control` 让输入框占满一行且样式统一,`.form-inline` 做一行式表单
- 模态框:隐藏的 `.modal` 容器内含 `.modal-dialog > .modal-content`,给按钮加 `data-toggle="modal" data-target="#myModal"` 即可弹出,点遮罩默认自动关闭
- 字体图标:`<span class="glyphicon glyphicon-search"></span>`,本质是字体不是图片,可以用 CSS 的 color/font-size 调整样式

```html
<button class="btn btn-primary" data-toggle="modal" data-target="#myModal">新增</button>

<div class="modal fade" id="myModal">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h4 class="modal-title">新增书籍</h4>
            </div>
            <div class="modal-body">
                <input type="text" class="form-control" placeholder="书名">
            </div>
            <div class="modal-footer">
                <button class="btn btn-success">确定</button>
            </div>
        </div>
    </div>
</div>
```

*按钮触发模态框*

### 11. 字符串常用方法
> 🎬 对应视频:P634~P635

**字符串**不可变**,所有方法都返回新值:`.length` 取长度、`indexOf` 找下标、`slice` 切片、`split` 转数组、`trim` 去两端空白、`replace` 替换、`toUpperCase/toLowerCase` 转大小写。**

- length 是**属性**不是方法,写 s.length 不加括号;字符串一旦创建不能修改,调用任何方法都返回新字符串
- charAt(i) 或 s[i] 取指定下标字符;indexOf("x") 返回第一次出现的下标,**找不到返回 -1**,常用来判断"是否包含"
- slice(start, end) 包头不包尾,end 省略就切到结尾,支持负数(从后往前数);substring 类似但不支持负数
- split("分隔符") 把字符串**切成数组**:"a,b,c".split(",") 得 ["a","b","c"],和数组的 join("分隔符") 正好互逆
- trim() 去掉两端空白(表单校验先 trim 再判空);replace 默认**只替换第一个**,要全部替换得配合正则 /x/g

```js
var s = " Hello World ";
console.log(s.length);                 // 13(属性,不加括号)
console.log(s.trim());                 // "Hello World" 去两端空白
console.log(s.trim().toUpperCase());   // "HELLO WORLD"
console.log("hello".indexOf("l"));     // 2,找不到返回 -1
console.log("a,b,c".split(","));       // ["a", "b", "c"] 切成数组
console.log("2026-01-01".replace("-", "/"));  // "2026/01-01" 只换第一个
```

### 12. 内置对象:Date 日期、JSON 与 RegExp 正则
> 🎬 对应视频:P643~P645

**JS 三类常用内置对象:**Date 处理日期与时间戳、JSON 负责"对象⇄字符串"互转、RegExp 正则做模式匹配**,数据传输和表单校验全靠它们。**

- new Date() 不传参取当前时间;getFullYear() 年、getMonth() **返回 0~11 记得 +1**、getDate() 日、getDay() 星期(0 是周日)、getHours/getMinutes/getSeconds 时分秒
- Date.now() 或 +new Date() 得到**毫秒时间戳**:两次时间戳相减就是耗时,常用于统计程序运行时间
- JSON.stringify(obj):对象 → JSON 字符串(序列化);JSON.parse(str):JSON 字符串 → 对象(反序列化),对应 Python 的 json.dumps / json.loads
- 正则两种写法:字面量 /模式/标志 或 new RegExp("模式");标志 i 忽略大小写、g 全局匹配;test() 返回 true/false,exec() 返回匹配详情或 null
- 常用校验正则:手机号 /^1[3-9]\d{9}$/,配合 test() 在表单提交前校验格式

```js
var d = new Date();
console.log(d.getFullYear(), d.getMonth() + 1, d.getDate());  // 月要+1
console.log(Date.now());              // 毫秒时间戳

var obj = { name: "alex", score: 90 };
var str = JSON.stringify(obj);        // 对象 → 字符串
console.log(str, typeof str);         // '{"name":"alex","score":90}' string
console.log(JSON.parse(str).name);    // alex

var re = /^1[3-9]\d{9}$/;             // 手机号正则
console.log(re.test("13812345678"));  // true
console.log(re.test("12345678901"));  // false
```

*Date、JSON、RegExp 三件套*

### 13. 页面加载:window.onload 与 $(function(){})
> 🎬 对应视频:P685

**原生 **window.onload 等图片等全部资源加载完**才触发、只能绑一个(后写覆盖先写);jQuery 的 **$(function(){}) 等 DOM 树建好就执行**,不用等图片、可写多个,实际开发首选。**

- script 写在 head 里时 body 标签还没解析,直接取元素得到 null,所以操作 DOM 的代码必须等页面加载完成
- window.onload = fn:等**所有资源**(DOM、图片、iframe)加载完才执行,触发最晚;重复赋值会**覆盖**,只保留最后一个
- $(function(){}) 是 $(document).ready(fn) 的简写:**DOM 树构建完成**就触发,不等图片下载,因此比 onload 先执行
- $(fn) 可以写**多个**依次执行、互不覆盖,多人协作时各写各的 ready 不会冲突
- 原生等价物是 document.addEventListener("DOMContentLoaded", fn);更简单的办法是把 script 标签放到 body 最底部

```js
// 原生:全部资源加载完才触发,后写的覆盖先写的
window.onload = function () {
    console.log("onload:图片等资源也都加载完了");
};

// jQuery:DOM 就绪即执行,可写多个,推荐
$(function () {
    console.log("ready:DOM 建好就执行,先于 onload");
});
```

*两种页面加载时机对比*

### 14. jQuery 动画效果
> 🎬 对应视频:P686

**jQuery 内置三组动画:**show()/hide()/toggle() 显示隐藏、slideDown/slideUp 滑动、fadeIn/fadeOut 淡入淡出**,自定义用 `animate({样式: 目标值}, 时长, 回调)`;连续调用会排队,用 stop() 打断。**

- show(毫秒)/hide(毫秒)/toggle(毫秒):同时动画 width、height、opacity 再切换 display;不传参数则"秒切"没有过渡过程
- slideDown/slideUp/slideToggle:从上往下展开、从下往上收起,适合做下拉菜单;fadeIn/fadeOut/fadeToggle 淡入淡出,fadeTo(时长, 透明度) 渐变到指定透明度
- animate(目标样式对象, 速度, 回调):自定义动画,样式属性写**驼峰**如 marginLeft、fontSize;transform 这类属性不能直接用 animate 改
- jQuery 动画有**排队机制**:连续动画语句按顺序依次执行,事件里反复触发会积压延迟,动画前先 stop() 清掉队列
- 回调函数在动画**完成后**执行,常用于"动画结束后再弹提示";这些方法是原生 JS 没有的封装,也是 jQuery 当年流行的原因之一

```js
$("#box").hide(1000);       // 1秒内收起
$("#box").show(1000);       // 展开显示
$("#box").slideDown(500);   // 下拉展开
$("#box").fadeTo(500, 0.5); // 渐变到半透明
$("#box").animate({ marginLeft: 200 }, 800, function () {
    console.log("动画结束才执行我");
});
$("#box").stop(true);       // 清空动画队列,防止叠加
```

*jQuery 常用动画方法*

## 📖 课后作业（前端）

> 🎬 对应课程:Day57 jQuery练习题(P673)、Day58 图书管理系统前端页面搭建(P699),练习按作业主题原创编写

### 1. 作业清单与完成顺序
> 🎬 对应视频:P673、P699

**前端阶段两大作业:**jQuery练习题(Day57,选择器/筛选器/样式操作综合)→ 图书管理系统前端页面搭建(Day58,HTML+CSS+Bootstrap+jQuery 串起来)**,先练零件再装整机。**

- Day57 jQuery练习题:全选反选、表格隔行变色、tab切换 —— 综合考选择器、筛选器、css()/prop() 操作,对应本站前端阶段「jQuery」各小节
- Day58 图书管理系统前端:登录页(Bootstrap 栅格居中)、图书列表页(表格+按钮)、新增图书表单 —— 对应「HTML/CSS/Bootstrap」各章
- 列表页交互:隔行变色、全选反选、删除行,把 jQuery 练习题的成果直接复用进项目,体会「作业为项目服务」
- 先静态后动态:HTML 结构和 Bootstrap 样式调好,再用 jQuery 加交互,别一上来就写 JS
- 做完到「题库练习」刷前端各章的题自测,重点补盒子模型计算和 DOM 取值赋值

```python
<!-- 作业目录结构建议 -->
<!-- my_book_ui/
  css/       自己写的少量样式
  js/        交互脚本(全选反选/删行都在这)
  login.html 登录页
  list.html  图书列表页
  add.html   新增图书 -->
```

---

**系列目录 / 工具获取方式见文末 👇**