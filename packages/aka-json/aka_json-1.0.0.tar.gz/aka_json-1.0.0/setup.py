from setuptools import setup, find_packages

setup(
    name="aka_json",
    version="1.0.0",
    author="FluffyFolfie",
    author_email="e-stepanov-ig@yandex.ru",
    description="JSON/JSON5 file handling with dataclass support",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FluffyFolfie/aka_json",
    packages=find_packages(),
    install_requires=[
        "dacite>=1.6.0",
        "json5>=0.9.5"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities"
    ],
    python_requires='>=3.7',
    license="MIT",
    license_files=("LICENSE"),
    keywords=["json", "json5", "dataclass", "serialization"],
    project_urls={
        "Documentation": "https://github.com/FluffyFolfie/aka_json/wiki",
        "Source": "https://github.com/FluffyFolfie/aka_json",
        "Bug Tracker": "https://github.com/FluffyFolfie/aka_json/issues",
    },
    include_package_data=True
)