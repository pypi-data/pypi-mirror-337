from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vibez",
    version="0.1.0",
    description="Lightweight CLI tool to extract file contents for LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/williamgrosset/vibez",
    project_urls={
        "Source": "https://github.com/williamgrosset/vibez",
        "Bug Tracker": "https://github.com/williamgrosset/vibez/issues",
        "Documentation": "https://github.com/williamgrosset/vibez#readme",
    },
    packages=find_packages(),
    install_requires=["pyperclip"],
    entry_points={
        "console_scripts": [
            "vibez=vibez.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    license="MIT",
    include_package_data=True,
)
