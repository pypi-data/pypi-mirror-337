from setuptools import setup, find_packages

setup(
    name="textgradient",
    version="0.1",
    packages=find_packages(),
    install_requires=["colorama"],
    entry_points={
        "console_scripts": [
            "textgradient=textgradient.gradient:main"
        ]
    },
    include_package_data=True,
    package_data={"textgradient": ["config.json"]},
    description="A Python package to create gradient-colored text",
    author="Prime",
    author_email="push9352@gmail.com",
    url="https://github.com/l/textgradient",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
