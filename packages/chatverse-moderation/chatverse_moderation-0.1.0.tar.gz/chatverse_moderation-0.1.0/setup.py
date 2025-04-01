from setuptools import setup, find_packages

setup(
    name="chatverse_moderation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "textblob",
        "nltk"
    ],
    author="Hari Prasanna Kumar",
    author_email="your.email@example.com",
    description="Custom library for sentiment analysis and content moderation in chat applications.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/chatverse-moderation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
