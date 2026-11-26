# AI 代码与文档规范

- 修改或新增 Skill 时保持一个 Skill 一个独立目录，所有规则自包含在目录内。
- Frontmatter 的 `description` 必须明确触发和不触发场景，不得为了提高调用率写成宽泛描述。
- 核心流程放在 `SKILL.md`；详细规则按需放入一级 `references/`，避免跨文件重复。
- 修改能力、措辞或触发范围后，同步更新 `agents/openai.yaml` 和 `translations/zh-CN/` 对应中文镜像。
- 根目录 `README.md` 负责仓库入口和 Skill 索引；各 Skill 不创建自己的 README、安装指南或更新日志。
- 已完成修改和待办统一维护在根目录 `CHANGELOG.md`。
- 修改后运行 `python3 tools/validate_skills.py` 与受影响脚本的单元测试，并确认 Git 差异中没有缓存、构建产物和敏感信息。
- 不加入真实密码、Token、私钥、个人隐私信息、未发表稿件或无权公开的资料。
- 使用平实、直接、清楚的中文，避免说教、抽象黑话、冗余和重复。
