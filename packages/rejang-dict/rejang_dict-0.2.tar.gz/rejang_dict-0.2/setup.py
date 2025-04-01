from setuptools import setup, find_packages

setup(
    name='rejang_dict',
    version='0.2',
    packages=find_packages(),
    install_requires=['requests', 'termcolor'],
    entry_points={
        'console_scripts': [
        'rejang-dict = rejang_dict.main:main',
        ],
    },
)

