from setuptools import setup, find_packages

setup(
    name='github_storage',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'PyGithub',
        'pycryptodome',
    ],
    entry_points={
        'console_scripts': [
            'github-storage=github_storage.github_storage:main',
        ],
    },
    author='Ahson H.',
    author_email='ahson01@proton.me',
    description='A Python package that uses GitHub repositories as a database for storing and retrieving data.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ahson01/github_storage',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
