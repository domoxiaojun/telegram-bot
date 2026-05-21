# Telegram Sticker Bot
> 一个用于获取 Telegram Premium 贴纸 Custom ID 的开源 Bot，致力于简洁易用、功能强大，并完全遵守开源协议。

## 🔧 功能特性

-   **多表情查询**：一次发送多个 Emoji，如 `😂😍✨`，即可批量获取对应的 Premium 贴纸 Custom ID。
-   **链接直链支持**：粘贴任意 Telegram 贴纸的链接，Bot 会自动提取并返回 Custom ID。
-   **响应迅速**：高效异步处理，快速返回结果。
-   **易于扩展**：模块化设计，方便后续添加更多功能（例如：贴纸包搜索、下载、管理等）。
-   **完全开源**：遵循 MIT 许可证，欢迎社区贡献和二次开发。

## 📦 安装和运行

1.  克隆仓库：
    ```bash
    git clone [https://github.com/domoxiaojun/telegram-bot.git](https://github.com/domoxiaojun/telegram-bot.git)
    cd telegram-bot
    ```
2.  创建并激活虚拟环境：
    ```bash
    uv venv
    source .venv/bin/activate  # Linux/Mac
    ```
3.  安装依赖：
    ```bash
    uv pip install -r requirements.txt
    ```
4.  配置环境变量：
    -   在根目录下创建 `.env` 文件，添加：
        ```text
        BOT_TOKEN=你的Telegram机器人Token
        BOT_MODE=webhook
        WEBHOOK_URL=https://你的域名/telegram-webhook
        ```
5.  启动 Bot：
    ```bash
    uv run python src/bot.py
    ```

    本地调试如果没有公网 HTTPS 地址，可以临时使用 polling：
    ```bash
    BOT_MODE=polling uv run python src/bot.py
    ```

### Docker 部署

项目会通过 GitHub Actions 构建并推送多架构镜像到 GHCR：

```text
ghcr.io/domoxiaojun/telegram-bot:latest
```

该镜像支持 `linux/amd64` 和 `linux/arm64`。配置好 `.env` 后可以直接启动：

```bash
docker compose up -d
```

如需使用其它镜像：

```text
DOCKER_IMAGE=ghcr.io/你的账号/telegram-bot:latest
```

## ⚙️ 配置项

| 配置项      | 说明                 | 示例                                           |
| ----------- | -------------------- | ---------------------------------------------- |
| `BOT_TOKEN` | Telegram Bot API Token | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `BOT_MODE` | 运行模式，支持 `webhook` / `polling` | `webhook` |
| `WEBHOOK_URL` | Telegram 回调的公网 HTTPS 完整地址 | `https://bot.example.com/telegram-webhook` |
| `WEBHOOK_LISTEN` | Webhook 服务监听地址 | `0.0.0.0` |
| `WEBHOOK_PORT` | Webhook 服务监听端口，Telegram 常用 `443` / `8443` | `8443` |
| `WEBHOOK_SECRET_TOKEN` | 可选，用于校验 Telegram webhook 请求来源 | `一段随机字符串` |
| `WEBHOOK_CERT` / `WEBHOOK_KEY` | 可选，直接暴露 HTTPS 时使用的证书和私钥路径；反向代理终止 TLS 时不用配置 | `/app/cert.pem` / `/app/key.pem` |
| `LOG_LEVEL` | 日志等级             | `DEBUG`, `INFO`, `WARNING`                     |

### Webhook 部署说明

Telegram webhook 必须使用公网 HTTPS 地址。推荐部署方式是让 Nginx、Caddy 或 Cloudflare 负责 HTTPS，然后把请求转发到容器的 `WEBHOOK_PORT`。

如果 `.env` 中设置：

```text
WEBHOOK_URL=https://bot.example.com/telegram-webhook
WEBHOOK_PORT=8443
```

反向代理需要把 `https://bot.example.com/telegram-webhook` 转发到 bot 服务的 `http://127.0.0.1:8443/telegram-webhook`。

## 🛠 架构与实现

-   基于 `python-telegram-bot` 框架，使用异步 `asyncio` 进行并发处理。
-   核心模块：
    -   `bot.py`：启动脚本，加载配置和命令处理器；
    -   `handlers/emoji.py`：处理 Emoji 查询逻辑；
    -   `handlers/link.py`：处理贴纸链接解析；
    -   `utils/api.py`：封装与 Telegram API 的交互。

## 🤝 贡献指南

1.  Fork 本仓库并新建 Feature 分支：
    ```bash
    git checkout -b feature/your-feature-name
    ```
2.  提交你的改动并推送：
    ```bash
    git commit -m "Add new feature"
    git push origin feature/your-feature-name
    ```
3.  发起 Pull Request，描述你的变更内容和动机。
4.  通过 CI 检查后，项目维护者将进行代码审阅并合并。


## 📄 开源协议
本项目采用 MIT 许可证 开源，具体内容请参见 [LICENSE](https://github.com/domoxiaojun/telegram-bot/blob/master/LICENSE) 文件。
