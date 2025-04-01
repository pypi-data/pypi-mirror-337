from setuptools import setup

setup(
    name="bhp9",
    version="1.0.8",
    packages=["bhp"],  # Package the bhp directory
    package_data={
        "bhp": [
            "bhp.cpython-312-x86_64-linux-gnu.so",  # Include .so file
            "bhp.o",                                # Include .o file
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "bhp9 = bhp.bhp:main",  # Make sure the wrapper file imports the main function from the .so file
        ]
    },
)
