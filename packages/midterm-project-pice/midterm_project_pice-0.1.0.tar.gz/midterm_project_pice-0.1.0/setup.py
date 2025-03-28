from setuptools import setup, find_packages

setup(
    name='midterm-project-pice',
    version='0.1.0',
    author='Your Name',
    author_email='ptope@g.harvard.edu',
    description='A package for collecting and analyzing symptom frequency data from online sources.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'scikit-learn',
        'plotly',
        'seaborn',
        'scipy',
        'requests',
        'beautifulsoup4',
        'pytrends'
    ],
    entry_points={
        'console_scripts': [
            'symptom-pca=analysis.symptom_pca:cli',  # maps command to function
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
