📦 Telegram Sticker Bot
一个专为 Telegram 用户打造的 Bot，支持提取 Premium 表情包的 Custom ID。你可以通过发送 Emoji 或贴纸链接，快速获取 Custom ID，便于开发者或用户使用贴纸进行进一步创作、分析、二次开发等操作。

✨ 功能特性
✅ 支持发送单个或多个 Emoji（如：😂😍✨），自动提取 Telegram Premium 动态贴纸的 Custom ID。

✅ 支持直接发送贴纸链接，自动识别并提取对应 ID。

✅ 自动判断是否为 Premium 表情，非 Premium 也会给出明确提示。

✅ 快速响应，极简交互，适合所有用户。

✅ 完全开源，支持二次开发。

✅ 后续将支持：

获取表情的打包 ID 与所属 Sticker Set；

将 Custom ID 反向转为贴纸/Emoji 预览；

一键保存与收藏；

Telegram 群组/频道插件支持；

与 AI 表情推荐系统集成。

🚀 快速开始
使用 Bot
向 Bot 发送一个或多个 Emoji，例如：

复制
编辑
😂😍✨
或发送一个 Telegram 表情贴纸链接：

arduino
复制
编辑
https://t.me/addstickers/NameOfPremiumPack
Bot 将自动解析并返回如下信息：

vbnet
复制
编辑
Emoji: 😂
Custom ID: CAACAgUAAxkBAAEK2F1kZ...
Type: Premium Animated
🛠 本地部署
环境要求
Python 3.9+

Telegram Bot Token（可从 @BotFather 获取）

推荐部署于 Linux 或 VPS 上（如 Ubuntu）

安装依赖
bash
复制
编辑
git clone https://github.com/domoxiaojun/telegram-bot.git
cd telegram-bot
pip install -r requirements.txt
启动 Bot
将 .env.example 重命名为 .env 并填入你的 BOT_TOKEN，然后运行：

bash
复制
编辑
python bot.py
🧱 技术栈
Python

python-telegram-bot

dotenv

asyncio（计划支持异步架构以提升响应速度）

🤝 贡献指南
我们欢迎任何形式的贡献！

Fork 本项目

创建你的特性分支：git checkout -b feature/你的特性

提交你的修改：git commit -m '增加某功能'

推送到分支：git push origin feature/你的特性

提交 Pull Request

请遵守项目的代码规范，并保持模块化与清晰注释。

📜 开源协议
本项目采用 MIT License 开源协议。你可以自由使用、修改、发布该代码，但请保留原作者信息。

🔮 未来规划
✅ 多语言支持（中文 / 英文）
✅ 自定义 Emoji 组合收藏功能
✅ 与其他 Telegram 工具生态整合（如 bot 内使用 AI 表情匹配推荐）
✅ 可视化界面（支持网页端操作贴纸库）
✅ 插件系统（便于开发者扩展功能）

❤️ 鸣谢
Telegram 团队提供的开放 API 和优秀生态

所有开源社区的开发者与灵感启发

感谢使用与支持本项目的每一位朋友！
