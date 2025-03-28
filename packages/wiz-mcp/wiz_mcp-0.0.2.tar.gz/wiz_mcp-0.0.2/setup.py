from setuptools import setup, find_packages

setup(
    name='wiz-mcp',  # 项目名称
    version='0.0.2',      # 项目版本
    packages=find_packages(),  # 自动找到所有的包
    install_requires=[   # 项目的依赖包
        'aiohttp',      # 示例依赖包
        'mcp',         # 示例依赖包
    ],
    author="Gentleelephant",  # 作者
    author_email="moon0hello@gmail.com",
    description="This is a mcp server for KubeSphere Wizard.",  # 项目简短描述
    long_description=open('README.md').read(),  # 从 README 文件中读取详细描述
    long_description_content_type='text/markdown',  # README 文件类型，通常为 Markdown
    url="https://github.com/Gentleelephant",  # 项目网址（GitHub 等）
    python_requires='>=3.10',  # Python 最低版本要求
)