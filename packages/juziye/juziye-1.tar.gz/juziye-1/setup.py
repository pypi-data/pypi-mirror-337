from setuptools import setup, find_packages

setup(
    name="juziye",  # 包名
    version="v1",    # 版本号
    packages=find_packages(),  # 查找包
    install_requires=[  # 列出包的依赖项（如果有）
        'torch','math'
    ],
    author="Jason",  # 你的名字
    author_email="1816423817@qq.com",  # 你的邮箱
    description="一个实现transformer结构的简单的包",  # 包的简介
    long_description_content_type="text/markdown",  # 描述类型
    url="https://github.com/yourusername/my_package",  # 项目的 GitHub 或网站地址
    classifiers=[  # 用于 PyPI 中的分类标签
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 适用的 Python 版本
)
