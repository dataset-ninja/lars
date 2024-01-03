import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import file_exists, get_file_name
from supervisely.io.json import load_json_file
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    train_images_path = "/home/alex/DATASETS/TODO/LaRS/lars_v1.0.0_images_seq/train/images_seq"
    val_images_path = "/home/alex/DATASETS/TODO/LaRS/lars_v1.0.0_images_seq/val/images_seq"
    test_images_path = "/home/alex/DATASETS/TODO/LaRS/lars_v1.0.0_images_seq/test/images_seq"

    train_anns_path = "/home/alex/DATASETS/TODO/LaRS/lars_v1.0.0_annotations/train"
    val_anns_path = "/home/alex/DATASETS/TODO/LaRS/lars_v1.0.0_annotations/val"

    bboxes_file_name = "panoptic_annotations.json"
    tags_file_name = "image_annotations.json"
    masks_folder = "semantic_masks"

    images_ext = ".jpg"
    masks_ext = ".png"

    batch_size = 30

    ds_name_to_split = {
        "val": (val_images_path, val_anns_path),
        "train": (train_images_path, train_anns_path),
        "test": (test_images_path, None),
    }

    def create_ann(image_path):
        labels = []
        tags = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        image_name = get_file_name(image_path)

        if image_name[:2] != "or":
            seq_name = image_name.split("_")[0]
            if image_name.split("_")[1] == "old":
                seq_name = "mastr old"
        elif image_name[:9] == "orca_flow":
            seq_name = "orca flow"
        else:
            seq_name = image_name[:18]

        seq_name_tag = sly.Tag(seq_name_meta, value=seq_name)
        tags.append(seq_name_tag)

        seq_id_value = image_name.split("_")[-2]
        seq_id = sly.Tag(seq_id_meta, value=seq_id_value)
        tags.append(seq_id)

        mask_path = os.path.join(masks_path, image_name + masks_ext)
        if file_exists(mask_path):
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            unique_pixels = np.unique(mask_np)

            for pixel in unique_pixels:
                if pixel not in list(pixel_to_class.keys()):
                    continue
                obj_class = pixel_to_class.get(pixel)
                mask = mask_np == pixel
                ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
                for i in range(1, ret):
                    obj_mask = curr_mask == i
                    curr_bitmap = sly.Bitmap(obj_mask)
                    if curr_bitmap.area > 30:
                        curr_label = sly.Label(curr_bitmap, obj_class)
                        labels.append(curr_label)

            ann_data = image_name_to_ann_data.get(image_name.replace("_old_", "_"))
            if ann_data is None:
                ann_data = image_name_to_ann_data.get(image_name)
            for curr_ann_data in ann_data:
                category_id = curr_ann_data["category_id"]
                obj_class = idx_to_obj_class[category_id]
                supercategory_value = id_to_supercategory.get(category_id)
                supercategory = sly.Tag(supercategory_meta, value=supercategory_value)

                bbox_coord = curr_ann_data["bbox"]
                rectangle = sly.Rectangle(
                    top=int(bbox_coord[1]),
                    left=int(bbox_coord[0]),
                    bottom=int(bbox_coord[1] + bbox_coord[3]),
                    right=int(bbox_coord[0] + bbox_coord[2]),
                )
                label_rectangle = sly.Label(rectangle, obj_class, tags=[supercategory])
                labels.append(label_rectangle)

            tags_data = image_name_to_tags[image_name]
            scene_type_value = tags_data["scene_type"]
            if scene_type_value is not None:
                scene_type = sly.Tag(scene_type_meta, value=scene_type_value)
                tags.append(scene_type)
            lighting_value = tags_data["lighting"]
            if lighting_value is not None:
                lighting = sly.Tag(lighting_meta, value=lighting_value)
                tags.append(lighting)
            reflections_value = tags_data["reflections"]
            if reflections_value is not None:
                reflections = sly.Tag(reflections_meta, value=reflections_value)
                tags.append(reflections)
            waves_value = tags_data["waves"]
            if waves_value is not None:
                waves = sly.Tag(waves_meta, value=waves_value)
                tags.append(waves)

            extra_dark_value = tags_data["special"]["extra_dark"]
            if extra_dark_value is True:
                extra_dark = sly.Tag(extra_dark_meta)
                tags.append(extra_dark)

            extra_bright_value = tags_data["special"]["extra_bright"]
            if extra_bright_value is True:
                extra_bright = sly.Tag(extra_bright_meta)
                tags.append(extra_bright)

            glitter_value = tags_data["special"]["glitter"]
            if glitter_value is True:
                glitter = sly.Tag(glitter_meta)
                tags.append(glitter)

            dirty_lens_value = tags_data["special"]["dirty_lens"]
            if dirty_lens_value is True:
                dirty_lens = sly.Tag(dirty_lens_meta)
                tags.append(dirty_lens)

            wakes_value = tags_data["special"]["wakes"]
            if wakes_value is True:
                wakes = sly.Tag(wakes_meta)
                tags.append(wakes)

            rain_value = tags_data["special"]["rain"]
            if rain_value is True:
                rain = sly.Tag(rain_meta)
                tags.append(rain)

            fog_value = tags_data["special"]["fog"]
            if fog_value is True:
                fog = sly.Tag(fog_meta)
                tags.append(fog)

            plants_debris_value = tags_data["special"]["plants_debris"]
            if plants_debris_value is True:
                plants_debris = sly.Tag(plants_debris_meta)
                tags.append(plants_debris)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    seq_name_meta = sly.TagMeta("seq name", sly.TagValueType.ANY_STRING)
    seq_id_meta = sly.TagMeta("seq id", sly.TagValueType.ANY_STRING)

    supercategory_meta = sly.TagMeta("supercategory", sly.TagValueType.ANY_STRING)
    scene_type_meta = sly.TagMeta("scene type", sly.TagValueType.ANY_STRING)
    lighting_meta = sly.TagMeta("lighting", sly.TagValueType.ANY_STRING)
    reflections_meta = sly.TagMeta("reflections", sly.TagValueType.ANY_STRING)
    waves_meta = sly.TagMeta("waves", sly.TagValueType.ANY_STRING)
    extra_dark_meta = sly.TagMeta("extra dark", sly.TagValueType.NONE)
    extra_bright_meta = sly.TagMeta("extra bright", sly.TagValueType.NONE)
    glitter_meta = sly.TagMeta("glitter", sly.TagValueType.NONE)
    dirty_lens_meta = sly.TagMeta("dirty lens", sly.TagValueType.NONE)
    wakes_meta = sly.TagMeta("wakes", sly.TagValueType.NONE)
    rain_meta = sly.TagMeta("rain", sly.TagValueType.NONE)
    fog_meta = sly.TagMeta("fog", sly.TagValueType.NONE)
    plants_debris_meta = sly.TagMeta("plants debris", sly.TagValueType.NONE)

    id_to_supercategory = {
        1: "obstacle",
        3: "water",
        5: "sky",
        11: "obstacle",
        12: "obstacle",
        13: "obstacle",
        14: "obstacle",
        15: "obstacle",
        16: "obstacle",
        17: "obstacle",
        19: "obstacle",
    }

    water = sly.ObjClass("water", sly.AnyGeometry, color=(41, 167, 224))
    sky = sly.ObjClass("sky", sly.AnyGeometry, color=(90, 75, 164))
    obstacle = sly.ObjClass("obstacle", sly.AnyGeometry, color=(247, 195, 37))

    idx_to_obj_class = {
        1: sly.ObjClass("static obstacle", sly.Rectangle, color=(230, 25, 75)),
        3: water,
        5: sky,
        11: sly.ObjClass("boat/ship", sly.Rectangle, color=(60, 180, 75)),
        12: sly.ObjClass("row boats", sly.Rectangle, color=(255, 225, 25)),
        13: sly.ObjClass("paddle board", sly.Rectangle, color=(0, 130, 200)),
        14: sly.ObjClass("buoy", sly.Rectangle, color=(245, 130, 48)),
        15: sly.ObjClass("swimmer", sly.Rectangle, color=(145, 30, 180)),
        16: sly.ObjClass("animal", sly.Rectangle, color=(70, 240, 240)),
        17: sly.ObjClass("float", sly.Rectangle, color=(240, 50, 230)),
        19: sly.ObjClass("other", sly.Rectangle, color=(210, 245, 60)),
    }

    pixel_to_class = {
        0: obstacle,
        1: water,
        2: sky,
    }

    obj_classes = [obstacle] + list(idx_to_obj_class.values())

    meta = sly.ProjectMeta(
        obj_classes=obj_classes,
        tag_metas=[
            seq_name_meta,
            seq_id_meta,
            supercategory_meta,
            scene_type_meta,
            lighting_meta,
            reflections_meta,
            waves_meta,
            extra_dark_meta,
            extra_bright_meta,
            glitter_meta,
            dirty_lens_meta,
            rain_meta,
            fog_meta,
            plants_debris_meta,
            wakes_meta,
        ],
    )

    api.project.update_meta(project.id, meta.to_json())

    for ds_name, ds_data in ds_name_to_split.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        images_path, anns_path = ds_data

        if anns_path is not None:
            bboxes_path = os.path.join(anns_path, bboxes_file_name)
            tags_path = os.path.join(anns_path, tags_file_name)
            masks_path = os.path.join(anns_path, masks_folder)

            image_name_to_ann_data = {}
            # image_name_to_shape = {}

            ann = load_json_file(bboxes_path)

            # for curr_image_info in ann["images"]:
            #     image_name_to_shape[curr_image_info["file_name"]] = (
            #         curr_image_info["height"],
            #         curr_image_info["width"],
            #     )

            for curr_ann_data in ann["annotations"]:
                image_id = curr_ann_data["image_id"]
                image_name_to_ann_data[get_file_name(curr_ann_data["file_name"])] = curr_ann_data[
                    "segments_info"
                ]

            image_name_to_tags = {}
            ann_tags = load_json_file(tags_path)["annotations"]
            for curr_ann_tag in ann_tags:
                image_name_to_tags[get_file_name(curr_ann_tag["file_name"])] = curr_ann_tag[
                    "labels"
                ]

        images_names = os.listdir(images_path)

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for images_names_batch in sly.batched(images_names, batch_size=batch_size):
            img_pathes_batch = [
                os.path.join(images_path, image_name) for image_name in images_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))

    return project
