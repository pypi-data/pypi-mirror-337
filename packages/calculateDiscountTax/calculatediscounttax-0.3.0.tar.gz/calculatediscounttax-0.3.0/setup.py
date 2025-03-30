from setuptools import setup, find_packages

setup(
    name='calculateDiscountTax',
    version='0.3.0',
    description='A simple Python library used to calculate the final amount for the given tax rate or discount rate.',
    long_description=open('USAGE.md').read(),
    long_description_content_type='text/markdown',
    author='Nidhi Anandan',
    author_email='x23286873@student.ncirl.ie',
    packages=find_packages(),
    install_requires=[
    ],
    license='MIT',
    python_requires='>=3.7',
)