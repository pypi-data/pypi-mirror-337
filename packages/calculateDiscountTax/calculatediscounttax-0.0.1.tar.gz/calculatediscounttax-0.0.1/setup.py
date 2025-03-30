from setuptools import setup, find_packages

setup(
    name='calculateDiscountTax',
    version='0.0.1',
    description='A simple Python library used to calculate the final amount for the given tax rate or discount rate.',
    long_description=open('USAGE.md').read(),
    long_description_content_type='text/markdown',
    author='Nidhi Anandan',
    author_email='x23286873@student.ncirl.ie',
    packages=find_packages(),
    install_requires=[
        'decimal',
        'numbers',
    ],
    license='MIT',
    python_requires='>=3.7',
)