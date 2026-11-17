# -*- coding: utf-8 -*-
"""把 D:/laonanhai-xuexi/blog 下的课程笔记批量转换成 Hexo 博客文章。
生成文件到 source/_posts/,文件名用 python-NN 作 slug,URL 干净且顺序可控。
原始笔记不修改。"""
import os
import datetime

SRC = r"D:\laonanhai-xuexi\blog"
DST = r"D:\laonanhai-xuexi\hexo-blog\source\_posts"
CATEGORY = ["Python学习笔记"]
START_DATE = datetime.date(2026, 10, 31)  # 00 -> 10-31, 14 -> 11-14,每天一篇

# (源文件名, slug, tags, 标题覆盖)
META = [
    ("00-导读与获取方式.md",     "python-00", ["Python", "随笔"],      "Python全栈学习笔记:课程导读与目录"),
    ("01-Python入门与数据类型.md", "python-01", ["Python", "基础"],      None),
    ("02-流程控制与文件操作.md",   "python-02", ["Python", "基础"],      None),
    ("03-函数与模块.md",         "python-03", ["Python", "基础"],      None),
    ("04-面向对象编程.md",       "python-04", ["Python", "面向对象"],  None),
    ("05-网络编程逐集精讲.md",    "python-05", ["Python", "网络编程"],  None),
    ("06-并发编程逐集精讲.md",    "python-06", ["Python", "并发编程"],  None),
    ("07-异常处理与代码模板.md",  "python-07", ["Python", "异常处理"],  None),
    ("08-经典练习与课后作业.md",  "python-08", ["Python", "练习"],      None),
    ("09-MySQL数据库.md",       "python-09", ["Python", "数据库", "MySQL"], None),
    ("10-前端三件套.md",         "python-10", ["前端", "HTML", "CSS", "JavaScript"], None),
    ("11-Django与DRF.md",       "python-11", ["Python", "Django"],   None),
    ("12-项目实战.md",           "python-12", ["Python", "项目实战"], None),
    ("13-运维与面试.md",         "python-13", ["运维", "面试"],       None),
    ("14-课堂代码精选51段.md",    "python-14", ["Python", "代码"],     None),
]


def title_from_filename(name: str) -> str:
    """'01-Python入门与数据类型.md' -> 'Python入门与数据类型'"""
    stem = os.path.splitext(name)[0]
    first, sep, rest = stem.partition("-")
    stem = rest if sep and first.isdigit() and rest else stem
    return stem


def strip_leading_h1(text: str) -> str:
    """去掉正文开头的大标题(避免和 front-matter 的 title 重复)"""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "":
            continue
        if line.startswith("# "):
            lines = lines[i + 1:]
            return "\n".join(lines).lstrip("\n")
        break
    return text


def main():
    os.makedirs(DST, exist_ok=True)
    for i, (src_name, slug, tags, title_override) in enumerate(META):
        src_path = os.path.join(SRC, src_name)
        if not os.path.exists(src_path):
            print(f"[跳过] 源文件不存在: {src_path}")
            continue
        with open(src_path, encoding="utf-8") as f:
            body = strip_leading_h1(f.read())
        title = title_override or title_from_filename(src_name)
        date = datetime.datetime.combine(
            START_DATE + datetime.timedelta(days=i), datetime.time(9, 0))
        fm_lines = ["---", f"title: {title}", f"date: {date:%Y-%m-%d %H:%M:%S}",
                    "tags:", *[f"  - {t}" for t in tags],
                    "categories:", *[f"  - {c}" for c in CATEGORY], "---", ""]
        out_path = os.path.join(DST, f"{slug}.md")
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(fm_lines) + body)
        print(f"[完成] {src_name} -> {slug}.md ({title})")


if __name__ == "__main__":
    main()
