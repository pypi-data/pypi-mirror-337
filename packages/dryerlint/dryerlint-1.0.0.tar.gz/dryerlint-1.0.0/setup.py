from setuptools import setup

setup(
    name='dryerlint',
    version='1.0.0',
    py_modules=['dryerlint'],
    install_requires=[],
    entry_points='''
        [console_scripts]
        dryerlint=dryerlint:main
    ''',
    author='Charlie',
    description='🧺 DryerLint - Remove the Fuzz. A Python-powered code quality and linting tool.',
    long_description = open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)