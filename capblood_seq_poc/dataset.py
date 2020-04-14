import os

import numpy
from scrapi.dataset import Gene_Expression_Dataset

from . import common


class Capblood_Seq_Dataset:

    def __init__(self, data_directory="data", pipeline_name=None):
        self._data_directory = data_directory
        self._sample_datasets = {}
        self._gene_list = []
        self._is_loaded = False
        self._pipeline_name = pipeline_name

    def load(self):
        """
        Load all sample workspaces.

        :return: None
        """

        if self._is_loaded:
            return

        intersecting_genes = None

        for sample_name in common.SAMPLE_NAMES:

            workspace_path = os.path.join(self._data_directory, sample_name)
            if self._pipeline_name:
                ged = Gene_Expression_Dataset(
                    workspace_path, name=self._pipeline_name)
            else:
                ged = Gene_Expression_Dataset(workspace_path)

            self._sample_datasets[sample_name] = ged

            if intersecting_genes is None:
                intersecting_genes = set(ged.get_genes())
            else:
                intersecting_genes = intersecting_genes.intersection(
                    ged.get_genes())

        self._gene_list = list(sorted(intersecting_genes))

        for sample_name, ged in self._sample_datasets.items():
            ged.filter_genes(self._gene_list)

        self._is_loaded = True

    def get_num_genes(self):
        return len(self._gene_list)

    def filter_unlabeled_cells(self, labels=None):
        """
        Inspect all the cells in each sample and filter in place any that are
        not labeled by one of the provided labels.

        :param labels: The labels to keep. By default, filters all cells that
            don't have one of capblood_seq.common.SUBJECT_IDS or
            capblood_seq.common.CELL_TYPES
        :return: None
        """

        if labels is None:
            labels = common.CELL_TYPES + common.SUBJECT_IDS

        for sample, ged in self._sample_datasets.items():
            ged.filter_unlabeled_cells(labels)

    def filter_multi_labeled_cells(self, labels):
        """
        Inspect all the cells in each sample and filter in place any that are
        labeled by more than one of the given labels.

        :param labels: The labels to inspect.
        :return: None
        """

        for sample, ged in self._sample_datasets.items():

            cells_so_far = set()
            filter_barcodes = set()

            for label in labels:

                if label not in ged.get_labels():
                    continue

                labeled_cells = ged.get_cells(label)

                for cell_barcode in labeled_cells:
                    if cell_barcode in cells_so_far:
                        filter_barcodes.add(cell_barcode)
                    cells_so_far.add(cell_barcode)

            ged.filter_cells(filter_barcodes)

    def get_combined_transcript_counts(self):

        combined_transcript_counts = []

        for sample, ged in self._sample_datasets.items():
            cell_transcript_counts = ged.get_cell_transcript_counts()
            cell_transcript_counts = cell_transcript_counts.to_array()
            combined_transcript_counts.append(cell_transcript_counts)

        combined_transcript_counts = numpy.concatenate(
            combined_transcript_counts, axis=0)

        return combined_transcript_counts

    def get_num_cells(
            self,
            sample,
            cell_type=None,
            subject_id=None):

        filter_labels = []

        if cell_type is not None:
            filter_labels.append(cell_type)
        if subject_id is not None:
            if subject_id not in self._sample_datasets[sample].get_labels():
                return 0
            filter_labels.append(subject_id)

        cells = self._sample_datasets[sample].get_cells(filter_labels)

        return len(cells)

    def get_transcript_counts(
            self,
            sample,
            cell_type=None,
            subject_id=None,
            normalized=False):

        filter_labels = []

        if cell_type is not None:
            filter_labels.append(cell_type)
        if subject_id is not None:
            if subject_id not in self._sample_datasets[sample].get_labels():
                return None
            filter_labels.append(subject_id)

        sample_transcript_counts = \
            self._sample_datasets[sample].get_cell_transcript_counts(
                filter_labels=filter_labels, normalized=normalized)

        return sample_transcript_counts