from setuptools import setup, find_packages

setup(
    name='qubelib',
    version='0.1',
    description='Qubelib for our new website, our github: https://github.com/RobloxFactoryRyaturmite/discordus/tree/main',
    packages=find_packages(),
    install_requires=[
        'pillow',  # Adds the Discord library as a dependency
        'tkinter'
    ]
)
