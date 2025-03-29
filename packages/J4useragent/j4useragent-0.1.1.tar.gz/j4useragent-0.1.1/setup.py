from setuptools import setup, find_packages

setup(
    name="J4useragent",
    version="0.1.1",
    description="Generator User-Agent untuk berbagai perangkat",
    author="Saepul Fajar",
    author_email="s.fajar.id@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Fajarrrrky/J4useragent",  
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
