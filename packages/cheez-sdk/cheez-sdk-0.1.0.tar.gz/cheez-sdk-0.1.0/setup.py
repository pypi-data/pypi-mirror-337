
from setuptools import setup, find_packages

setup(
    name='cheez-sdk',
    version='0.1.0',
    description='SDK for Cheez USB/BLE Devices',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Cheez', 
    url='https://github.com/ewecan/cheez-sdk',
    packages=find_packages(),
    install_requires=[
        'pyserial',
        'aioserial',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
    include_package_data=True,
    package_data={
        'cheez_sdk': ['config/*.json'],
    },
)
