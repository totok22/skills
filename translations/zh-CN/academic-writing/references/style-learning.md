# 作用域风格学习

说明如何在原生 Agent 会话中提炼、更新、保存并按作用域应用写作风格偏好，避免档案臃肿、带入旧稿事实或跨项目串味。

## 目录

1. 基本原则
2. 作用域与优先级
3. 建立与更新流程
4. 档案字段说明

## 1. 基本原则

- **只记风格，不记内容：** 记录重复出现的结构、语态和术语习惯，不把过往论文的实验结果、引用或套话论断写进档案。
- **准确优先，风格在后：** 先保证事实准确、分寸得当和受保护记号无误，再按风格偏好调整表达。
- **只记录具体偏好：** 只写超出本 Skill 默认规范的具体选择（期刊格式、语态分工、术语表、排版习惯），不写“行文清晰客观”这类空泛提醒。
- **限定范围并经本人确认：** 偏好只在声明的作用域（`lab`、`author`、`journal`、`language`、`genre`）内生效，与清晰度或保真冲突时直接让步；写盘前须经用户确认，不把 AI 自查算作人工批准。

## 2. 作用域与优先级

同时加载多份档案时，按从宽到窄的顺序合并（后者覆盖前者）：

```text
课题组 / 团队档案（lab / team）
  → 个人作者档案（author）
    → 期刊 / 体裁档案（journal / genre）
      → 语言 × 体裁交集（languages.<lang>.genres.<genre>）
        → 本次任务要求
          → 事实准确（最高优先级，始终不被覆盖）
```

中文（`zh`）与英文（`en`）分别放在 `languages.zh` 和 `languages.en` 下，不把英文期刊习惯照搬到中文技术报告，也不反向套用。

## 3. 建立与更新流程

### 首次建立（`learn-style`）

1. **确认材料与范围。** 明确 1–3 份授权样稿、修改前后对比或期刊要求，以及目标 `scope`（`lab`、`author` 或 `journal`）、`language` 和 `genre`。
2. **提取具体可观察的习惯：**
   - 句长变化与从句层级；
   - 不同章节的主被动语态分工（例如 Discussion 用主动 `we`，Methods 用被动）；
   - 引用方式（括号 `(Author, Year)`、主语融入 `Author (Year) showed` 或数字 `[1]`）；
   - 结论分寸、负面结果和局限性的写法；
   - 过渡词、标点和结论位置的习惯；
   - 固定规范（术语表、禁止翻译词、美/英式拼写、单位空格、双语首现标注）。
3. **先提案，确认后再保存。** 基于 [profile.example.json](../assets/profile.example.json) 生成精炼的 v1 草案，附上对应示例和例外说明，用户批准后再写入文件。

### 从日常修改中更新

- **根据改稿提出小补丁：** 用户修改了候选稿或给出明确偏好纠正时，对比候选稿与终稿，总结用户固定删掉、收紧或替换的写法，直接提出 1–3 行档案修改建议，获确认后合入。
- **可选的本地反馈日志：** 需要长期或团队留痕时，可将用户的明确判断追加到共享仓库外的本地私有 JSONL 文件：
  ```json
  {"timestamp":"2026-11-26T12:00:00Z","scope":"lab","task":"polish","language":"en","genre":"results","decision":"rejected","reason":"把明确的湿滑赛道失败弱化成了 limitations。","source":"...","candidate":"..."}
  ```
  每条 `rejected` 记录须写明具体 `reason`。写作时读取日志须严格匹配 `scope`、`language`、`genre` 和 `task`，只取最近 3–5 条（`accepted` 作参考，`rejected` 作提醒）。

### 晋升与维护

- 同一偏好重复出现至少 2–3 次，或用户明确要求时，再写入 `languages.<lang>.genres.<genre>.preferences`，不因一次偶发改动立长期规则。
- 定期清理过时、冲突或过于笼统的条目，保持档案简短、易读。
- 每次确认更新递增 `version`，保留旧版本或借助 Git 历史回滚。不把涉密稿件摘录提交到公开仓库。

## 4. 档案字段说明

从 [profile.example.json](../assets/profile.example.json) 复制起步：

- `profile_id` / `scope` / `version`：档案标识、作用域（`lab`、`author`、`journal`）和整数版本号。
- `preferences`：通用范围内的具体选择（语态分工、过渡习惯、缩写规则）。
- `conventions`：固定格式规范（`spelling`、`citation_style`、`unit_spacing`、`bilingual_first_mention`）。
- `languages.<lang>.preferences` 与 `languages.<lang>.genres.<genre>.preferences`：仅在对应语言（及体裁）精确匹配时生效的规则。
- `glossary.do_not_translate` 与 `glossary.bilingual_terms`：须原样保留的词（可同步传给 `check_fidelity.py --protect`）及标准中英术语对照。
- `exceptions`：防止机械过度套用的例外说明。
- `evidence`：简短带日期的修改依据，不粘贴涉密长段原文。
