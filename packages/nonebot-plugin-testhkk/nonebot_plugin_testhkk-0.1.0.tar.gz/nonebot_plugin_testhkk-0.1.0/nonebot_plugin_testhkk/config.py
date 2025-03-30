from nonebot import get_driver, get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    # OpenAI API 配置
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 1000
    # 每个用户每天可以调用的次数限制
    openai_daily_limit: int = 10


# 配置加载
plugin_config: Config = get_plugin_config(Config)
global_config = get_driver().config

# 全局名称
NICKNAME: str | None = next(iter(global_config.nickname), None)
