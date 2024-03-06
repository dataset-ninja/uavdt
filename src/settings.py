from typing import Dict, List, Literal, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "UAVDT"
PROJECT_NAME_FULL: str = "UAVDT Dataset"
HIDE_DATASET = False  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.Custom()
APPLICATIONS: List[Union[Industry, Domain, Research]] = [
    Domain.DroneInspection(),
]
CATEGORY: Category = Category.Drones()

CV_TASKS: List[CVTask] = [CVTask.ObjectDetection()]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.ObjectDetection()]

RELEASE_DATE: Optional[str] = "2018-03-26"  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = None

HOMEPAGE_URL: str = "https://sites.google.com/view/grli-uavdt/%E9%A6%96%E9%A1%B5"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 14716862
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/uavdt"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = {
    "UAVDT-Benchmark-M": "https://drive.google.com/file/d/1m8KA6oPIRK_Iwt9TYFquC87vBc_8wRVc/view?usp=sharing",
    "DET/MOT toolkit": "https://drive.google.com/open?id=19498uJd7T9w4quwnQEy62nibt3uyT9pq",
    "Attributes": "https://drive.google.com/open?id=1qjipvuk3XE3qU3udluQRRcYuiKzhMXB1",
    "UAVDT-Benchmark-S": "https://drive.google.com/open?id=1661_Z_zL1HxInbsA2Mll9al-Ax6Py1rG",
    "SOT toolkit": "https://drive.google.com/open?id=1YMFTBatK6qUrtnIe4fZNMZ9FpCpD2cxm",
}
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]] or Literal["predefined"]] = {
    "car": [230, 25, 75],
    "truck": [60, 180, 75],
    "bus": [255, 225, 25],
    "vehicle": [0, 130, 200],
}
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[Union[str, List[str], Dict[str, str]]] = "https://arxiv.org/pdf/1804.00518"
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = None

CITATION_URL: Optional[str] = None
AUTHORS: Optional[List[str]] = [
    "Dawei Du",
    "Yuankai Qi",
    "Hongyang Yu",
    "Yifan Yang",
    "Kaiwen Duan",
    "Guorong Li",
    "Weigang Zhang",
    "Qingming Huang",
    "Qi Tian",
]
AUTHORS_CONTACTS: Optional[List[str]] = ["dawei.du@vipl.ict.ac.cn"]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = [
    "University of Chinese Academy of Sciences, China",
    "Harbin Institute of Technology, China",
    "The University of Texas at San Antonio, USA",
]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = [
    "https://english.ucas.ac.cn/",
    "http://en.hit.edu.cn/",
    "https://www.utsa.edu/",
]

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = {
    "occlusions types": ["no occlusion", "lagre occlusio", "medium occlusion", "small occlusion"],
    "out of views": ["no out", "medium out", "small out"],
    "weather conditions": ["daylight", "night", "fog"],
    "flying altitudes": ["low alt", "medium alt", "high alt"],
    "camera views": ["front view", "side view", "bird view"],
    "__POSTTEXT__": "Additionally, every image marked with its ***sequence*** tag, labels marked with ***target id*** and ***long term*** tags. Explore its in Supervisely labelling tool",
}
TAGS: Optional[List[str]] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["authors_contacts"] = AUTHORS_CONTACTS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
