# 更新记录

## 未发布

### 已完成

- 建立个人公开多 Skill 仓库结构，配置 `skills.sh.json`、自动校验脚本 `tools/validate_skills.py`、ZIP 打包脚本 `tools/package_skills.py`、MIT 许可证及 GitHub Actions 校验流程。
- 新增 `academic-writing` 及其 1:1 中文镜像（`translations/zh-CN/academic-writing/`）：
  - 覆盖校对、润色、改写、中英互译、基于材料起草、只读审阅、技术笔记合并整理与作用域风格学习；
  - 明确区分必须守住的保真底线与可按语境覆盖的灵活判断，避免机械套用规则与矫枉过正；
  - 支持按风险分级校验，高风险文稿可派发全新上下文只读审阅子智能体复核；
  - 内置零依赖本地保真校验脚本 `scripts/check_fidelity.py`（支持数值、单位、公式、引用、Markdown 链接 URL、`--allow-dedup`、`--protect` 与 `--allow-change`）及 18 个单元测试。

### 待办

- 按实际论文与技术报告使用反馈持续微调 `academic-writing` 触发描述与参考细则。
