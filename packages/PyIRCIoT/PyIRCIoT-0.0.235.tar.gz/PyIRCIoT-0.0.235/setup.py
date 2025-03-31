from setuptools import setup, find_packages

setup(
    name='PyIRCIoT',
    version='0.0.235',
    description='IRC-IoT is the universal protocol for building IoT',
    long_description_content_type='text/markdown',
    long_description = open('README.md').read(),
    packages=find_packages() + [
     'PyIRCIoT.esp8266',
     'PyIRCIoT.examples',
     'PyIRCIoT.iimakecert',
     'PyIRCIoT.techdoc',
     'PyIRCIoT.services',
     'PyIRCIoT.testing'
    ],
    author='Alexey Woronov',
    author_email='alexey@woronov.ru',
    license='MIT',
    url='https://github.com/Markatrafik/PyIRCIoT',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
     "twofish>=0.3.0",
     "PyNaCl>=1.3.0",
     "ifaddr>=0.1.6",
    ],
    classifiers=[
     "Programming Language :: Python :: 3",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
    ]
)

