from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jikime_cookai",
    version="0.1.6",
    author="Anthony.Kim",
    author_email="jikime@gmail.com",
    description="Jikime Cook AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jikime/jikime-cookai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        # 필요한 의존성 패키지들
    ],
) 