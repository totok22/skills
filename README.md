# Personal Agent Skills

[![skills.sh](https://skills.sh/b/totok22/skills)](https://skills.sh/totok22/skills)

个人公开维护的 Agent Skills 仓库。每个 Skill 独立成目录，可单独安装、校验、打包和迭代。

## 当前 Skills

| Skill | 中文镜像 | 用途 | 调用建议 |
| --- | --- | --- | --- |
| [`academic-writing`](skills/academic-writing/SKILL.md) | [中文](translations/zh-CN/academic-writing/SKILL.md) | 中英文学术论文、学位论文、技术报告、设计文档、审稿回复与笔记整理的校对、润色、改写、互译、起草、审阅与风格学习 | 处理学术或工程写作、中英互译、审稿回复、合并笔记或提炼个人/课题组风格时调用；不用于文献检索、LaTeX 编译排错、绘图或代码实现 |

## 目录结构

```text
skills/
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md             # 必需；触发描述、任务路由与执行规范
│       ├── agents/openai.yaml   # 推荐；展示名称与默认提示
│       ├── references/          # 按需读取的详细规范
│       ├── scripts/             # 可选；本地确定性工具与测试
│       └── assets/              # 可选；模板或示例文件
├── translations/zh-CN/
│   └── <skill-name>/            # 1:1 中文镜像，仅供阅读，不参与安装和发布
├── tools/
│   ├── validate_skills.py       # 校验结构、链接、配置、脚本语法及中文镜像一致性
│   └── package_skills.py        # 生成可复现的独立 ZIP 包（dist/<skill-name>.zip）
├── skills.sh.json               # skills.sh 仓库分组配置
└── .github/workflows/           # CI 自动校验与单元测试
```

每个 Skill 只依赖自己目录内的文件，不依赖外部链接或本地其他工程。`skills/` 是面向 Agent 的英文原版与安装来源；`translations/zh-CN/` 是便于阅读的 1:1 中文镜像，修改任意一侧时同步更新另一侧。

## 安装

使用 `skills` CLI 查看并安装：

```bash
npx skills add totok22/skills --list

# 全局安装到 Codex
npx skills add totok22/skills \
  --skill academic-writing \
  --agent codex \
  --global

# 全局安装到 Claude Code
npx skills add totok22/skills \
  --skill academic-writing \
  --agent claude-code \
  --global
```

也可以克隆仓库后手动安装（本地维护时可用 `ln -sfn` 代替 `cp -R`）：

```bash
git clone https://github.com/totok22/skills.git
cp -R skills/skills/academic-writing ~/.agents/skills/
```

更新后重启或新建 Agent 会话即可生效。不要把整个仓库根目录当作单个 Skill 安装。

## 校验与打包

仅依赖 Python 3.9+ 标准库，无需额外安装第三方依赖：

```bash
# 结构、链接、skills.sh.json、脚本语法、中英镜像 1:1 一致性与公开边界校验
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_skills.py

# 运行 Skill 自带脚本单元测试
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/academic-writing/scripts -p 'test_*.py' -v

# 打包为可复现 ZIP（输出至 dist/<skill-name>.zip，不提交 Git）
python3 tools/package_skills.py
```

## 维护说明

1. 新增或修改 Skill 时遵循 [CONTRIBUTING.md](CONTRIBUTING.md) 与 [AGENTS.md](AGENTS.md)；
2. 同步更新 `agents/openai.yaml`、`translations/zh-CN/` 中文镜像、`skills.sh.json` 和 [CHANGELOG.md](CHANGELOG.md)；
3. 运行 `python3 tools/validate_skills.py` 及对应单元测试通过后再提交。

## 公开仓库边界

不得提交密码、Token、私钥、个人隐私信息、未发表稿件、审稿意见原文或无权公开的资料。

## 许可证

本仓库采用 [MIT License](LICENSE)。
