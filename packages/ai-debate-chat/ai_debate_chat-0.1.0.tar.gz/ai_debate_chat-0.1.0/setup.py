from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai_debate_chat",
    version="0.1.0",
    author="Amir Mirfallahi",
    author_email="mirfallahi2009@gmail.com",  # Replace with your actual email
    description="A package for AI debate and chat functionalities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Amir-Mirfallahi/ai-debate-chat",  # Replace with your actual repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "beautifulsoup4>=4.13.3",
        "faiss-cpu>=1.10.0",
        "g4f>=0.4.9",
        "langchain-community>=0.3.20",
        "langchain-core>=0.3.48",
        "langchain-huggingface>=0.1.2",
        "langchain-text-splitters>=0.3.7",
        "nltk>=3.9.1",
        "numpy>=2.2.4",
        "requests>=2.32.3",
        "torch>=2.6.0",
        "transformers>=4.50.0",
        "python-dotenv>=1.0.1",
        "sentence-transformers>=3.4.1",
    ],
)
