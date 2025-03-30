from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="EnvBider",
    version="0.1.0a1",  # Alpha release version
    packages=find_packages(),
    description="A Python library for simplified environment variable management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/EnvBider",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="environment, configuration, env, dotenv, settings",
    python_requires=">=3.6",
    project_urls={
        "Bug Tracker": "https://github.com/user/EnvBider/issues",
        "Documentation": "https://github.com/user/EnvBider#readme",
        "Source Code": "https://github.com/user/EnvBider",
    },
)