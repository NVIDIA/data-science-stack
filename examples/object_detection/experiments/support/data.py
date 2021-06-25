import os
import shutil
from typing import Any, Dict
from urllib.parse import urlparse
from urllib.request import urlretrieve

import numpy as np
import torch
from torchvision.transforms import Compose, ToTensor
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from PIL import Image

def download_data(download_directory: str, data_config: Dict[str, Any]) -> str:
    if not os.path.exists(download_directory):
        os.makedirs(download_directory, exist_ok=True)
    url = data_config["url"]
    filename = os.path.basename(urlparse(url).path)
    filepath = os.path.join(download_directory, filename)
    if not os.path.exists(filepath):
        urlretrieve(url, filename=filepath)
        shutil.unpack_archive(filepath, download_directory)


def collate_fn(batch):
    return tuple(zip(*batch))


def get_transform():
    transforms = []
    transforms.append(ToTensor())
    return Compose(transforms)


def load_and_transform_image(img_path):
    image = Image.open(img_path).convert("RGB")
    image = get_transform()(image)
    return image


def draw_example(image, labels, title=None):
    fig,ax = plt.subplots(1)
    plt.title(title)
    ax.imshow(image)
    boxes = labels['boxes'].numpy()
    boxes = np.vsplit(boxes, boxes.shape[0])
    for box in boxes:
        box = np.squeeze(box)
        bottom, left = box[0], box[1]
        width = box[2] - box[0]
        height = box[3] - box[1]
        rect = patches.Rectangle((bottom,left),width,height,linewidth=2,edgecolor='r',facecolor='none')
        # # Add the patch to the Axes
        ax.add_patch(rect)
    plt.axis('off')
    plt.show()


# Custom dataset for PennFudan based on:
# https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html
class PennFudanDataset(object):
    def __init__(self, root, transforms, device=None):
        self.root = root
        self.transforms = transforms
        # load all image files, sorting them to
        # ensure that they are aligned
        self.imgs = sorted(os.listdir(os.path.join(root, "PNGImages")))
        self.masks = sorted(os.listdir(os.path.join(root, "PedMasks")))
        self.device = device

    def __getitem__(self, idx):
        # load images ad masks
        img_path = os.path.join(self.root, "PNGImages", self.imgs[idx])
        mask_path = os.path.join(self.root, "PedMasks", self.masks[idx])
        img = Image.open(img_path).convert("RGB")
        # note that we haven't converted the mask to RGB,
        # because each color corresponds to a different instance
        # with 0 being background
        mask = Image.open(mask_path)

        mask = np.array(mask)
        # instances are encoded as different colors
        obj_ids = np.unique(mask)
        # first id is the background, so remove it
        obj_ids = obj_ids[1:]

        # split the color-encoded mask into a set of binary masks
        masks = mask == obj_ids[:, np.newaxis, np.newaxis]

        # get bounding box coordinates for each mask
        num_objs = len(obj_ids)
        boxes = []
        for i in range(num_objs):
            pos = np.where(masks[i])
            xmin = np.min(pos[1])
            xmax = np.max(pos[1])
            ymin = np.min(pos[0])
            ymax = np.max(pos[0])
            boxes.append([xmin, ymin, xmax, ymax])

        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        # there is only one class
        labels = torch.ones((num_objs,), dtype=torch.int64)
        masks = torch.as_tensor(masks, dtype=torch.uint8).to(self.device)

        image_id = torch.tensor([idx]).to(self.device)
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        # suppose all instances are not crowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64).to(self.device)


        if self.transforms is not None:
            img = self.transforms(img)

        if self.device:
            boxes = boxes.to(self.device)
            labels = labels.to(self.device)
            masks = masks.to(self.device)
            image_id = image_id.to(self.device)
            iscrowd = iscrowd.to(self.device)
            img = img.to(self.device)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["masks"] = masks
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        return img.to(self.device), target

    def __len__(self):
        return len(self.imgs)
