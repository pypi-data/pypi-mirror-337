from setuptools import setup, find_packages

setup(
    name="ecmhongz",  # 你的包名称
    version="0.1.4",  # 版本号
    author="HongzhenHuang",
    author_email="202130500072@mail.scut.edn.cn", # 你的邮箱
    description="ecmhong is a Python package for Energy Consumption Monitoring.",  # 简短描述
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SusCom-Lab/ECM-Tool",  # 你的项目主页
    install_requires=[
        "psutil",
        "mysql-connector-python",  # mysql.connector 需要这个包
        "pandas",
        "plotly",
        "deprecated",
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # 适用的 Python 版本
)
