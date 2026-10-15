# COMP20003 Project 2: Spellcheck Lookup

本项目包含 COMP20003 Project 2 的作业规范、参考说明、数据集以及提交相关代码。
本文档用于指导项目开发，并为 AI 编程助手（VS Code Gemini Assistant）提供项目上下文与文件索引规范。

---

## 1. 命名规范与文件对应关系 (File Naming Conventions)

各目录下的文件采用数字及“主序号-子序号”规则命名，表示阅读先后次序与衍生关系：

- **数字序号文件 (`X.png`, `X.c`, `X.pdf`)**：
  - 代表该章节或页面按顺序展示的主内容/截图。
  - 数字越小，优先级越高，代表材料中自上而下的阅读顺序。
- **子序号衍生文件 (`X-Y.ext`)**：
  - **代码分段/提取 (`X-Y.c`)**：若主截图 `X.png` 中的代码过长、不完整或展示不便，提取并拆分后的可运行/可读代码文件会命名为 `X-1.c`、`X-2.c`。
  - **补充链接/文本 (`X-Y.txt`)**：主材料 `X.png` 中包含的超链接、补充说明或文字记录，会存放在 `X-1.txt`、`X-2.txt` 中。

> **Gemini Assistant 注意事项**：
> 当分析算法逻辑或代码实现时，请优先参考从截图中完整提取出的 `X-Y.c` 或 `X-Y.txt` 文件，其内容比对应 `X.png` 的视觉文字更加精确、完整。

---

## 2. 目录架构说明 (Directory Structure)

```text
COMP20003_Project 2/
├── README.md
├── Specification/                # 作业官方规范与要求说明
│   ├── Task_Descrip.pdf          # 总体任务概述
│   ├── Tree_intro/               # 基础理论：Tries 与 Radix Trees 介绍
│   ├── Extra_Insert_EXP/         # 进阶实例：额外插入示例与具体步骤演示
│   │   ├── 1.png, 2.png, ...
│   │   └── 2-1.txt               # 2.png 中包含的参考链接或文本补充
│   ├── Implement_Dt/             # 实现细节：核心数据结构与逻辑
│   │   ├── 1.png, 2.png, ...
│   │   ├── 3.c                   # 示例代码实现
│   │   ├── 5-1.c, 5-2.c          # 5.png 中分段整理的完整代码
│   │   └── ...
│   ├── Implement_Req...          # 实现要求（编程规范、复杂度与限制）
│   ├── Assessment.png            # 评分准则与分数构成
│   └── Assignment_ILOs/          # 课程预期学习目标（ILOs）对齐说明
│
├── Dataset_Download/             # 测试数据集与匹配用例
│   ├── dts_pic/                  # 数据集相关图示说明
│   ├── matching_results/         # 预期比对与测试输出结果
│   └── tests/                    # 测试输入用例
│
└── Assignment_Submission/        # 作业提交文件与辅助代码
    ├── 1.png, 2.png
    ├── 1-1.c, 2-1.c, 2-2.c       # 各提交阶段对应的源码与模块
    └── ...