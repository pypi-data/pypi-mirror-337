import os
from setuptools import setup, find_packages


setup(
    name='cartel',
    version='1.1a2',
    description='Как ему не страшно говорить про кортель. Инструкция: https://github.com/mistertay0dimon/cartel',
    author='mistertayodimon',
    author_email='dimondimonych1@outlook.com',
    url='https://github.com/mistertay0dimon/cartel',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'colorama',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Или другой статус разработки
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
)
