from setuptools import setup, find_packages

setup(
    name="bhp9",  # Your package name
    version="1.0.2",  # Version number
    author="ssskingsss12",
    author_email="smalls3000i@gmail.com",
    description="A powerful Python security tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/yourusername/bhp102",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],  # List dependencies here
    entry_points={
        "console_scripts": [
            "bhp=bhp:main",  # Allows running `bhp` as a command
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
