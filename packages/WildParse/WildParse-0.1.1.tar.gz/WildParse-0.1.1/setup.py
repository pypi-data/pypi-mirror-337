from setuptools import setup, find_packages

setup(
    name="WildParse",
    version="0.1.1",
    author="ThunderFoxYT, FBEmpire",
    author_email="bulbapotato2.0@gmail.com",
    description="это копия одной либы(специально не буду говорить какой), но без надоедливого высера в консоли при запуске(из разряда: ВАШИ ДАННЫЕ ПРИНАДЛЕЖАТ НЕ ВАМ А MICROSOFT, У У У У У Я ТУПАЯ МАКАКА, У У У Я НЕНАВИЖУ ВИНДУ)",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md', '*.json'],
        'tests': ['*.*'],
    },
)
