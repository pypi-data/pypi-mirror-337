import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pics",
    version="5.3.3",
    author="TEARK",
    author_email="913355434@qq.com",
    description="for cut picture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/teark/pictools.git",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
