from setuptools import setup

setup(
    name="capblood-seq",
    version="0.2.4",
    packages=[
        "capblood_seq",
        "capblood_seq.config",
        "capblood_seq.resources"
    ],
    author="David Brown",
    author_email="dibidave@gmail.com",
    url="https://github.com/thomsonlab/capblood-seq",
    install_requires=[
        "pandas>=0.23.0",
        "scrapi>=0.5.1",
        "numpy",
        "plotly",
        "sklearn",
        "scipy",
        "statsmodels",
        "matplotlib",
        "pepars",
        "scvi==0.6.8"
    ],
    package_data={
        "capblood_seq.config": [
            "default.json"
        ],
        "capblood_seq.resources": [
            "gene_pathway_dict.pickle",
            "pathway_class_labels.tsv",
            "pathway_classes.csv"
        ]
    },
)
