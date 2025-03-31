from setuptools import setup, find_packages

setup(
    name='GhObjects',
    version='0.0.1.dev1',
    packages=find_packages(),
    description='A package providing Gitter and lazyload classes',
    author='Lars Kruse',
    author_email='lars@lakruzz.com',
    url='https://github.com/thetechcollective/GhObjects',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    exclude_package_data={'': ['__pycache__/*']},

)