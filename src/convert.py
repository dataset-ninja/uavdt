import os
import shutil
from collections import defaultdict

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import (
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # Possible structure for bbox case. Feel free to modify as you needs.
    uav_m_train_path = "/home/alex/DATASETS/TODO/UAVDT/M_attr/train"
    uav_m_test_path = "/home/alex/DATASETS/TODO/UAVDT/M_attr/test"
    uav_m_pathes = "/home/alex/DATASETS/TODO/UAVDT/UAV-images-M"
    uav_s_pathes = "/home/alex/DATASETS/TODO/UAVDT/UAV-images-S"
    uav_s_attr_path = "/home/alex/DATASETS/TODO/UAVDT/UAV-S-anns/att"
    uav_m_bboxes_path = "/home/alex/DATASETS/TODO/UAVDT/UAV-M-anns/GT"
    uav_s_bboxes_path = "/home/alex/DATASETS/TODO/UAVDT/UAV-S-anns"
    anns_ext = "_gt_whole.txt"

    batch_size = 30

    ds_name_to_data = {
        "train": uav_m_train_path,
        "test": uav_m_test_path,
        "UAVDT-S": uav_s_bboxes_path,
    }

    def create_ann(image_path):
        labels = []
        tags = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        seq = sly.Tag(sequence_meta, value=subfolder)
        tags.append(seq)

        bboxes_data = name_to_coord_data.get(get_file_name_with_ext(image_path))
        if bboxes_data is not None:
            for curr_bboxes_data in bboxes_data:
                l_tags = []
                if ds_name != "UAVDT-S":
                    target_id_tag = sly.Tag(target_id_meta, value=curr_bboxes_data[0])
                    l_tags.append(target_id_tag)

                    out_meta = index_to_out[curr_bboxes_data[-3]]
                    out_tag = sly.Tag(out_meta)
                    l_tags.append(out_tag)

                    occlusion_meta = index_to_occlusion[curr_bboxes_data[-2]]
                    occlusion_tag = sly.Tag(occlusion_meta)
                    l_tags.append(occlusion_tag)

                    obj_class = index_to_class[curr_bboxes_data[-1]]

                    left = curr_bboxes_data[1]
                    right = left + curr_bboxes_data[3]
                    top = curr_bboxes_data[2]
                    bottom = top + curr_bboxes_data[4]

                else:
                    obj_class = vehicle
                    left = curr_bboxes_data[0]
                    right = left + curr_bboxes_data[2]
                    top = curr_bboxes_data[1]
                    bottom = top + curr_bboxes_data[3]

                rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)
                label = sly.Label(rectangle, obj_class, tags=l_tags)
                labels.append(label)

        if ds_name != "UAVDT-S":
            attr_data = seq_to_attr[subfolder]
            for idx, curr_attr_data in enumerate(attr_data):
                if curr_attr_data == 1:
                    curr_meta = idx_to_meta[idx]
                    curr_tag = sly.Tag(curr_meta)
                    tags.append(curr_tag)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    car = sly.ObjClass("car", sly.Rectangle)
    truck = sly.ObjClass("truck", sly.Rectangle)
    bus = sly.ObjClass("bus", sly.Rectangle)
    vehicle = sly.ObjClass("vehicle", sly.Rectangle)

    index_to_class = {1: car, 2: truck, 3: bus}

    sequence_meta = sly.TagMeta("sequence", sly.TagValueType.ANY_STRING)
    target_id_meta = sly.TagMeta("target id", sly.TagValueType.ANY_NUMBER)

    no_out_meta = sly.TagMeta("no out", sly.TagValueType.NONE)
    medium_out_meta = sly.TagMeta("medium out", sly.TagValueType.NONE)
    small_out_meta = sly.TagMeta("small out", sly.TagValueType.NONE)

    index_to_out = {1: no_out_meta, 2: medium_out_meta, 3: small_out_meta}

    no_occlusion_meta = sly.TagMeta("no occlusion", sly.TagValueType.NONE)
    lagre_occlusion_meta = sly.TagMeta("lagre occlusion", sly.TagValueType.NONE)
    medium_occlusion_meta = sly.TagMeta("medium occlusion", sly.TagValueType.NONE)
    small_occlusion_meta = sly.TagMeta("small occlusion", sly.TagValueType.NONE)

    index_to_occlusion = {
        1: no_occlusion_meta,
        2: lagre_occlusion_meta,
        3: medium_occlusion_meta,
        4: small_occlusion_meta,
    }

    daylight_meta = sly.TagMeta("daylight", sly.TagValueType.NONE)
    night_meta = sly.TagMeta("night", sly.TagValueType.NONE)
    fog_meta = sly.TagMeta("fog", sly.TagValueType.NONE)
    low_alt_meta = sly.TagMeta("low alt", sly.TagValueType.NONE)
    medium_alt_meta = sly.TagMeta("medium alt", sly.TagValueType.NONE)
    high_alt_meta = sly.TagMeta("high alt", sly.TagValueType.NONE)
    front_view_meta = sly.TagMeta("front view", sly.TagValueType.NONE)
    side_view_meta = sly.TagMeta("side view", sly.TagValueType.NONE)
    bird_view_meta = sly.TagMeta("bird view", sly.TagValueType.NONE)
    long_term_meta = sly.TagMeta("long term", sly.TagValueType.NONE)

    idx_to_meta = {
        0: daylight_meta,
        1: night_meta,
        2: fog_meta,
        3: low_alt_meta,
        4: medium_alt_meta,
        5: high_alt_meta,
        6: front_view_meta,
        7: side_view_meta,
        8: bird_view_meta,
        9: long_term_meta,
    }

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[car, truck, bus, vehicle],
        tag_metas=[
            sequence_meta,
            target_id_meta,
            no_out_meta,
            medium_out_meta,
            small_out_meta,
            no_occlusion_meta,
            lagre_occlusion_meta,
            medium_occlusion_meta,
            small_occlusion_meta,
            daylight_meta,
            night_meta,
            fog_meta,
            low_alt_meta,
            medium_alt_meta,
            high_alt_meta,
            front_view_meta,
            side_view_meta,
            bird_view_meta,
            long_term_meta,
        ],
    )
    api.project.update_meta(project.id, meta.to_json())

    for ds_name, ds_data in ds_name_to_data.items():

        if ds_name != "UAVDT-S":
            dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        for attr_name in os.listdir(ds_data):
            if attr_name == "att":
                continue
            subfolder = attr_name.split("_")[0]
            curr_images_path = os.path.join(uav_m_pathes, subfolder)
            curr_bboxes_file_path = os.path.join(uav_m_bboxes_path, subfolder + anns_ext)
            curr_attr_file_path = os.path.join(ds_data, attr_name)
            if ds_name == "UAVDT-S":
                curr_images_path = os.path.join(uav_s_pathes, subfolder)
                curr_bboxes_file_path = os.path.join(ds_data, attr_name)
                curr_attr_file_path = os.path.join(ds_data, "att", subfolder + "_att.txt")

            name_to_coord_data = defaultdict(list)
            seq_to_attr = {}

            with open(curr_bboxes_file_path) as f:
                content = f.read().split("\n")
                for idx, row in enumerate(content):
                    if len(row) > 1:
                        bboxes_data = row.split(",")
                        if ds_name == "UAVDT-S":
                            index = idx + 1
                            im_name = "img" + str(index).zfill(6) + ".jpg"
                            name_to_coord_data[im_name].append(list(map(int, bboxes_data)))
                        else:
                            im_name = "img" + bboxes_data[0].zfill(6) + ".jpg"
                            name_to_coord_data[im_name].append(list(map(int, bboxes_data[1:])))

            with open(curr_attr_file_path) as f:
                content = f.read().split("\n")[0].split(",")
                seq_to_attr[subfolder] = list(map(int, content))

            images_names = os.listdir(curr_images_path)

            progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

            for images_names_batch in sly.batched(images_names, batch_size=batch_size):
                img_pathes_batch = []
                img_names_batch = []
                for image_name in images_names_batch:
                    img_pathes_batch.append(os.path.join(curr_images_path, image_name))
                    img_names_batch.append(subfolder + "_" + image_name)

                img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
                img_ids = [im_info.id for im_info in img_infos]

                anns = [create_ann(image_path) for image_path in img_pathes_batch]
                api.annotation.upload_anns(img_ids, anns)

                progress.iters_done_report(len(images_names_batch))

    return project
