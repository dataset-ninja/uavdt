Dataset **UAVDT** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzM2MzdfVUFWRFQvdWF2ZHQtRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAiaDAxMEFOYjBMUDBVekkxM05jTkpxVi81VWFTbUFtQ3FUNzdDSnhnOFY5bz0ifQ==)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='UAVDT', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be downloaded here:

- [UAVDT-Benchmark-M](https://drive.google.com/file/d/1m8KA6oPIRK_Iwt9TYFquC87vBc_8wRVc/view?usp=sharing)
- [DET/MOT toolkit](https://drive.google.com/open?id=19498uJd7T9w4quwnQEy62nibt3uyT9pq)
- [Attributes](https://drive.google.com/open?id=1qjipvuk3XE3qU3udluQRRcYuiKzhMXB1)
- [UAVDT-Benchmark-S](https://drive.google.com/open?id=1661_Z_zL1HxInbsA2Mll9al-Ax6Py1rG)
- [SOT toolkit](https://drive.google.com/open?id=1YMFTBatK6qUrtnIe4fZNMZ9FpCpD2cxm)
