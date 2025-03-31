import setuptools

setuptools.setup(
    name="textsage",
    version="0.1.0",
    packages=setuptools.find_packages(),
    install_requires=["ollama"],
    author="Shivang Agarwal",
    description="A simple library to set up Ollama and summarize text using local LLMs.",
    url="https://github.com/shivang98/textsage",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
