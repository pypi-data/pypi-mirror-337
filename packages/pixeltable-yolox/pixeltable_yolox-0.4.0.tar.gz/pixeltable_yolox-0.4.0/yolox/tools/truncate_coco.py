import json
import os
from typing import Callable, Union


def truncate_coco(coco_file: Union[str, os.PathLike], condition: Callable[[int], bool], output_file: Union[str, os.PathLike]) -> None:
    with open(coco_file, "r") as fp:
        data = json.load(fp)

    data["images"] = [img for img in data["images"] if condition(img["id"])]
    data["annotations"] = [ann for ann in data["annotations"] if condition(ann["image_id"])]
    print(f'{len(data["images"])} images, {len(data["annotations"])} annotations.')

    with open(output_file, "w", encoding="utf8") as fp:
        json.dump(data, fp)
