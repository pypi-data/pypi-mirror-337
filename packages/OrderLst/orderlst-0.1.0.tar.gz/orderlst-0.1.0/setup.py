from setuptools import setup, find_packages

setup(
    name='OrderLst',
    version='0.1.0',
    description='Ordena listas de números sin usar sorted',
    author='Skriev',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
