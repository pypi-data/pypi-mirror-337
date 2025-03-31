from setuptools import setup, find_packages

setup(
    name="bhp9",
    version="1.0.6",
    author="ssskingsss12",
    author_email="smalls3000i@gmail.com",
    description="A powerful Python security tool",
    packages=find_packages(),
    package_data={
        'bhp': ['bhp.cpython-312-x86_64-linux-gnu.so'],  # Include the compiled Cython file
    },
    entry_points={
        'console_scripts': [
            'bhp9 = bhp.bhp:main',  # This should point to the main function in bhp.py
        ]
    },
    python_requires=">=3.12",
)
