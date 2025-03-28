from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()
    
VERSION = '0.1.1'

setup(
    name='sb2gs-fork',
    version=VERSION,
    author='aspizu',
    author_email='aspizu@protonmail.com',
    description='all credits go to aspizu on github',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=[]),
    classifiers=[
        
    ],
    keywords=['scratch'],
    install_requires=[
    ],
    python_requires='>=3.9',
    project_urls={"Source": 'https://github.com/thecommcraft/sb2gs-fork', "Original": 'https://github.com/aspizu/sb2gs'},
)
