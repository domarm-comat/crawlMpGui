import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crawlMp",
    version="0.3.1",
    license='MIT',
    author="Martin Domaracký",
    author_email="domarm@comat.sk",
    description="Multiprocess Crawler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/domarm-comat/crawlMp",
    packages=setuptools.find_packages(),
    package_data={'crawlMp.tests': ['fs_files.txt', 'fs_win_files.txt']},
    scripts=['crawlMp/scripts/search_fs_mp'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
    ],
    install_requires=[
        "coverage>=6.2",
        "pyfakefs>=4.5.3",
        "pytest>=6.2.5",
        "pandas>=1.1.5",
        "crawlMp>=0.3.1"
        "PyQt6>=6.2.2"
    ],
    extras_requires={
    },
    python_requires='>=3.6',
)
