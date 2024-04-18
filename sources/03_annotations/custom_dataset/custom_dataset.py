# coding=utf-8
"""
@credit
@article{Jaume2019FUNSDAD,
  title={FUNSD: A Dataset for Form Understanding in Noisy Scanned Documents},
  author={Guillaume Jaume and H. K. Ekenel and J. Thiran},
  journal={2019 International Conference on Document Analysis and Recognition Workshops (ICDARW)},
  year={2019},
  volume={2},
  pages={1-6}
}
"""
import json
import os

from PIL import Image, ImageFile
#ImageFile.LOAD_TRUNCATED_IMAGES = True

import datasets

def load_image(image_path):
  try:
    with Image.open(image_path).convert("RGB") as image:
        w, h = image.size
    return image, (w, h)
  except:
   print(image_path)


def normalize_bbox(bbox, size):
  return [
        int(1000 * bbox[0] / size[0]),
        int(1000 * bbox[1] / size[1]),
        int(1000 * bbox[2] / size[0]),
        int(1000 * bbox[3] / size[1]),
    ]

logger = datasets.logging.get_logger(__name__)


_CITATION = """\
Bureau d'études
"""

_DESCRIPTION = """\
Maybe later :)
"""


class DFConfig(datasets.BuilderConfig):
    """BuilderConfig for FUNSD"""

    def __init__(self, **kwargs):
        """BuilderConfig for FUNSD.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(DFConfig, self).__init__(**kwargs)


class CustomDataset(datasets.GeneratorBasedBuilder):
    """Conll2003 dataset."""

    BUILDER_CONFIGS = [
        DFConfig(name="custom_dataset", version=datasets.Version("1.0.0"), description="Bank Statement extraction dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "bboxes": datasets.Sequence(datasets.Sequence(datasets.Value("int64"))),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=["O","S-date","B-libelle","I-libelle","O-libelle", "S-debit", "S-credit"]
                        )
                    ),
                    "image": datasets.features.Image(),
                    "image_path": datasets.Value("string")
                } 
            ),
            supervised_keys=None,
            homepage="",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # downloaded_file = dl_manager.download_and_extract("https://guillaumejaume.github.io/FUNSD/dataset.zip")
        dataset_path = '/content/sample_data/'
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": f"{dataset_path}/annotated_data/train/"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepath": f"{dataset_path}/annotated_data/test/"}
            ),
        ]

    # def get_line_bbox(self, bboxs):
    #     x = [bboxs[i][j] for i in range(len(bboxs)) for j in range(0, len(bboxs[i]), 2)]
    #     y = [bboxs[i][j] for i in range(len(bboxs)) for j in range(1, len(bboxs[i]), 2)]

    #     x0, y0, x1, y1 = min(x), min(y), max(x), max(y)

    #     assert x1 >= x0 and y1 >= y0
    #     bbox = [[x0, y0, x1, y1] for _ in range(len(bboxs))]
    #     return bbox

    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)
        ann_dir = os.path.join(filepath, "annotations")
        img_dir = os.path.join(filepath, "images")


        for guid, file in enumerate(sorted(os.listdir(ann_dir))):
            tokens = []
            bboxes = []
            ner_tags = []
            file_path = os.path.join(ann_dir, file)
            with open(file_path, "r", encoding="utf8") as f:
                data = json.load(f)
            image_path = os.path.join(img_dir, file)
            image_path = image_path.replace("json", "png")
            image, size = load_image(image_path)
            
            tokens = [str(token) for token in data['tokens']]
            bboxes = [normalize_bbox(bbox, size) for bbox in data['bboxes']]
            bboxes = [
              [
                int(bbox[0]), 
                int(bbox[1]), 
                int(bbox[2]), 
                int(bbox[3])
              ] for bbox in bboxes]
              
            ner_tags = ['O' if tag=='B-other' else tag for tag in data['ner_tags']] # replace 'B-other' by 'O'
            
            assert 'B-other' not in ner_tags
            
            yield guid, {"id": str(guid), "tokens": tokens, "bboxes": bboxes, "ner_tags": ner_tags,
                         "image": image, 'image_path': image_path}