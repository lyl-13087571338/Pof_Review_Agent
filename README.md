# pof-review-agent

这是一个基于 agent + skill 架构的审稿自动化项目。

## 目录结构

- `agent/`
  - `run_agent.py`：Agent 入口，负责 orchestrate 处理流程。
- `skills/`
  - `email_download/`
    - `SKILL.md`：技能说明文件。
    - `download.py`：实现从邮箱下载 POF 投稿 PDF。
  - `auto_review/`
    - `SKILL.md`：技能说明文件。
    - `review.py`：实现 PDF 解析、LLM 生成审稿意见并输出 Word 文件。
- `config/`
  - `config.yaml`：统一配置文件。
- `requirements.txt`：项目依赖。
- `LICENSE.txt`：项目许可声明。
- `tests/`
  - `test_agent.py`：基础架构导入测cd /Users/lyl/Desktop/pof-review-agent试。

## 安装

```bash
python3 -m pip install -r requirements.txt
```

## 配置

编辑 `config/config.yaml`：
- `email`：邮箱登录信息
- `paths`：下载与审稿文件保存目录
- `llm`：LLM 提供商配置（支持 `openai` 或 `zhipu`）

如果你要使用质谱 BigModel，请填写：

```yaml
llm:
  provider: "zhipu"
  api_key: "YOUR_BIGMODEL_API_KEY"
  api_base: "https://open.bigmodel.cn/openai"
  model: "gpt-3.5-turbo"
```

如果仍然使用 OpenAI，则可以设置：

```yaml
llm:
  provider: "openai"
  api_key: "YOUR_OPENAI_API_KEY"
  api_base: ""
  model: "gpt-3.5-turbo"
```

## 运行

```bash
python3 agent/run_agent.py
```

## 说明

这个项目已经采用 `agent + skill` 形式；`agent/run_agent.py` 为主入口，`skills/*` 作为独立技能模块。
