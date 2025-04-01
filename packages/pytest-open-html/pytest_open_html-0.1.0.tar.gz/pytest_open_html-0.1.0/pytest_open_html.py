import webbrowser
from pathlib import Path
import pytest

def pytest_addoption(parser):
    group = parser.getgroup("open-html")
    group.addoption(
        "--no-open-html",
        action="store_true",
        default=False,
        help="Disable auto-opening HTML report",
    )

def pytest_configure(config):
    # 仅在生成 HTML 报告且未禁用时激活
    if (htmlpath := config.getoption("htmlpath")) and not config.getoption("--no-open-html"):
        config._open_html_path = Path(htmlpath).absolute()

def pytest_unconfigure(config):
    if hasattr(config, "_open_html_path"):
        report_path = config._open_html_path
        if report_path.exists():
            webbrowser.open_new_tab(f"file://{report_path}")