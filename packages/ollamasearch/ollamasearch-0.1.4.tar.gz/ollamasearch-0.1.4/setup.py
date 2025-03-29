from setuptools import setup, find_packages

setup(
    name="ollamasearch",
    version="0.1.4", 
    packages=find_packages(),
    install_requires=[
        'requests',
        'platformdirs', # Added for cross-platform config directory
        'sentence-transformers',
        'faiss-cpu',
        'numpy'
    ],
    entry_points={
        "console_scripts": [
            "ollamasearch=ollamasearch.app:main"
        ]
    },
    include_package_data=True,
    description="A Python package for intregating ollama with web with Web Serach and RAG.",
    author="Nikhil", 
    author_email="nikhilkhanwani60@gmail.com", 
)
