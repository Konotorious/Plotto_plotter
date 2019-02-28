from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()   

with open('LICENSE') as f:
    license = f.read()

setup(
    name='plotter',
    version='0.1.0',
    description='A random plot generator running on William Wallace Cook's Plotto',
    long_description=readme,
    author='Mark Neznansky',
    author_email='mark.neznansky@pm.me',
    url='https://github.com/Konotorious/Plotto_plotter',
    license=license,
    packages=find_packages(exclude=('tests'))
)
