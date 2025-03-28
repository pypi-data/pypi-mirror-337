# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="xgodoglib",
    version="0.1.1",
    author="LuwuDynamics",
    author_email="hello@xgorobot.com",
    description="XGO-DOG's python campaign file and graphical display file",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Xgorobot/XGO-PythonLib",
    packages=['xgolib', 'xgoscreen'],  
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[ 
    ],
)
