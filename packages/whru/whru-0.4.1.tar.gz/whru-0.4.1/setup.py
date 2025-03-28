from setuptools import setup, find_packages

setup(
    name='whru',
    version='0.4.1',
    description='My custom Python module',
    author='whr819987540',
    author_email='steeliron550@gmail.com',
    packages=find_packages(),
    project_urls={
    "Source": "https://github.com/whr819987540/whru",
    "Bug Tracker": "https://github.com/whr819987540/whru/issues",
    },
    install_requires=[
        "torch>=1.7.0",
        "tensorflow>=2.0.2",
    ],
)