# 孙绍振古典散文解读全编（Close Reading of Classical Prose）

孙绍振 著 · 上海教育出版社 · 2021 年

本项目将《孙绍振古典散文解读全编》PDF 经 [MinerU](https://github.com/opendatalab/MinerU) 双模式（pipeline / vlm）交叉识别、人工校对后排版为 Markdown，再由 pandoc 构建 EPUB 3 电子书。全书含导读《古代散文的解读观念和方法》及《老子》三章、《曹刿论战》、《过秦论》、《出师表》、《桃花源记》、《岳阳楼记》、《赤壁赋》、《项脊轩志》等六十余篇先秦至明清古典散文的个案解读，以脚注和散文选文为主要排版特征。

## 文件结构

| 文件 | 说明 |
| --- | --- |
| `manuscript/00-frontmatter.md` | 前置部分（电子版说明与免责声明） |
| `manuscript/*.md` | 序及各篇正文（**所有修改都在对应文件里进行**），构建时按文件名序合并 |
| `metadata.yaml` | pandoc 元数据（书名、作者、语言） |
| `assets/epub.css` | EPUB 样式（正文用阅读器默认字体；标题黑体 / 选文楷体 / 扉页仿宋，字体栈取自 [fonts.css](https://github.com/zenozeng/fonts.css) 跨平台方案） |
| `assets/cover.jpg` | 封面图（可选，存在即自动嵌入） |
| `scripts/ocr.sh` | MinerU 双模式分片识别（200 页/片，断点续跑） |
| `scripts/build.sh` | pandoc 构建脚本（`--split-level=2` 按节拆分文件即硬分页；CSS 剥注释后打包，兼容 Clearview） |
| `scripts/ascii-heading-ids.lua` | pandoc Lua 过滤器：标题锚点改写为 ASCII 序号（sec-N），否则中文锚点在 Clearview 等阅读器中目录无法跳转 |
| `Makefile` | `make build` 构建，`make ocr` 识别，`make clean` 清理 |
| `docs/workflow.md` | OCR 交叉校对流程与 Markdown 书写约定的完整说明 |
| `孙绍振古典散文解读全编.epub` | 构建产物（不入库，见 Releases） |

原始 PDF 与 OCR 中间结果（`source/`、`ocr/`）不入库，请自行准备。

## 下载

每次打 tag 都会由 GitHub Actions 自动构建 EPUB 并发布到 Releases：

- [下载最新版 EPUB](https://github.com/syhily/close-reading-of-classical-prose/releases/latest/download/close-reading-of-classical-prose.epub)（直链，始终指向最新 Release）
- [查看全部版本](https://github.com/syhily/close-reading-of-classical-prose/releases)

## 构建

```sh
make build    # 生成 build/孙绍振古典散文解读全编.epub
make clean    # 删除构建产物
```

只依赖 [pandoc](https://pandoc.org)。OCR 环节另需 `mineru-open-api`（`npm install -g mineru-open-api`）及 token，详见 `docs/workflow.md`。

## 参与校对与修改

欢迎通过 Issue 或 Pull Request 指正 OCR 讹误与排版问题。修改 `manuscript/` 对应文件后运行 `make build` 重建即可。Markdown 中的排版约定（详见 `docs/workflow.md`）：

- `# …`：序等独立部分标题（居中黑体，独立成页）；`## …`：各篇解读标题（居中黑体，独立成页）；`#### …`：篇内小节标题（居中黑体，不进目录）
- `> 文字`：按段排版的选文/引文（楷体缩进）
- `| 诗行`：文中引用诗句（行块，每句一行、整体缩进，楷体）
- `::: {.xuanwen}`：长篇选文（含标题、多段落的作品原文）
- `[文字]{.zhuozhong}`：着重号（字下圆点，原书表示关键概念的方式）
- `文字^[脚注内容]`：行内脚注（EPUB 3 弹注；不用 `[^n]` 编号式，避免多页合并时编号错位）
- `**文字**`：黑体强调；`*文字*`：楷体（中文不倾斜）
- `::: {.fangsong}`：扉页信息、题辞、出版说明（仿宋）
- 拿不准的字，加 HTML 注释 `<!-- 疑：原书作「x」 -->` 留待复核

## 致谢

- `assets/epub.css` 的跨平台中文字体栈来自 [fonts.css](https://github.com/zenozeng/fonts.css)，Copyright (C) 2013-2018 Zeno Zeng and contributors，[MIT License](https://github.com/zenozeng/fonts.css/blob/main/LICENSE)。
- `assets/epub.css` 的部分排版规则（CJK 换行禁则、悬挂标点、上下标归一、引号等）借鉴 [typo.css](https://github.com/sofish/typo.css)，Copyright (C) 2012 Sofish Lin，[MIT License](https://github.com/sofish/typo.css/blob/master/license.txt)。

## 免责声明

本书著作权归原作者及上海教育出版社所有。本项目仅供个人学习与研究使用，不进行任何商业用途，不用于任何形式的再出版。OCR 识别与人工校对可能存在讹误，内容请以上海教育出版社纸质原书为准。若本仓库内容涉及侵权，请联系仓库所有者，核实后将立即删除。
