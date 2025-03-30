<div align="center">
    <a href="https://v2.nonebot.dev/store">
    <img src="./.docs/NoneBotPlugin.svg" width="300" alt="logo"></a>
</div>

<div align="center">

## ✨ nonebot-plugin-testhkk ✨

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Wohaokunr/nonebot-plugin-testhkk.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-testhkk">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-testhkk.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
<a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" alt="ruff">
</a>
<a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
</a>
</div>

## 📝 介绍

基于 NoneBot2 的群聊 AI 对话插件，使用 OpenAI API 实现智能对话功能。

### 功能特点

- 支持群聊中的 AI 对话
- 每个用户每天有使用次数限制
- 支持自定义 OpenAI 模型和参数
- 简单易用的命令格式

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-testhkk --upgrade
使用 **pypi** 源安装

    nb plugin install nonebot-plugin-testhkk --upgrade -i "https://pypi.org/simple"
使用**清华源**安装

    nb plugin install nonebot-plugin-testhkk --upgrade -i "https://pypi.tuna.tsinghua.edu.cn/simple"


</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details open>
<summary>uv</summary>

    uv add nonebot-plugin-testhkk
安装仓库 master 分支

    uv add git+https://github.com/Wohaokunr/nonebot-plugin-testhkk@master
</details>

<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-testhkk
安装仓库 master 分支

    pdm add git+https://github.com/Wohaokunr/nonebot-plugin-testhkk@master
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-testhkk
安装仓库 master 分支

    poetry add git+https://github.com/Wohaokunr/nonebot-plugin-testhkk@master
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_testhkk"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
| :-----: | :---: | :----: | :------: |
| OPENAI_API_KEY | 是 | 无 | OpenAI API 密钥 |
| OPENAI_MODEL | 否 | gpt-3.5-turbo | 使用的 OpenAI 模型 |
| OPENAI_TEMPERATURE | 否 | 0.7 | 生成文本的随机性 (0-1) |
| OPENAI_MAX_TOKENS | 否 | 1000 | 生成文本的最大长度 |
| OPENAI_DAILY_LIMIT | 否 | 10 | 每人每天可使用次数 |

## 🎮 使用方法

### AI 对话

在群聊中发送以下命令进行 AI 对话：
