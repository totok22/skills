# 维护规范

## 新增 Skill

- 目录名使用小写字母、数字和连字符，并与 `SKILL.md` 的 `name` 完全一致；
- Frontmatter 只保留 `name` 和 `description`；
- `description` 同时说明能力、应触发场景和不应触发场景，避免写成过宽描述；
- `SKILL.md` 只放核心流程与硬底线，较长的专项规则放入一级 `references/`，且全部规则自包含，不依赖 AI 去抓取外部链接；
- 各 Skill 目录内不放独立的 README、安装指南或更新日志，统一由仓库根目录 `README.md` 和 `CHANGELOG.md` 承担；
- `agents/openai.yaml` 的 `default_prompt` 必须明确引用 `$skill-name`；
- 在 `translations/zh-CN/` 下同步维护同名 1:1 中文镜像；镜像只用于阅读，不参与安装、打包和发布；
- 在 `skills.sh.json` 中登记对应分组。

## 修改现有 Skill

先明确真实使用中暴露的问题（例如误触发、规则过严、细节缺失或措辞生硬），只做解决该问题所需的改动。若调整了能力或触发范围，同步检查：

- Frontmatter `description`；
- `agents/openai.yaml` 的名称、简介与默认提示；
- `translations/zh-CN/<skill-name>/` 对应镜像；
- 引用文件路径与路由是否准确；
- 根目录 `README.md`、`skills.sh.json` 与 `CHANGELOG.md`。

## 验证

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_skills.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/academic-writing/scripts -p 'test_*.py' -v
```

自动校验只检查结构、链接与脚本回归，不能替代对触发边界和实际写作效果的判断。
