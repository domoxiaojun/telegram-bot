import os
import json
import logging
import re
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import requests
from config import TOKEN

# 设置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,  # 设置为INFO以记录重要信息
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def escape_markdown(text: str) -> str:
    """转义Markdown特殊字符"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

def format_emoji_data(emoji_text: str, custom_emoji_id: str, index: int) -> dict:
    """格式化emoji数据"""
    if emoji_text:
        escaped_emoji = escape_markdown(emoji_text)
        text_format = f"{escaped_emoji} (ID: {custom_emoji_id})"
        markdown = f"![{escaped_emoji}](tg://emoji?id={custom_emoji_id})"
    else:
        # 当emoji_text为空时，仅显示ID或使用占位符
        text_format = f"(ID: {custom_emoji_id})"
        markdown = f"![Emoji](tg://emoji?id={custom_emoji_id})"
    
    logger.info(f"Formatted emoji {index}: {text_format}, Markdown: {markdown}")
    
    return {
        "index": index,
        "emoji": emoji_text if emoji_text else "Emoji",
        "custom_emoji_id": custom_emoji_id,
        "text_format": text_format,
        "markdown": markdown
    }

def utf16_offset_length_to_python(text: str, utf16_offset: int, utf16_length: int) -> str:
    """
    将基于 UTF-16 的 offset 和 length 转换为 Python 字符串的切片。
    
    Args:
        text (str): 消息文本。
        utf16_offset (int): 基于 UTF-16 的偏移量。
        utf16_length (int): 基于 UTF-16 的长度。
        
    Returns:
        str: 提取的子字符串。
    """
    try:
        # 编码为 UTF-16-LE 以便处理字节顺序
        utf16_encoded = text.encode('utf-16-le')
        
        # 计算字节位置
        byte_offset = utf16_offset * 2  # 每个代码单元为 2 字节
        byte_length = utf16_length * 2
        
        # 提取相应的字节片段
        substring_utf16 = utf16_encoded[byte_offset:byte_offset + byte_length]
        
        # 解码回 Python 字符串
        substring = substring_utf16.decode('utf-16-le')
        
        return substring
    except Exception as e:
        logger.error(f"转换 UTF-16 offset 和 length 时出错: {e}")
        return ""

def get_or_create_cache(sticker_set_name: str) -> dict:
    """从缓存读取或创建新的贴纸集信息"""
    cache_dir = "cache"
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"{sticker_set_name}.json")

    # 尝试从缓存读取
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                # 检查缓存是否过期（例如24小时）
                cache_time = os.path.getmtime(cache_file)
                if datetime.now().timestamp() - cache_time < 86400:  # 24小时
                    logger.info(f"使用缓存的贴纸集: {sticker_set_name}")
                    return cache_data
        except Exception as e:
            logger.error(f"读取缓存时出错: {e}")

    # 缓存不存在、过期或读取失败时，从API获取
    try:
        sticker_data = get_sticker_set_from_api(sticker_set_name)
    except Exception as e:
        logger.error(f"无法获取贴纸集 '{sticker_set_name}' 的信息: {e}")
        return {}

    # 保存到缓存
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(sticker_data, f, indent=2, ensure_ascii=False)
        logger.info(f"缓存贴纸集: {sticker_set_name}")
    except Exception as e:
        logger.error(f"写入缓存时出错: {e}")

    return sticker_data

def get_sticker_set_from_api(name: str) -> dict:
    """使用API获取贴纸集信息"""
    url = f"https://api.telegram.org/bot{TOKEN}/getStickerSet"
    params = {"name": name}
    
    try:
        response = requests.get(url, params=params, timeout=10)  # 添加超时
        response.raise_for_status()
        data = response.json()
        
        if not data.get("ok"):
            raise Exception(data.get("description", "Unknown error"))
            
        logger.info(f"成功获取贴纸集: {name}")
        return data["result"]
    except requests.RequestException as e:
        logger.error(f"获取贴纸集时的网络错误: {e}")
        raise
    except Exception as e:
        logger.error(f"获取贴纸集时出错: {e}")
        raise

def extract_sticker_set_name(url: str) -> str:
    """从分享链接中提取贴纸包名称"""
    pattern = r't\.me/(?:addemoji|addstickers)/([A-Za-z0-9_]+)'
    match = re.search(pattern, url)
    if match:
        sticker_set_name = match.group(1)
        logger.info(f"提取的贴纸集名称: {sticker_set_name}")
        return sticker_set_name
    logger.info("未从链接中提取到贴纸集名称")
    return None

async def handle_custom_emoji(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理直接发送的custom emoji"""
    message_entities = update.message.entities
    if not message_entities:
        return
        
    emoji_data = []
    output_text = []
    has_additional_text = False  # 标记是否有除自定义emoji之外的文本
    
    try:
        message_text = update.message.text or ""
        # 计算所有自定义emoji的总长度（基于 UTF-16 的代码单元）
        total_custom_emoji_length = sum(entity.length for entity in message_entities if entity.type == "custom_emoji")
        # 计算消息文本的总 UTF-16 代码单元数
        message_text_utf16_length = len(message_text.encode('utf-16-le')) // 2
        if message_text_utf16_length > total_custom_emoji_length:
            has_additional_text = True
            logger.info("消息中包含除自定义emoji之外的文本")
        
        for i, entity in enumerate(message_entities, 1):
            if entity.type == "custom_emoji":
                # 使用转换函数提取 emoji_text
                emoji_text = utf16_offset_length_to_python(
                    message_text,
                    entity.offset,
                    entity.length
                )
                
                logger.info(f"处理emoji {i}: text='{emoji_text}', ID='{entity.custom_emoji_id}'")
                
                data = format_emoji_data(emoji_text, entity.custom_emoji_id, i)
                emoji_data.append(data)
                
                # 格式化输出文本
                output_text.append(f"{i}. `{data['markdown']}`")
        
        if emoji_data:
            if has_additional_text:
                # 如果有混合内容，发送JSON文件和文本信息
                # 创建输出数据
                output_filename = f"emoji_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                output_path = os.path.join("data", output_filename)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(emoji_data, f, indent=2, ensure_ascii=False)
                logger.info(f"保存JSON文件: {output_path}")
                
                # 发送JSON文件
                with open(output_path, 'rb') as f:
                    await update.message.reply_document(
                        document=f,
                        caption=f"找到 {len(emoji_data)} 个自定义emoji"
                    )
                    
                # 清理临时文件
                os.remove(output_path)
                logger.info(f"删除临时文件: {output_path}")
            
            # 始终发送格式化的文本信息
            text = "\n\n".join(output_text)
            if len(text) < 4000:  # Telegram消息长度限制
                await update.message.reply_text(text, parse_mode='Markdown')
                logger.info("发送格式化的文本信息")
                
    except Exception as e:
        logger.error(f"处理自定义emoji时出错: {e}")
        await update.message.reply_text(f"处理自定义emoji时出错：{str(e)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理消息（链接或custom emoji）"""
    try:
        message_text = update.message.text
        
        # 处理custom emoji
        if update.message.entities and any(entity.type == "custom_emoji" for entity in update.message.entities):
            await handle_custom_emoji(update, context)
            return
            
        # 处理分享链接
        sticker_set_name = extract_sticker_set_name(message_text)
        if not sticker_set_name:
            return
            
        # 从缓存获取或创建贴纸集信息
        sticker_set = get_or_create_cache(sticker_set_name)
        
        if not sticker_set:
            await update.message.reply_text(f"无法获取贴纸集 '{sticker_set_name}' 的信息。")
            return
        
        # 处理数据
        output_data = {
            "name": sticker_set.get("name"),
            "title": sticker_set.get("title"),
            "stickers": []
        }
        
        for sticker in sticker_set.get("stickers", []):
            emoji = sticker.get("emoji", "")
            custom_id = sticker.get("custom_emoji_id", "")
            if emoji and custom_id:  # 只添加有效的表情
                escaped_emoji = escape_markdown(emoji)
                sticker_info = {
                    "emoji": emoji,
                    "custom_emoji_id": custom_id,
                    "markdown": f"![{escaped_emoji}](tg://emoji?id={custom_id})"
                }
                output_data["stickers"].append(sticker_info)
        
        # 创建输出目录（如果不存在）
        os.makedirs("data", exist_ok=True)
        
        # 保存JSON文件
        filename = f"sticker_set_{sticker_set_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join("data", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        logger.info(f"保存贴纸集JSON文件: {filepath}")
            
        # 发送文件
        with open(filepath, 'rb') as f:
            await update.message.reply_document(
                document=f,
                caption=f"贴纸包：{output_data['title']}\n共 {len(output_data['stickers'])} 个表情"
            )
            
        # 清理临时文件
        os.remove(filepath)
        logger.info(f"删除临时文件: {filepath}")
            
    except Exception as e:
        logger.error(f"处理消息时出错: {str(e)}")
        await update.message.reply_text(f"处理请求时出错：{str(e)}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """发送开始消息"""
    await update.message.reply_text(
        "Hi! 我可以帮你获取表情包信息。你可以：\n"
        "1. 发送表情包分享链接(如：https://t.me/addemoji/RestrictedEmoji)\n"
        "2. 直接发送custom emoji\n"
        "我会返回emoji信息和Markdown格式。"
    )

def main() -> None:
    """启动机器人"""
    try:
        # 创建必要的目录
        os.makedirs("logs", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        os.makedirs("cache", exist_ok=True)

        # 创建应用
        application = Application.builder().token(TOKEN).build()

        # 添加处理器
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # 添加错误处理
        def error_handler(update, context):
            logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)
        application.add_error_handler(error_handler)

        logger.info("Bot started")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"启动机器人时出错: {e}")
        raise

if __name__ == "__main__":
    main()
