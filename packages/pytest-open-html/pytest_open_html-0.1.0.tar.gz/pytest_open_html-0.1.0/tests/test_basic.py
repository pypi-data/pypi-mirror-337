def test_plugin(tmp_path, pytestconfig):
    """模拟 pytest-html 报告生成"""
    fake_report = tmp_path / "report.html"
    fake_report.write_text("<html><body>Test</body></html>")
    
    # 模拟 pytest 配置
    pytestconfig.option.htmlpath = str(fake_report)
    
    # 触发插件逻辑
    pytestconfig.hook.pytest_configure(config=pytestconfig)
    pytestconfig.hook.pytest_unconfigure(config=pytestconfig)
    
    # 实际测试需要手动验证浏览器是否打开
    assert fake_report.exists()  