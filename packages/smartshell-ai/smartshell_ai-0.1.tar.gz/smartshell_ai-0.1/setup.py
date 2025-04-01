from setuptools import setup, find_packages

setup(
    name="smartshell-ai",
    version="0.1",
    packages=find_packages(),
    py_modules=["smartshell"],
    install_requires=[
        "click",
        "colorama",
        "rich",
        "requests",
        "rapidfuzz",
        "openai",
        "ollama",
        "pyreadline3",
    ],
    entry_points={
        "console_scripts": [
            "smartshell=smartshell:cli",
        ],
    },
)
