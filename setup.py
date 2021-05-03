from setuptools import setup

setup(
    name="overcast_stats_extractor",
    version="0.1.0",
    author="David Stephens",
    author_email="dev@dwrs.org",
    packages=["overcast_stats_extractor"],
    entry_points={
        'console_scripts': ["extract-overcast-stats=overcast_stats_extractor.cli:main"]
    },
    license="LICENSE.txt",
    description="Extract some some starts from your Overcast library",
    long_description=open("README.md").read(),
    install_requires=[
        "requests",
        "python-dateutil"
    ],
)
