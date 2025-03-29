# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='simpleui_ext',
    version="0.1",
    packages=['simpleui_ext'],
    zip_safe=False,
    include_package_data=True,
    url='https://github.com/yxh123739/simpleui-ext',
    license='Apache License 2.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='yxh123739',
    author_email='499884734@qq.com',
    description='django simpleui扩展包',
    install_requires=['django'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
