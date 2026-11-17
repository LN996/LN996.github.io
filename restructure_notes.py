# -*- coding: utf-8 -*-
"""把 hexo-blog/source/_posts/python-*.md 改造成"我自己的笔记":

1. 分类从统一的「Python学习笔记」拆成按知识点划分的栏目
2. 删除别人的视频链接、获取方式推广、课程水印
3. 标题去掉"逐集精讲/课堂"等课程痕迹

python-00(原课程推广导读)不处理,由人工重写为个人目录页。
重复执行安全:每次都从原始笔记 D:/laonanhai-xuexi/blog 重新生成。"""
import os
import re

SRC = r"D:\laonanhai-xuexi\blog"          # 原始课程笔记(不动)
DST = r"D:\laonanhai-xuexi\hexo-blog\source\_posts"

# slug -> (源文件名, 新分类, 新标题, tags)
PLAN = {
    "python-01": ("01-Python入门与数据类型.md", "Python基础", "Python 入门与数据类型", ["Python", "基础"]),
    "python-02": ("02-流程控制与文件操作.md", "Python基础", "流程控制与文件操作", ["Python", "基础"]),
    "python-03": ("03-函数与模块.md", "Python基础", "函数与模块", ["Python", "基础"]),
    "python-04": ("04-面向对象编程.md", "面向对象", "面向对象编程", ["Python", "OOP"]),
    "python-05": ("05-网络编程逐集精讲.md", "网络编程", "网络编程", ["Python", "网络"]),
    "python-06": ("06-并发编程逐集精讲.md", "并发编程", "并发编程", ["Python", "并发"]),
    "python-07": ("07-异常处理与代码模板.md", "Python基础", "异常处理与代码模板", ["Python", "基础"]),
    "python-08": ("08-经典练习与课后作业.md", "练习与代码", "经典练习题", ["Python", "练习"]),
    "python-09": ("09-MySQL数据库.md", "数据库", "MySQL 数据库", ["MySQL", "数据库"]),
    "python-10": ("10-前端三件套.md", "前端", "前端三件套:HTML/CSS/JS", ["前端", "HTML", "CSS"]),
    "python-11": ("11-Django与DRF.md", "Django", "Django 与 DRF", ["Django", "DRF"]),
    "python-12": ("12-项目实战.md", "项目实战", "项目实战", ["Django", "实战"]),
    "python-13": ("13-运维与面试.md", "运维与面试", "运维与面试", ["运维", "面试"]),
    "python-14": ("14-课堂代码精选51段.md", "练习与代码", "代码精选 51 段", ["Python", "代码"]),
}

# 含这些关键词的整行直接删掉(视频引用/推广/课程水印)
DROP_PATTERNS = [
    "对应视频", "🎬", "获取方式", "可刷题", "刷题", "学习中心", "配套",
    "系列笔记", "视频课程", "bilibili", "B站", "b23.tv", "网盘", "夸克",
    "pan.baidu", "老男孩", "逐集", "追更", "免费分享", "收藏",
]

# 从这种标题开始到下一个同级标题为止整段删除
SECTION_CUT = re.compile(r"^#{2,3}\s*(获取方式|配套工具|获取笔记|完整版).*$", re.M)

INTRO = "> 我的学习笔记,边学边记,持续修订。最后更新:2026-11。"


def clean_body(text: str) -> str:
    """清洗正文:删推广段落和水印行,替换掉开头的课程腔调。"""
    # 1. 删除"获取方式"类整段
    def cut_section(m):
        return m.group(0)  # 占位,下面用行级处理更稳
    lines = text.splitlines()
    out, cutting = [], False
    cut_level = 0
    for line in lines:
        heading = re.match(r"^(#{2,3})\s+(.*)$", line)
        if cutting:
            if heading and len(heading.group(1)) <= cut_level:
                cutting = False  # 遇到同级或更高级标题,停止删除
            else:
                continue
        if heading and re.search(r"获取方式|配套工具|获取笔记|完整版", heading.group(2)):
            cutting, cut_level = True, len(heading.group(1))
            continue
        out.append(line)
    # 2. 行级过滤:水印/视频/推广
    out = [
        l for l in out
        if not any(p.lower() in l.lower() for p in DROP_PATTERNS)
    ]
    # 3. 去掉开头的空行和残留的分隔线,统一换成个人化引言
    while out and (out[0].strip() in ("", "---", ">")):
        out.pop(0)
    return INTRO + "\n\n" + "\n".join(out).strip() + "\n"


def main():
    for slug, (src_name, category, title, tags) in PLAN.items():
        src_path = os.path.join(SRC, src_name)
        if not os.path.exists(src_path):
            print(f"[跳过] 找不到 {src_name}")
            continue
        with open(src_path, encoding="utf-8") as f:
            raw = f.read()
        # 去掉文件开头的大标题(和标题重复)
        body = re.sub(r"^#\s+.*\n+", "", raw, count=1)
        body = clean_body(body)
        # 沿用原来的发布日期(convert_notes.py 的安排:01 -> 11-01)
        n = int(slug.split("-")[1])
        date = f"2026-11-{n:02d} 09:00:00"
        front = (
            "---\n"
            f"title: {title}\n"
            f"date: {date}\n"
            "tags:\n" + "".join(f"  - {t}\n" for t in tags) +
            f"categories:\n  - {category}\n"
            "---\n\n"
        )
        dst_path = os.path.join(DST, f"{slug}.md")
        with open(dst_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(front + body)
        print(f"[完成] {slug} -> [{category}] {title}")
    print("全部处理完成")


if __name__ == "__main__":
    main()
