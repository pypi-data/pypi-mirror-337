from setuptools import setup, find_packages

setup(
    name='gitactiontest',
    version='1.0.3',
    description='git action test',
    author='Lian Park',
    author_email='g1000white@gmail.com',
    url='',
    install_requires=['selenium',],
    packages=find_packages(exclude=[]),
    keywords=['python tutorial', 'pypi'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)