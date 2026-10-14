#!/usr/bin/env python3
"""全书标点统一：正文中的半角标点转全角。

规则：
- 处理 ? ! ; : , ( ) 七个半角标点；
- 仅当其前后（忽略空格）有中文字符或全角标点时转换，西文/数字语境不动；
- 跳过 HTML 注释、行内脚注 ^[…]（脚注文献信息照原书保留半角）、URL。
"""
import re
import sys
import unicodedata

PUNCT = {"?": "？", "!": "！", ";": "；", ":": "：", ",": "，", "(": "（", ")": "）"}


def is_cjk_context(ch: str) -> bool:
    if not ch:
        return False
    cp = ord(ch)
    if (
        0x4E00 <= cp <= 0x9FFF      # CJK 统一表意文字
        or 0x3400 <= cp <= 0x4DBF   # 扩展 A
        or 0x3000 <= cp <= 0x303F   # CJK 标点（。、「」等）
        or 0xFF00 <= cp <= 0xFFEF   # 全角形式（）？！，：；《》等
        or ch in "—…·“”‘’〖〗【】〔〕〘〙《》〈〉、。，；：？！—…"
    ):
        return True
    return False


def mask_spans(text: str):
    """返回与 text 等长的布尔列表，True 表示该位置应跳过。"""
    mask = [False] * len(text)
    for m in re.finditer(r"<!--.*?-->", text, re.S):
        for i in range(m.start(), m.end()):
            mask[i] = True
    for m in re.finditer(r"https?://\S+", text):
        for i in range(m.start(), m.end()):
            mask[i] = True
    # 行内脚注 ^[ ... ]（平衡括号，内容里可能有 [M] 等）
    i = 0
    while True:
        j = text.find("^[", i)
        if j == -1:
            break
        depth = 0
        k = j + 1
        while k < len(text):
            if text[k] == "[":
                depth += 1
            elif text[k] == "]":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        for p in range(j, min(k + 1, len(text))):
            mask[p] = True
        i = k + 1
    return mask


def convert(text: str) -> str:
    mask = mask_spans(text)
    chars = list(text)
    n = len(chars)

    def neighbor(pos: int, step: int) -> str:
        p = pos + step
        while 0 <= p < n and chars[p] == " ":
            p += step
        return chars[p] if 0 <= p < n else ""

    for i, ch in enumerate(chars):
        if mask[i] or ch not in PUNCT:
            continue
        prev_c, next_c = neighbor(i, -1), neighbor(i, 1)
        if is_cjk_context(prev_c) or is_cjk_context(next_c):
            chars[i] = PUNCT[ch]
    return "".join(chars)


def main():
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as f:
            src = f.read()
        out = "\n".join(convert(line) for line in src.split("\n"))
        if out != src:
            with open(path, "w", encoding="utf-8") as f:
                f.write(out)
            print(f"已转换: {path}")


if __name__ == "__main__":
    main()
