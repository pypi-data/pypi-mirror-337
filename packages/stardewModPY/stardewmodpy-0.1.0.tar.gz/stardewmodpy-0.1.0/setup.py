from setuptools import setup, find_packages

setup(
    name='stardewModPY',
    version='0.1.0',
    packages=find_packages(include=['StardewValley', 'StardewValley.*']),
    install_requires=[
        'prettytable'
    ],
    author='Alichan',
    author_email='ecchinya25@gmail.com',
    description='Uma biblioteca para gerar mods usando o Content Pacher em json para Stardew Valley',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',  # O URL do repositório do seu projeto
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
