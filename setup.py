from setuptools import setup, find_packages

setup(
    name='reaper',
    version='0.1.0',
    description='Utility to manage rpm repositories',
    long_description=readme,
    author='Philipp Matti',
    author_email='philippmatti@gmail.com',
    packages=find_packages('src'),
    package_dir={'':'src'},
    install_requires=[]
)
