from setuptools import setup, find_packages# 导入setuptools打包工具

from SakiPy._version import __version__,__author__


VERSION = __version__
DESCRIPTION = 'SakiPy 是十六夜咲月自建的一个库'
AUTHOR = __author__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="SakiPy",  # 用自己的名替换其中的YOUR_USERNAME_
    version= VERSION,  # 包版本号，便于维护版本,保证每次发布都是版本都是唯一的
    author=AUTHOR,  # 作者，可以写自己的姓名
    author_email="ma18387890737@outlook.com",  # 作者联系方式，可写自己的邮箱地址
    description=DESCRIPTION,  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://github.com/Saki/SakiPy",  # 自己项目地址，比如github的项目地址
    packages=find_packages(),
    keywords = ['API', 'SakiPy', 'Python'],   # Keywords that define your package best
    install_requires=["numpy", "joblib","pandas","scikit-learn","requests","chardet",
                      "typing_inspect","pdfplumber","PyPDF2","tqdm","colorama"],  # 运行时依赖关系
    package_data={
        'SakiPy': ['Resources/*.pkl','Resources/*.xlsx','Resources/*.json'],  # 指定my_package包中需要包含data文件夹下的所有.txt文件

    },
    include_package_data=True,
    entry_points={
        "console_scripts" : ['SakiPy = SakiPy.manage:run']
    }, #安装成功后，在命令行输入SakiPy 就相当于执行了SakiPy.manage.py中的run了
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # 对python的最低版本要求
)
# python setup.py sdist bdist_wheel
# twine upload dist/*

# pip uninstall SakiPy
# pdoc --output docs SakiPy
# pip install --upgrade dist/SakiPy-0.0.2-py3-none-any.whl

