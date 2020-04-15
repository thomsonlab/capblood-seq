from setuptools import setup

setup(
    name="capblood-seq",
    version="0.1.0",
    packages=[
        "capblood_seq"
    ],
    install_requires=[
        "pandas>=0.23.0",
        "scrapi>=0.5.0",
        "numpy",
        "plotly",
        "sklearn",
        "scipy",
        "statsmodels"
    ]
)
