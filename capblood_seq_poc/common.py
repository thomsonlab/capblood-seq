SAMPLE_NAMES = [
    "AM1",
    "PM1",
    "AM2",
    "PM2",
    "AM3",
    "PM3"
]

SUBJECT_IDS = [
    "S1",
    "S2",
    "S3",
    "S4"
]

CELL_TYPES = [
    "B Cells",
    "Monocytes",
    "NK Cells",
    "T Cells"
]

CELL_SUBTYPES = [
    "CD4 T Cells",
    "CD8 T Cells",
    "CD14 Monocytes",
    "CD16 Monocytes"
]


def get_datasets(gene_filter_threshold=None, cell_types=None):
    """
    Get all datasets in the study, optionally filtering genes with a user-
    defined threshold.

    :param gene_filter_threshold: Remove genes that are not present at this
        ratio in at least one of the defined cell types

    :param cell_types: If using gene_filter_threshold, specify the cell types
        to consider. Default: capblood_seq_poc.common.CELL_TYPES

    :return: A dictionary of samples and their associated Gene Expression
        Dataset object (from SCRAPi)
    """

    if gene_filter_threshold is not None:
        raise NotImplementedError("David hasn't done this yet")

    if cell_types is not None and gene_filter_threshold is None:
        raise UserWarning("Specifying cell_types doesn't do anything if \
                          gene_filter_threshold isn't set")

    sample_datasets = {}
    gene_set = None

    for sample in SAMPLES:

        workspace_path = os.path.join("..", "data", sample, "workspaces",
                                      WORKSPACE_NAME)

        ged = Gene_Expression_Dataset(workspace_path, name=PIPELINE_NAME)

        sample_datasets[sample] = ged

        if gene_set is None:
            gene_set = set(ged._cell_transcript_counts.column_names)
        else:
            gene_set = gene_set.intersection(
                ged._cell_transcript_counts.column_names)

    gene_list = list(sorted(gene_set))