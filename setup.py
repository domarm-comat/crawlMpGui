import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crawlMpGui",
    version="0.0.5",
    license='MIT',
    author="Martin Domaracký",
    author_email="domarm@comat.sk",
    description="GUI for CrawlMp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/domarm-comat/crawlMpGui",
    packages=setuptools.find_packages(),
    #package_data={'crawlMp.tests': ['fs_files.txt', 'fs_win_files.txt']},
    scripts=['crawlMpGui/scripts/search_fs_mp_gui'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
    ],
    install_requires=[
        "crawlMp>=0.3.7",
        "PyQt6>=6.2.2"
    ],
    extras_requires={
    },
    python_requires='>=3.6',
)
