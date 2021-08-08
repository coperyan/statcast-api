from setuptools import setup

setup(
    name='baseball_savant',
    description="Python wrapper for Baseball Savant data",
    url="https://github.com/coperyan/baseball_savant/",

    author='Ryan Cope',
    author_email='ryancopedev@gmail.com',

    version='0.0.1',
    packages=['baseball_savant'],
    install_requires=[
        'requests',
        'importlib; python_version == "2.6"',
    ],

    license='MIT',
    keywords = 'baseball savant API',

    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
    ]

)