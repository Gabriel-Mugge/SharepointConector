from setuptools import setup

setup(name='conector_sharepoint',
version='0.1',
description='Testing installation of Package',
url='',
author='Gabriel-Mugge',
author_email='',
license='',
packages=['ConectorSharepoint'],
install_requires=[
        "pip install git+https:/github.com/vgrem/Office365-REST-Python-Client.git",
        "treelib",
        "Pillow"
    ],      
zip_safe=False)
