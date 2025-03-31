from setuptools import setup, find_packages

setup(
    name="pdefinder",  # your package name on PyPI
    version="0.1.7",
    description="A package for discovering PDEs using data-driven techniques",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Amartya Roy", 
    author_email="srz248670@iitd.ac.in",
    url="https://github.com/Amartya-Roy/pdefinder",  # optional: your repo URL
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        "numpy",
        "scipy",
        "torch",
        "openai",
        # list any other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "pdefinder = pdefinder.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # if applicable
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
