import json
from matplotlib import pyplot
import numpy
import os

CONFIG = {

}

SAMPLE_NAMES = [

]

SUBJECT_IDS = [
]

CELL_TYPES = [
]

CELL_SUBTYPES = {
}

CELL_TYPE_HIERARCHICAL_COLORS = {}
CELL_TYPE_COLORS = {}
SUBJECT_ID_COLORS = {}
AM_COLOR = None
PM_COLOR = None


def load_config(file_path=None):

    global CONFIG
    global SAMPLE_NAMES
    global SUBJECT_IDS
    global CELL_TYPES
    global CELL_SUBTYPES
    global CELL_TYPE_COLORS
    global SUBJECT_ID_COLORS
    global AM_COLOR
    global PM_COLOR
    global CELL_TYPE_HIERARCHICAL_COLORS

    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), "default.json")

    with open(file_path) as new_config_file:
        new_config = json.load(new_config_file)

    for key, value in new_config.items():
        if key == "SAMPLE_NAMES":
            SAMPLE_NAMES = value
        elif key == "SUBJECT_IDS":
            SUBJECT_IDS = value
        elif key == "CELL_TYPES":
            CELL_TYPES = value
        elif key == "CELL_SUBTYPES":
            CELL_SUBTYPES = value
        elif key == "AM_COLOR":
            AM_COLOR = value
        elif key == "PM_COLOR":
            PM_COLOR = value
        elif key == "CELL_TYPE_HIERARCHICAL_COLORS":
            CELL_TYPE_HIERARCHICAL_COLORS = value
        else:
            CONFIG[key] = value

    cell_type_colormap = pyplot.cm.get_cmap("inferno")
    color_list = cell_type_colormap(numpy.linspace(0, 0.9, len(CELL_TYPES)))

    for cell_type_index, cell_type in enumerate(sorted(CELL_TYPES)):
        CELL_TYPE_COLORS[cell_type] = \
            "rgba(%.2f, %.2f, %.2f, %.2f)" % tuple(color_list[cell_type_index])

    subject_colormap = pyplot.cm.get_cmap("viridis")
    color_list = subject_colormap(numpy.linspace(0, 0.9, len(SUBJECT_IDS)))

    for subject_index, subject_id in enumerate(sorted(SUBJECT_IDS)):
        SUBJECT_ID_COLORS[subject_id] = \
            "rgba(%.2f, %.2f, %.2f, %.2f)" % tuple(color_list[subject_index])


def get(key):

    return CONFIG[key]


# Load config on import
load_config()
