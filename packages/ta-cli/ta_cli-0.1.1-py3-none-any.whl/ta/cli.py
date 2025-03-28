import click
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from ta.core.ta import TAClient
from ta.core.db import Database
from playwright.sync_api import sync_playwright


# @click.group(invoke_without_command=True)
@click.group()
def main():
    """与 DeepSeek AI 进行对话的命令行工具"""
    pass


@main.command()
def install_browsers():
    """安装 Playwright 浏览器"""
    try:
        with sync_playwright() as p:
            p.chromium.install()
        click.echo(click.style("浏览器安装成功！", fg="green"))
    except Exception as e:
        click.echo(click.style(f"安装浏览器时出错: {e}", fg="red"))


@main.command()
@click.argument("question", nargs=-1, required=False)
@click.option("-s", "--search", is_flag=True, help="使用搜索模式")
@click.option("-x", "--execute", is_flag=True, help="使用执行模式")
@click.option("-r", "--role", type=str, help="指定角色")
def chat(question, search, execute, role):
    """与 AI 进行对话"""
    try:
        # 如果没有提供问题，则提示用户输入
        if not question:
            question_text = input(click.style("请输入您的问题: ", fg="yellow"))
        else:
            question_text = " ".join(question)
        client = TAClient()
        md = Markdown("*对方正在输入...*")
        with Live(md) as live:
            client.chat(question_text, live, use_search=search)
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red"))


@main.command()
@click.argument("question", nargs=-1, required=False)
def sh(question):
    """生成命令行命令"""
    try:
        if not question:
            question_text = input(click.style("请描述您想要执行的命令: ", fg="yellow"))
        else:
            question_text = " ".join(question)

        client = TAClient()
        prompt = f"""请根据以下描述生成一个命令行命令。
要求：
1. 只返回命令本身，不要包含任何解释或额外文本
2. 不要使用反引号（`）包裹命令
3. 不要使用任何代码块标记
4. 确保命令可以直接在终端中执行

描述：{question_text}"""

        # 显示加载提示
        with Live(
            Spinner("dots", click.style("正在生成命令...", fg="blue")),
            refresh_per_second=10,
            vertical_overflow="visible",
        ) as live:
            response = client.chat(prompt)
            live.update("")  # 清除 spinner 显示

        # 清理响应文本，移除所有反引号和代码块标记
        command = response.strip().replace("`", "").replace("```", "").strip()

        # 显示命令并询问是否执行
        click.echo(f"生成的命令：{click.style(command, fg='cyan')}")
        if click.confirm(click.style("是否执行此命令？", fg="yellow"), default=True):
            import subprocess

            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                click.echo(click.style(f"命令执行失败: {e}", fg="red"))
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red"))


@main.command()
@click.option(
    "--api-key",
    prompt=click.style("请输入 API Key", fg="yellow"),
    hide_input=True,
    help="设置 API Key",
)
@click.option(
    "--base-url",
    prompt=click.style("请输入 Base URL", fg="yellow"),
    default="https://api.deepseek.com",
    help="设置 Base URL",
)
@click.option(
    "--model",
    prompt=click.style("请输入模型名称", fg="yellow"),
    default="deepseek-chat",
    help="设置模型名称",
)
def config(api_key, base_url, model):
    """配置 TA 客户端"""
    try:
        db = Database()
        if api_key:
            db.set_config("api_key", api_key)
        if base_url:
            db.set_config("base_url", base_url)
        if model:
            db.set_config("model", model)
        click.echo(click.style("配置已更新！", fg="green"))
    except Exception as e:
        click.echo(click.style(f"配置更新失败: {e}", fg="red"))


if __name__ == "__main__":
    main()
