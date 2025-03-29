from setuptools import setup, find_packages

setup(
    name='pyg4i',
    version='0.1.0',
    author='pyg4i',
    author_email='kigzobadi@gmail.com',
    description='Более удобное использование pyg4i',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'pyg4i',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)