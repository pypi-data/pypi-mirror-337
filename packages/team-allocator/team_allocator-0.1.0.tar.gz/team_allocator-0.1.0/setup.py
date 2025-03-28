from setuptools import setup, find_packages

setup(
    name='team_allocator',
    version='0.1.0',
    author='Vineet Kumar',
    author_email='whyvineet@outlook.com',
    description='A flexible team allocation library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/whyvineet/team_allocator',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[],
    extras_require={
        'dev': ['pytest', 'twine', 'wheel']
    }
)