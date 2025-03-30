from setuptools import find_packages, setup

setup(
    name="ai-translator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.65.0",
        "python-dotenv>=1.0.0",
    ],
    author="Lewis Chou",
    author_email="maninhouse@protonmail.com",
    description="An AI-powered translation tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/maninhouse/ai-translator",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)
