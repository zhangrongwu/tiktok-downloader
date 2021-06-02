from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tiktok-downloader',
    version='1.0.0',
    description='Python package to download TikTok\'s profile content or just some videos with their URL.',
    long_description=readme,
    author='Quatrecentquatre',
    author_email='obvious.ly.dev@gmail.com',
    url='https://github.com/quatrecentquatre-404/tiktok-downloader',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
