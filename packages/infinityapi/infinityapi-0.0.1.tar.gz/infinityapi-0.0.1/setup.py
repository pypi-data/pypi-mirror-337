from setuptools import setup, find_packages

setup(
    name="infinityapi",  # Назва пакету
    version="0.0.1",  # Версія пакету
    packages=find_packages(include=["IAPI"]),  # Збирає всі пакети в проекті
    install_requires=[  # Залежності, якщо є
        # наприклад: "numpy", "requests"
    ],
    package_dir={'': 'IAPI'},
    description="InfinityAPI",
    long_description=open("README.md").read(),  # Опис з README
    long_description_content_type="text/markdown",  # Формат опису
    author="AWIMatvey",
    author_email="kmatvij71@gmail.com",
    license="MIT (MODIFIED)",  # Ліцензія
    url="https://itsrealawi.github.io/awisite/"
)

# L:\Python\64\python.exe l:/iapiins/setup.py sdist bdist_wheel
# twine upload dist/*