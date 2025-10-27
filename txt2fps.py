#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
txt → fps-xml 1.2  批量转换（与官方格式 100% 一致）
python3 txt2fps.py
"""
import re
from pathlib import Path

FPS_HEAD = """<?xml version="1.0" encoding="UTF-8"?>
<fps version="1.2" url="https://github.com/zhblue/freeproblemset/">
  <generator name="txt2fps" url="https://github.com/yourname/txt2fps"/>
"""

FPS_TAIL = "</fps>"

TIME_LIMIT = "1"      # 秒
MEM_LIMIT  = "128"    # MB

# 正则：贪婪匹配 <problem>…</problem>
PROB_RE = re.compile(r'<problem.*?>(.*?)</problem>', re.DOTALL)


def fix_tags(text: str) -> str:
    """大小写修正 + 补全 time/memory + 统一缩进"""
    # 1. 样例标签大小写
    text = re.sub(r'<sampleInput>(.*?)</sampleInput>',
                  r'<sample_input>\1</sample_input>', text, flags=re.S)
    text = re.sub(r'<sampleOutput>(.*?)</sampleOutput>',
                  r'<sample_output>\1</sample_output>', text, flags=re.S)
    # 把完全空的 <sample_input></sample_input> 换成空白 CDATA
    text = re.sub(r'<sample_input>\s*</sample_input>',
              r'<sample_input><![CDATA[NULL]]></sample_input>', text)

    # 同理 sample_output
    text = re.sub(r'<sample_output>\s*</sample_output>',
              r'<sample_output><![CDATA[NULL]]></sample_output>', text)

    # 2. 补默认限制
    if "<time_limit" not in text:
        text = (f'\t\t<time_limit unit="s"><![CDATA[{TIME_LIMIT}]]></time_limit>\n'
                f'\t\t<memory_limit unit="mb"><![CDATA[{MEM_LIMIT}]]></memory_limit>\n') + text
    return text


def build_xml(prob_inner: str) -> str:
    prob_inner = fix_tags(prob_inner)
    # 统一缩进：两层 tab
    prob_inner = "\t\t" + prob_inner.strip().replace("\n", "\n\t\t") + "\n"
    return f"{FPS_HEAD}\t<item>\n{prob_inner}\t</item>\n{FPS_TAIL}"


def txt_to_fps(txt_file: Path, out_dir: Path):
    content = txt_file.read_text(encoding='utf-8')
    m = PROB_RE.search(content)
    if not m:
        print(f"[WARN] {txt_file} 未找到 <problem> 块，跳过")
        return
    xml_doc = build_xml(m.group(1))
    out_file = out_dir / f"{txt_file.stem}.xml"
    out_file.write_text(xml_doc, encoding='utf-8')
    print(f"[ OK ] {txt_file}  ->  {out_file}")


def main():
    src_dir = Path.cwd()
    out_dir = src_dir / "fps_xml"
    out_dir.mkdir(exist_ok=True)

    txt_list = sorted(src_dir.glob("*.txt"))
    if not txt_list:
        print("当前目录未发现 .txt 文件")
        return

    for txt in txt_list:
        txt_to_fps(txt, out_dir)

    print(f"\n全部转换完成！结果保存在 ./{out_dir.relative_to(src_dir)}/")


if __name__ == "__main__":
    main()