from setuptools import setup, find_packages
import platform

# Detect the platform to include the correct dynamic library
if platform.system() == 'Linux':
    dynamic_library = 'CloseFormIK.cpython-39-x86_64-linux-gnu.so'
elif platform.system() == 'Windows':
    dynamic_library = 'CloseFormIK.cp39-win_amd64.pyd'
else:
    raise RuntimeError('Unsupported platform')

setup(
    name='robot6Ik',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'cik': [dynamic_library],
    },
    install_requires=[
        'numpy',
        'scipy',
    ],
    python_requires='>=3.9',
    description='closeformik Package with dynamic libraries for both Linux and Windows',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Frank',
    url='https://github.com/Frank/closeformik',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)