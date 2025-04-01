# setup.py
from setuptools import setup, find_packages

setup(
    name="vspexhost",
    version="2.0",  # Updated version to 2.0
    description="A python web server designed to help with displaying html if you only have python. This can be used for all purposes including Development, just for fun, and serious topics, or anything.",
    packages=find_packages(),
    install_requires=[
        # Add any dependencies you may have, for example: 'flask', etc.
    ],
    entry_points={  # This part is for creating command-line scripts
        'console_scripts': [
            'vspexhost = vspexhost.vspexhost:main',  # Reference to the main function in your vspexhost.py
        ],
    },
)
