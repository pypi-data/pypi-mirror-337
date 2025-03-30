import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from nonebot import logger
from nonebot_plugin_localstore import get_cache_dir
import openai
from openai import AsyncOpenAI
import json
import os

from .config import plugin_config

# 用户调用次数记录
user_call_records: Dict[str, List[datetime]] = {}
# 缓存目录
CACHE_DIR = get_cache_dir("nonebot_plugin_testhkk")
USAGE_FILE = CACHE_DIR / "usage_records.json"

# 初始化 OpenAI 客户端
client = AsyncOpenAI(api_key=plugin_config.openai_api_key)


async def load_usage_records():
    """加载使用记录"""
    global user_call_records
    if os.path.exists(USAGE_FILE):
        try:
            with open(USAGE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 将字符串时间转换回 datetime 对象
                for user_id, times in data.items():
                    user_call_records[user_id] = [
                        datetime.fromisoformat(time_str) for time_str in times
                    ]
            logger.info("已加载用户使用记录")
        except Exception as e:
            logger.error(f"加载使用记录失败: {e}")
    else:
        # 确保缓存目录存在
        os.makedirs(CACHE_DIR, exist_ok=True)
        logger.info("创建新的使用记录文件")


async def save_usage_records():
    """保存使用记录"""
    try:
        # 将 datetime 对象转换为 ISO 格式字符串
        data = {
            user_id: [time.isoformat() for time in times]
            for user_id, times in user_call_records.items()
        }
        with open(USAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"保存使用记录失败: {e}")


async def check_rate_limit(user_id: str) -> Tuple[bool, int]:
    """
    检查用户是否超过使用限制
    
    返回: (是否可以使用, 剩余次数)
    """
    # 获取今天的开始时间
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 如果用户不在记录中，初始化
    if user_id not in user_call_records:
        user_call_records[user_id] = []
    
    # 清理过期记录（只保留今天的）
    user_call_records[user_id] = [
        time for time in user_call_records[user_id] if time >= today
    ]
    
    # 计算今天已使用次数
    used_today = len(user_call_records[user_id])
    remaining = plugin_config.openai_daily_limit - used_today
    
    # 检查是否超过限制
    if used_today >= plugin_config.openai_daily_limit:
        return False, 0
    
    return True, remaining


async def record_usage(user_id: str):
    """记录用户使用"""
    if user_id not in user_call_records:
        user_call_records[user_id] = []
    
    user_call_records[user_id].append(datetime.now())
    await save_usage_records()


async def chat_with_ai(prompt: str, user_id: str) -> str:
    """与 AI 对话"""
    try:
        # 检查 API 密钥是否配置
        if not plugin_config.openai_api_key:
            return "错误：未配置 OpenAI API 密钥，请联系管理员设置"
        
        # 检查使用限制
        can_use, remaining = await check_rate_limit(user_id)
        if not can_use:
            return f"今日 AI 对话次数已用完，请明天再试"
        
        # 调用 OpenAI API
        response = await client.chat.completions.create(
            model=plugin_config.openai_model,
            messages=[
                {"role": "system", "content": "你是一个友好、有帮助的AI助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=plugin_config.openai_temperature,
            max_tokens=plugin_config.openai_max_tokens,
        )
        
        # 记录使用
        await record_usage(user_id)
        
        # 获取回复内容
        reply = response.choices[0].message.content
        return f"{reply}\n\n(今日剩余次数: {remaining-1})"
    
    except openai.RateLimitError:
        return "OpenAI API 调用频率超限，请稍后再试"
    except openai.AuthenticationError:
        return "OpenAI API 认证失败，请联系管理员检查 API 密钥设置"
    except Exception as e:
        logger.error(f"AI 对话出错: {e}")
        return f"AI 对话出错: {str(e)}"