from setuptools import setup, find_packages

setup(
    name="ccm_analysis",  # Paketname
    version="0.1.0",  # Initiale Version
    description="A package for performing Convergent Cross Mapping (CCM) analysis on time series data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Karl Balzer",
    author_email="klbalzer@web.de",
    url="https://github.com/chaseU2/CCM_analysis_Python",  # Optional: Link zu deinem Repo
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "scipy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Oder eine andere Lizenz
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
