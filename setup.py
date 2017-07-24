from setuptools import setup

REQUIRES = [
    'markdown',
]

SOURCES = []

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name="mdx-variables",
    version="0.1.3",
    url='http://github.com/CTPUG/mdx_variables',
    license='MIT',
    description="A variables extension for Markdown",
    long_description=long_description,
    author='CTPUG',
    author_email='ctpug@googlegroups.com',
    py_modules=[
        'mdx_variables',
    ],
    install_requires=REQUIRES,
    dependency_links=SOURCES,
    setup_requires=[
        # Add setuptools-git, so we get correct behaviour for
        # include_package_data
        'setuptools_git >= 1.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
