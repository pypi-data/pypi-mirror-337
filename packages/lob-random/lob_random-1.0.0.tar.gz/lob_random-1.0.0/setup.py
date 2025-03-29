from setuptools import setup, find_packages

setup(
    name="lob-random",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "lxml",
        "beautifulsoup4"
    ],
    entry_points={
        'console_scripts': [
            'lob-random = lob_random.lob:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
