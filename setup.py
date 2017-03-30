from setuptools import find_packages, setup

# PyPI only supports nicely-formatted README files in reStructuredText.
# Newsapps seems to prefer Markdown.  Use a version of the pattern from
# https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules
# to convert the Markdown README to rst if the pypandoc package is
# present.
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, OSError):
    long_description = open('README.md').read()

# Load the version from the version module
exec(open('congressional_tweets/version.py').read())

setup(
        name='congressional_tweets',
        version=__version__,
        author='Geoff Hing',
        author_email='geoffhing@gmail.com',
        url='https://github.com/ghing/congressional-tweets',
        description="Capture tweets from members of congress",
        long_description=long_description,
        packages=find_packages(exclude=["tests", "tests.*"]),
        include_package_data=True,
        install_requires=[
            'tweepy',
            'pymongo',
            'pyzmq',
        ],
        tests_require=[
        ],
        test_suite='tests',
        entry_points={
            'console_scripts': [
                'congressional_tweets=congressional_tweets.cli:main',
            ],
        },
        keywords='twitter congress',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
        ],
)
