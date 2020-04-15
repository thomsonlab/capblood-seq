from setuptools import setup

setup(
    name="capblood-seq",
    version="0.1.0",
    packages=[
        "capblood_seq",
        "capblood_seq.config",
        "capblood_seq.resources"
    ],
    install_requires=[
        "pandas>=0.23.0",
        "scrapi>=0.5.0",
        "numpy",
        "plotly",
        "sklearn",
        "scipy",
        "statsmodels",
        "matplotlib"
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
