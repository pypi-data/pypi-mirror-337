from nonebot import logger, require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_waiter")
require("nonebot_plugin_uninfo")
require("nonebot_plugin_alconna")
require("nonebot_plugin_localstore")
require("nonebot_plugin_apscheduler")
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="AI 群聊助手",
    description="基于 OpenAI 的群聊 AI 对话插件",
    usage="使用方法：\n1. 发送 '!ai <问题>' 进行 AI 对话\n2. 发送 '!ai 帮助' 查看帮助信息",
    type="application",  # library
    homepage="https://github.com/Wohaokunr/nonebot-plugin-testhkk",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna", "nonebot_plugin_uninfo"),
    # supported_adapters={"~onebot.v11"},
    extra={"author": "Wohaokunr <your@mail.com>"},
)

from arclet.alconna import Alconna, Args, Arparma, Option, Subcommand
from nonebot_plugin_alconna import on_alconna
from nonebot_plugin_alconna.uniseg import UniMessage
from nonebot.adapters import Event

from .ai_chat import chat_with_ai, load_usage_records



# AI 对话命令
ai_chat = on_alconna(
    Alconna(
        "!ai",
        Args["prompt", str],
    )
)

@ai_chat.handle()
async def handle_ai_chat(event: Event, result: Arparma):
    prompt = result.all_matched_args.get("prompt", "")
    
    # 处理帮助命令
    if prompt.strip() == "帮助":
        help_text = (
            "AI 群聊助手使用指南：\n"
            "1. 发送 '!ai <问题>' 进行 AI 对话\n"
            "2. 每人每天可使用 AI 对话 {limit} 次\n"
            "3. 示例：!ai 介绍一下自己"
        ).format(limit=Config.openai_daily_limit)
        await UniMessage.text(help_text).send()
        return
    
    # 空提示词处理
    if not prompt.strip():
        await UniMessage.text("请输入有效的问题，例如：!ai 今天天气怎么样？").send()
        return
    
    # 获取用户ID
    user_id = str(event.get_user_id())
    
    # 发送等待消息
    await UniMessage.text("正在思考中...").send()
    
    # 调用 AI 对话
    response = await chat_with_ai(prompt, user_id)
    
    # 发送回复
    await UniMessage.text(response).send()

# 保留原有的 pip 命令示例
pip = on_alconna(
    Alconna(
        "pip",
        Subcommand(
            "install",
            Args["package", str],
            Option("-r|--requirement", Args["file", str]),
            Option("-i|--index-url", Args["url", str]),
        ),
    )
)


@pip.handle()
async def _(result: Arparma):
    package: str = result.other_args["package"]
    logger.info(f"installing {package}")
    await UniMessage.text(package).send()
