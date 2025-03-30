from setuptools import setup, find_packages

setup(
    name='mygoogleAuth_fastAPI',
    version='1.1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'oauthlib',
        'starlette',
        'itsdangerous',
    ],
    url='https://github.com/lupin-oomura/mygoogleAuth_fastAPI.git',
    author='Shin Oomura',
    author_email='shin.oomura@gmail.com',
    description='A simple OpenAI function package',
)
