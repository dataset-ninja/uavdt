from dataset_tools.templates import AnnotationType
from src.settings import ANNOTATION_TYPES
from typing import List

###############################################################################
# ! Set up values if you want to change default values of visualizations
###############################################################################

SAMPLE_RATE = 1  # make less if dataset is too big

# * Preview class to visualize in SUMMARY.md overview section
# * Literal["ClassesPreview", "HorizontalGrid", "SideAnnotationsGrid", "Poster", "HorizontalGridAnimated", "VerticalGridAnimated"]
# * If None, then preview_class will be set automatically to "ClassesPreview"
PREVIEW_CLASS = "Poster"

IS_DETECTION_TASK: bool = None  # ? Set True if you want to visualize only bbox annotations
if IS_DETECTION_TASK is None:
    IS_DETECTION_TASK = ANNOTATION_TYPES == [AnnotationType.ObjectDetection()]

###############################################################
####### * Set up visualization params for Poster class ########
POSTER_IS_DETECTION_TASK: bool = IS_DETECTION_TASK
POSTER_TITLE: str = None
###############################################################


###############################################################
#### * Set up visualization params for HorizontalGrid class ###
HORIZONTAL_GRID_ROWS: int = None
HORIZONTAL_GRID_COLS: int = None
HORIZONTAL_GRID_IS_DETECTION_TASK: bool = IS_DETECTION_TASK
###############################################################


###############################################################
#### * Set up visualization params for VerticalGrid class #####
VERTICAL_GRID_ROWS: int = None
VERTICAL_GRID_COLS: int = None
VERTICAL_GRID_IS_DETECTION_TASK: bool = IS_DETECTION_TASK
###############################################################


###############################################################
# * Set up visualization params for SideAnnotationsGrid class #
SIDE_ANNOTATIONS_GRID_ROWS: int = None
SIDE_ANNOTATIONS_GRID_COLS: int = None
SIDE_ANNOTATIONS_GRID_IS_DETECTION_TASK: bool = IS_DETECTION_TASK
###############################################################


###############################################################
###### * Set up visualization params for Previews class #######
PREVIEWS_IS_DETECTION_TASK: bool = IS_DETECTION_TASK
###############################################################

###############################################################
### * Set up visualization params for ClassesPreview class ####
CLASSES_PREVIEW_ROW_HEIGHT: int = None
CLASSES_PREVIEW_PADDINGS: dict = None
CLASSES_PREVIEW_ROWS: int = None
CLASSES_PREVIEW_GAP: int = None
CLASSES_PREVIEW_TAGS: List[str] = None
# default {"top": "10%", "bottom": "10%", "left": "10%", "right": "10%"}
# set % or px as string values (e.i. "10%" or "10px")
###############################################################


###############################################################
### * Set up visualization params for ClassesHeatmaps class ###
# args for "to_image" method
DRAW_STYLE: str = None  # "inside_white" or "outside_black"
HEATMAP_ROWS: int = None
HEATMAP_COLS: int = None
HEATMAP_GRID_SPACING: int = None
HEATMAP_OUTER_GRID_SPACING: int = None
HEATMAP_OUTPUT_WIDTH: int = (
    None  # 1 class in dataset? -> 1600px for portrait images, 2200px for landscape
)
###############################################################


##################################
###### ? Do not edit bellow #####
##################################


def get_visualization_options():
    vis_settings = {
        "Poster": {
            "title": POSTER_TITLE,
            "is_detection_task": POSTER_IS_DETECTION_TASK,
            "num_classes": None if CLASSES_PREVIEW_TAGS is None else len(CLASSES_PREVIEW_TAGS),
        },
        "HorizontalGrid": {
            "rows": HORIZONTAL_GRID_ROWS,
            "cols": HORIZONTAL_GRID_COLS,
            "is_detection_task": HORIZONTAL_GRID_IS_DETECTION_TASK,
        },
        "VerticalGrid": {
            "rows": VERTICAL_GRID_ROWS,
            "cols": VERTICAL_GRID_COLS,
            "is_detection_task": VERTICAL_GRID_IS_DETECTION_TASK,
        },
        "SideAnnotationsGrid": {
            "rows": SIDE_ANNOTATIONS_GRID_ROWS,
            "cols": SIDE_ANNOTATIONS_GRID_COLS,
            "is_detection_task": SIDE_ANNOTATIONS_GRID_IS_DETECTION_TASK,
        },
    }

    checked_vis_settings = {}

    for class_name, class_settings in vis_settings.items():
        new_class_settings = {}
        for field, value in class_settings.items():
            if value is not None:
                new_class_settings[field] = value
        if len(new_class_settings) > 0:
            checked_vis_settings[class_name] = new_class_settings

    return checked_vis_settings


def get_stats_options():
    stats_settings = {
        "ClassesPreview": {
            "row_height": CLASSES_PREVIEW_ROW_HEIGHT,
            "pad": CLASSES_PREVIEW_PADDINGS,
            "rows": CLASSES_PREVIEW_ROWS,
            "gap": CLASSES_PREVIEW_GAP,
            "tags": CLASSES_PREVIEW_TAGS,
        },
        "ClassesHeatmaps": {
            "draw_style": DRAW_STYLE,
            "rows": HEATMAP_ROWS,
            "cols": HEATMAP_COLS,
            "grid_spacing": HEATMAP_GRID_SPACING,
            "outer_grid_spacing": HEATMAP_OUTER_GRID_SPACING,
            "output_width": HEATMAP_OUTPUT_WIDTH,
        },
        "Previews": {
            "is_detection_task": PREVIEWS_IS_DETECTION_TASK,
        },
        "Other": {"sample_rate": SAMPLE_RATE},
    }

    checked_stats_settings = {}

    for class_name, class_settings in stats_settings.items():
        new_class_settings = {}
        for field, value in class_settings.items():
            if value is not None:
                new_class_settings[field] = value
        if len(new_class_settings) > 0:
            checked_stats_settings[class_name] = new_class_settings

    return checked_stats_settings
