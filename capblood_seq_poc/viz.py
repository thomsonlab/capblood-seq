import numpy
from matplotlib import pyplot

from . import common

CELL_TYPE_COLOR_MAP = {
    "T Cells": "rgba(0, 104, 55, 255)",
    "CD8 T Cells": "rgba(0, 145, 68, 255)",
    "CD4 T Cells": "rgba(141, 198, 67, 255)",
    "Monocytes": "rgba(170, 39, 45, 255)",
    "CD14 Monocytes": "rgba(230, 59, 67, 255)",
    "CD16 Monocytes": "rgba(237, 37, 40, 255)",
    "B Cells": "rgba(44, 55, 144, 255)",
    "NK Cells": "rgba(65, 36, 20, 255)",
    "Dendritic Cells": "rgba(249, 237, 37, 255)"
}

SUBJECT_ID_COLORS = {}

subject_colormap = pyplot.cm.get_cmap("viridis")
color_list = subject_colormap(numpy.linspace(0, 0.9, len(common.SUBJECT_IDS)))

for subject_index, subject_id in enumerate(sorted(common.SUBJECT_IDS)):
    SUBJECT_ID_COLORS[subject_id] = \
        "rgba(%.2f, %.2f, %.2f, %.2f)" % tuple(color_list[subject_index])
