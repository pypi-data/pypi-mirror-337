# setup.py

from setuptools import setup, find_packages

setup(
    name="Effortless",
    version="1.3.2",
    packages=find_packages(),
    description="Databases should be Effortless.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://effortless.bboonstra.dev/",
    author="Ben Boonstra",
    author_email="ben@bboonstra.dev",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Natural Language :: English",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires=">=3.9",
    install_requires=[
        "cryptography>=41.0.0",
    ],
    keywords="database, effortless, simple storage, beginner, easy, db",
    project_urls={
        "Bug Tracker": "https://github.com/bboonstra/Effortless/issues",
        "Documentation": "https://effortless.bboonstra.dev",
        "Source Code": "https://github.com/bboonstra/Effortless",
    },
    include_package_data=True,
)
