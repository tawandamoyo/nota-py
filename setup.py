from setuptools import setup, find_packages

setup(
    name="kindle-highlights",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'sentence-transformers',
        'scikit-learn',
        'numpy',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'notaReader=src.cli:main',
        ],
    },
    author="Tawanda Moyo",
    author_email="moyotawanda@gmail.com",
    description="A tool for analyzing Kindle highlights and notes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kindle-highlights",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)