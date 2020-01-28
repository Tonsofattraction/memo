from setuptools import setup

setup(
    name='memo',
    version='0.1',
    py_modules=['memo'],
    install_requires=[
        'pyyaml',
    ],
    maintainer='Tonsofattraction (kuznetsov.d.p@gmail.com)',
    maintainer_email='kuznetsov.d.p@gmail.com',
    url='https://github.com/Tonsofattraction/memo',
    entry_points={
        'console_scripts': [
            'memo = memo:main',
        ],
    },
)