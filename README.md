```markdown
# Telegram Sticker Bot

> 一个用于获取 Telegram Premium 贴纸 Custom ID 的开源 Bot，致力于简洁易用、功能强大，并完全遵守开源协议。


## 🔧 功能特性

- **多表情查询**：一次发送多个 Emoji，如 `😂😍✨`，即可批量获取对应的 Premium 贴纸 Custom ID。
- **链接直链支持**：粘贴任意 Telegram 贴纸的链接，Bot 会自动提取并返回 Custom ID。
- **响应迅速**：高效异步处理，快速返回结果。
- **易于扩展**：模块化设计，方便后续添加更多功能（例如：贴纸包搜索、下载、管理等）。
- **完全开源**：遵循 MIT 许可证，欢迎社区贡献和二次开发。

## 📦 安装和运行

1. 克隆仓库：
   ```bash
   git clone https://github.com/domoxiaojun/telegram-bot.git
   cd telegram-bot
   ```
2. 创建并激活虚拟环境：
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\\Scripts\\activate  # Windows
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
4. 配置环境变量：
   - 在根目录下创建 `.env` 文件，添加：
     ```text
     BOT_TOKEN=你的Telegram机器人Token
     ```
5. 启动 Bot：
   ```bash
   python bot.py
   ```

## ⚙️ 配置项

| 配置项       | 说明                  | 示例                           |
| ------------ | --------------------- | ------------------------------ |
| `BOT_TOKEN`  | Telegram Bot API Token | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `LOG_LEVEL`  | 日志等级               | `DEBUG`, `INFO`, `WARNING`     |

## 🛠 架构与实现

- 基于 `python-telegram-bot` 框架，使用异步 `asyncio` 进行并发处理。
- 核心模块：
  - `bot.py`：启动脚本，加载配置和命令处理器；
  - `handlers/emoji.py`：处理 Emoji 查询逻辑；
  - `handlers/link.py`：处理贴纸链接解析；
  - `utils/api.py`：封装与 Telegram API 的交互。



## 🤝 贡献指南

1. Fork 本仓库并新建 Feature 分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. 提交你的改动并推送：
   ```bash
   git commit -m "Add new feature"
   git push origin feature/your-feature-name
   ```
3. 发起 Pull Request，描述你的变更内容和动机。
4. 通过 CI 检查后，项目维护者将进行代码审阅并合并。


## 📄 开源协议
本项目采用 MIT 许可证 开源，具体内容请参见 LICENSE 文件。


