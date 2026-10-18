# LangChain 中使用 Ace Data Cloud

本仓库提供原生 `ChatAceDataCloud` 聊天类，以及 Suno、Seedance、HappyHorse、GPT Image、Nano Banana 五个可以分别安装的工具包。它们由 Ace Data Cloud 提供，不冒充服务品牌的官方客户端。源码已合入main；0.1.0已发布：六包可从GitHub安装，四包同时在PyPI，Suno/Seedance仍受新项目配额限制。PyPI发包、LangChain官方收录和默认Provider列表是独立阶段，实际包版本以发布状态为准。

## 安装与密钥

Python 3.10+，先创建独立环境。下面命令以正式版本 `0.1.0` 锁定安装；[发布状态](../RELEASE_STATUS.md)逐项列清PyPI/GitHub可用性。源码已合入main，官方目录申请仍待审。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install langchain-acedatacloud==0.1.0
```

| 服务 | 中文安装、Key填写和同ID查询教程 |
| --- | --- |
| Suno by Ace Data Cloud | [独立中文指南](../packages/suno/readme/README_zh_Hans.md) |
| Seedance by Ace Data Cloud | [独立中文指南](../packages/seedance/readme/README_zh_Hans.md) |
| HappyHorse by Ace Data Cloud | [独立中文指南](../packages/happyhorse/readme/README_zh_Hans.md) |
| GPT Image by Ace Data Cloud | [独立中文指南](../packages/gpt-image/readme/README_zh_Hans.md) |
| Nano Banana by Ace Data Cloud | [独立中文指南](../packages/nano-banana/readme/README_zh_Hans.md) |

各独立指南说明当前包状态与备用下载路径。源码安装可用 `git clone --branch main https://github.com/AceDataCloud/LangChain.git`，`cd LangChain` 后再安装所需目录；main已包含实现。

1. [注册／登录 Ace → 应用](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_zh_api_key)，没有通用应用时先初始化。
2. 打开通用应用，复制 API Key，或“管理密钥 → 创建”一个单独命名的 LangChain Key。
3. 检查服务权限、余额、有效期、用量和允许的 API，同时允许对应生成和任务查询接口；查看[当前价格](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_zh_pricing)。

![复制已遮挡的应用密钥或进入管理](../docs/assets/get-api-key-en.png)

![创建独立命名密钥](../docs/assets/create-api-key-en.png)

创建图中仍显示历史名称 `Dify tutorial`，实际请填写 `LangChain <服务名>`。上图为真实 Ace 控制台历史截图，来源 SunoDify 固定版本，2026-10-18 复用，真实密钥已遮挡；不是 LangChain 界面图。只复制原始 Token，不含 Bearer、引号或遮挡字符。`platform-...` 管理 Token 不能用于生成。

```bash
export ACEDATACLOUD_API_TOKEN='你的应用 Key'
```

## 原生聊天类

```python
from langchain_acedatacloud import ChatAceDataCloud

model = ChatAceDataCloud(model="gpt-4o-mini")
reply = model.invoke("用一句话问好。")  # 一次可能计费的 API 请求
print(reply.content)
```

不必再填自定义 Base URL。此类继承标准协议实现，指定 Ace 凭据、端点与追踪名称，默认关闭自动重试。它没有偷偷修改 LangChain 的默认 Provider 表；不能声称 `init_chat_model` 已原生默认支持 Ace。

## 单独安装服务并接入 Agent

```python
from langchain_acedatacloud import AceAPIClient
from langchain_suno_acedatacloud import SunoToolkit

kit = SunoToolkit(client=AceAPIClient())
print([tool.name for tool in kit.get_tools()])  # 默认仅查询，不发网络请求
```

要主动启用收费生成，应用明确设置 `include_generation=True`，然后把 `get_tools()` 返回的工具交给 LangChain Agent 或直接调用。生成提交一次，返回 task_id；后续只调用查询工具的同一 task_id。`pending` 与预览媒体不是完成，不要重新生成来等待；`terminal=true` 后再读失败或最终媒体链接。异步、同步 Python 调用都遵守同一边界。工具不自动下载媒体。

## 常见问题

401 检查原始 Key 和环境变量；403 检查余额、权限、有效期和 API 限制；429 降低并发；超时或 5xx 先查原任务与[使用历史](https://platform.acedata.cloud/console/usages?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_zh_usage)再决定是否重发。用量 tokens 不是实际扣费 Credits；安装数不是收入。当前没有新增付费 live 证明或增长数据。

本集成是开发者 Python 入口，不新增图形聊天按钮。五项服务的英文专属教程在 `packages/`，包含精确工具名、路径、安装和查询示例。官方目录遵循“先发包，再 listing issue，由维护者触发”的流程；准备材料在 `submissions/`。
