from setuptools import setup, find_packages

setup(
    name="discord-webhook-tool",
    version="0.1",
    author="Kingbob",
    author_email="business5kingbob@gmail.com",
    description="A Python package for interacting with Discord webhooks, including sending messages, spamming, deleting, and fetching webhook data.",
    url="https://github.com/K1ngbobb/discord-webhook-tool",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
