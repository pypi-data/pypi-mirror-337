from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="cartel",  # Замените на желаемое имя пакета
    version="1.0",
    description="Как ему не страшно говорить про кортель",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="mistertayodimon",  # Замените на своё имя
    author_email="dimondimonych1@outlook.com",  # Замените на свой email
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Укажите минимальную версию Python
    # url="https://github.com/mistertay0dimon"
)