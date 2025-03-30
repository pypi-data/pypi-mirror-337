from setuptools import setup, find_packages
import platform

# Define the dynamic libraries for different platforms
dynamic_libraries = {
    'Linux': ['closeformIK/CloseFormIK.cpython-39-x86_64-linux-gnu.so'],
    'Windows': ['closeformIK/CloseFormIK.cp39-win_amd64.pyd']
}

# Detect the platform to include the correct dynamic library
platform_system = platform.system()
if platform_system not in dynamic_libraries:
    raise RuntimeError('Unsupported platform')

setup(
    name='closeformIK',
    version='1.0.3',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'closeformIK': dynamic_libraries[platform_system],
    },
    install_requires=[
        'numpy',
        'scipy',
    ],
    python_requires='>=3.9',
    description='closeformIK Package with dynamic libraries for both Linux and Windows',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Frank',
    url='https://github.com/Frank/closeformIK',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)