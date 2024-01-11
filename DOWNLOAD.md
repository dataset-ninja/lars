Dataset **LaRS** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://www.dropbox.com/scl/fi/1296b8jhvsqgx3wk098d9/lars-DatasetNinja.tar?rlkey=9xsxca5vfdlqk7aso9he8yvxx&dl=1)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='LaRS', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be downloaded here:

- [Sequence images](https://box.vicos.si/lars/lars_v1.0.0_images_seq.zip)
- [Annotations](https://box.vicos.si/lars/lars_v1.0.0_annotations.zip)
- [Single-frame images](https://box.vicos.si/lars/lars_v1.0.0_images.zip)
