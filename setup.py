from setuptools import setup

setup(
    name="capblood-seq-poc",
    version="0.4.3",
    packages=[
        "capblood_seq_poc"
    ],
    install_requires=[
        "pandas>=0.23.0",
        "scrapi>=0.4.3",
        "numpy",
        "plotly",
        "sklearn",
        "scipy",
        "statsmodels"
    ]
)
