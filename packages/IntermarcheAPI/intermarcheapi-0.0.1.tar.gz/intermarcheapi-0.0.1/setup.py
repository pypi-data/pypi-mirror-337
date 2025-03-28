from setuptools import setup, find_packages

setup(
    name='IntermarcheAPI',
    version='0.0.1',
    packages=find_packages(),
    description='API d\'intermarche simplement sur Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Hugo Hennetin',
    author_email='hugo.hennetin@proton.me',
    url='https://github.com/Zerbaib/IntermarcheAPI',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=[],
)