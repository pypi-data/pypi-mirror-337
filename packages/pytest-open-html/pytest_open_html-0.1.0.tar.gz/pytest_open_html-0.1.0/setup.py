from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pytest-open-html",
    version="0.1.0",
    description="Auto-open HTML reports after pytest runs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your@email.com",
    license="MIT",
    py_modules=["pytest_open_html"],
    install_requires=["pytest>=6.0", "pytest-html"],
    classifiers=[
        "Framework :: Pytest",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["open-html = pytest_open_html"]},
)