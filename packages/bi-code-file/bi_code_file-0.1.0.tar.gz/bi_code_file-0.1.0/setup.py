from setuptools import setup, find_packages

setup(
    name="bi_code_file",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,  # Include non-Python files
    package_data={
        "bi_code_file": ["files/*"],  # Include all files inside the 'files' folder
    },
    install_requires=[],
    author="Johnny Sins",
    description="A package to download predefined files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/",  # Update with your repo link
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
