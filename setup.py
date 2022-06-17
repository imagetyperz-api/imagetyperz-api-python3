import os
from setuptools import setup


def get_packages():
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk("imagetyperzapi3")
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


setup(
    name='imagetyperzapi3',
    url='https://github.com/belvo-finance/imagetyperz-api-python3',
    version='0.3',
    description='Image Typerz interface',
    author='Belvo Finance, S.L.',
    install_requires=[
        'requests'
    ],
    author_email="hello@belvo.com",
    license='MIT',
    packages=get_packages(),
)
