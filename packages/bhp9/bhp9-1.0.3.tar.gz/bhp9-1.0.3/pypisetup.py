from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

setup(
    name="bhp9",
    version="1.0.3",
    author="ssskingsss12",
    author_email="smalls3000i@gmail.com",
    description="A powerful Python security tool",
    packages=find_packages(),
    package_data={"bhp": ["*.so", "*.py"]},  # Ensure .so and .py files are included
    ext_modules=cythonize([Extension("bhp.bhp", ["bhprun.py"])]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
