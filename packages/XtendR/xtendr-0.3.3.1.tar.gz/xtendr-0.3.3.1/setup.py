if __name__ == "__main__":
    from setuptools import setup, find_packages
    from pathlib import Path
    this_directory = Path(__file__).parent
    long_description = (this_directory / "README.md").read_text()

    setup(
        name="XtendR",
        version="0.3.3.1",
        packages=find_packages(),
        install_requires=[],
        author="Jan Lerking",
        author_email="",
        description="A modular plugin system for Python.",
        url="https://www.gitea.com/Lerking/XtendR",
        classifiers=[
            "Programming Language :: Python :: 3.11",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.11',
        long_description=long_description,
        long_description_content_type='text/markdown'
    )