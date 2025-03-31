from setuptools import setup, find_packages

setup(
    name="bhp9",
    version="1.0.5",
    author="ssskingsss12",
    author_email="smalls3000i@gmail.com",
    description="A powerful Python security tool",
    packages=find_packages(),
    package_data={"bhp": ["bhp.cpython-312-x86_64-linux-gnu.so", "bhp.py"]},  # Include both .so and .py
    include_package_data=True,  # Ensure files are included
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "bhp9 = bhp.bhp:main",  # Ensure main() exists in bhp.py
        ]
    },
)
