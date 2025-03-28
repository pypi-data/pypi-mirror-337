from pathlib import Path

from setuptools import find_packages, setup

with open(Path(__file__).parent / 'README.rst') as f:
    long_description = f.read()


setup(
    name='league-ranker',
    version='1.0.5',
    packages=find_packages(exclude=('tests',)),
    package_data={'league_ranker': ['py.typed']},
    url='https://ranker.readthedocs.io/en/latest/',
    project_urls={
        'Documentation': 'https://ranker.readthedocs.io/en/latest/',
        'Code': 'https://github.com/PeterJCLaw/ranker',
        'Issue tracker': 'https://github.com/PeterJCLaw/ranker/issues',
    },
    description="League ranking for arbitrary numbers of competitors.",
    long_description=long_description,
    author='Student Robotics Competition Software SIG',
    author_email='srobo-devel@googlegroups.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Typing :: Typed',
    ],
    python_requires='>=3.7',
    zip_safe=True,
)
