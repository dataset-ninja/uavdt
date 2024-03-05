import os
import shutil

import supervisely as sly
from supervisely.io.fs import (
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s
from dataset_tools.convert import unpack_if_archive


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # Possible structure for bbox case. Feel free to modify as you needs.

    root_path = ""
    images_folder = "images"
    bboxes_folder = "labels"
    batch_size = 30
    img_ext = ".png"
    ann_ext = ".txt"

    def create_ann(image_path):
        labels, img_tags, label_tags = [], [], []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_width = image_np.shape[1]

        file_name = get_file_name(image_path)
        curr_anns_dirpath = ""
        ann_path = os.path.join(curr_anns_dirpath, file_name + ann_ext)

        if file_exists(ann_path):
            with open(ann_path) as f:
                content = f.read().split("\n")
                for curr_data in content:
                    if len(curr_data) != 0:
                        curr_data = list(map(float, curr_data.split(" ")))

                        left = int((curr_data[1] - curr_data[3] / 2) * img_width)
                        right = int((curr_data[1] + curr_data[3] / 2) * img_width)
                        top = int((curr_data[2] - curr_data[4] / 2) * img_height)
                        bottom = int((curr_data[2] + curr_data[4] / 2) * img_height)

                        rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)

                        for obj_class in obj_classes:
                            if obj_class.name == idx2clsname[curr_data[0]]:
                                curr_obj_class = obj_class
                                break
                        label = sly.Label(rectangle, curr_obj_class, label_tags)
                        labels.append(label)

        return sly.Annotation(img_size=(img_height, img_width), labels=labels, img_tags=img_tags)

    class_names = ["class1", "class2", ...]
    idx2clsname = {}
    obj_classes = [sly.ObjClass(name, sly.Rectangle) for name in class_names]

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=obj_classes)
    api.project.update_meta(project.id, meta.to_json())

    for ds_name in os.listdir(root_path):
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)
        dataset_path = os.path.join(root_path, ds_name)

        images_pathes = sly.fs.list_files_recursively(dataset_path, valid_extensions=[img_ext])

        pbar = tqdm(desc=f"Create dataset '{ds_name}'", total=len(images_pathes))
        for images_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
            images_names_batch = [
                get_file_name_with_ext(image_path) for image_path in images_pathes_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, images_pathes_batch)
            img_ids = [image.id for image in img_infos]

            anns = [create_ann(image_path) for image_path in images_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            pbar.update(len(images_names_batch))
    return project
