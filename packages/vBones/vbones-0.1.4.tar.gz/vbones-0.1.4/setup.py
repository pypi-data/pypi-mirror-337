from setuptools import setup, find_packages

setup(
    name="vBones",
    use_scm_version=True,
    author="Bequeller",
    author_email="example@example.com",
    description="A simple Hello World package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Bequeller/vBones",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 