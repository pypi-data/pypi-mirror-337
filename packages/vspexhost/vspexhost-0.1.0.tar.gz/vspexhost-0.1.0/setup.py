# setup.py
from setuptools import setup, find_packages

setup(
    name="vspexhost",
    version="0.1.0",
    description="A python web server designed to help with displaying html if you only have python. This can be used for all purposes including Development, just for fun, and serious topics, or anything.",
    packages=find_packages(),
    install_requires=[
        # List any external dependencies here
    ],
    entry_points={
        'console_scripts': [
            'vspexhost = vspexhost.vspexhost:main',
        ],
    },
)
