# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2025-03-27 22:21:43
# @Last Modified by:   Your name
# @Last Modified time: 2025-03-27 22:30:59
# 为了向后兼容保留此文件
# 实际配置已迁移到pyproject.toml

import setuptools

str_version = '1.3.8'

if __name__ == '__main__':
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setuptools.setup(
        name='cellink',
        version=str_version,
        description='An easy-to-use engine that allows python programmers to code with Chain of Responsibility Pattern',
        long_description=long_description,
        long_description_content_type="text/markdown",
        author='Zhai Menghua',
        author_email='viibridges@gmail.com',
        # 将来如果代码托管到GitHub或其他平台，取消下面的注释并添加正确的URL
        # url='https://github.com/username/cellink',
        packages=setuptools.find_packages(),
        package_data={
            '': ['assets/imgs/*.png', 'README.md'],
        },
        include_package_data=True,
        install_requires=[
            'graphviz>=0.16.0',
            'numpy>=1.19.0',
        ],
        python_requires='>=3.6',
        license='Apache 2.0',
        zip_safe=False,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Software Development :: Libraries',
        ],
        keywords='chain of responsibility, design pattern',
    )
