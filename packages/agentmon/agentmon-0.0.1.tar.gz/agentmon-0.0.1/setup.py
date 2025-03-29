from setuptools import setup, find_packages

setup(
    name="agentmon",
    version="0.0.1",
    author="streamize",
    author_email="admin@streamize.net",
    description="AI Agent Monitoring SDK",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Streamize-llc/agentmon",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
