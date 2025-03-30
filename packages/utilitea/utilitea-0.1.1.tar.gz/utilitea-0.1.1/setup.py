if __name__ == "__main__":
    from setuptools import setup, find_packages
    from pathlib import Path
    this_directory = Path(__file__).parent
    long_description = (this_directory / "README.md").read_text()

    setup(
        name="utilitea",
        version="0.1.1",
        packages=find_packages(),
        install_requires=[],
        author="Jan Lerking",
        author_email="",
        description="A collection of convenience functions and classes for Python.",
        url="https://www.gitea.com/Lerking/utilitea",
        classifiers=[
            "Programming Language :: Python :: 3.11",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.11',
        long_description=long_description,
        long_description_content_type='text/markdown'
    )