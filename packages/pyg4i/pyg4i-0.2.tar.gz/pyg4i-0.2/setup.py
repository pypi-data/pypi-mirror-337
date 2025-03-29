from setuptools import setup, find_packages

setup(
    name='pyg4i',
    version='0.2',
    author='pyg4i',
    author_email='kigzobadi@gmail.com',
    description='Более удобное использование g4f',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'g4f',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)