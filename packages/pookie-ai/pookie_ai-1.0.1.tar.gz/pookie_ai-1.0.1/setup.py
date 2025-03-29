from setuptools import setup, find_packages

setup(
    name='pookie-ai',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'rich',
        'google-generativeai', 
        'inquirer',
        'argparse'
    ],
    entry_points={
        'console_scripts': [
            'pookie=pookie.cli:main',
        ],
    },
    description='Pookie: An AI-powered terminal assistant',
    author='Aryan Dev',
    author_email='your_email@example.com',
    url='https://github.com/Aryandev12/pookie',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
