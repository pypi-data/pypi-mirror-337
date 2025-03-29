# Tensorscope
Tensorscope is an extension of the [fvcore](https://github.com/facebookresearch/fvcore) library created by Facebook that provides additional model analysis. Tensorscope adds the ability to count the number of bytes that are read and written by each operation. Additionally, a function is provided that outputs the limiting factor for each operation in your model, whether that is Arithmetic Intensity or GPU ops:bytes. This can be useful when attempting to optimize your model and identify bottlenecks.

## Features
* Analysis of the number of elements read or written in each operation of a model
* Analysis of the number of bytes read or written in each operation of a model
* Calculation of the arithmetic intensity of each operation
* Calculation of a GPU's ops:bytes ratio
* Support for various precisions and GPUs
* Support for various model types and architectures
* Estimation of the forward pass time for the given model, data, precision, and GPU

## Installation
```
pip install tensorscope
```

## Element Counting
Tensorscope contains a class called ElemCountAnalysis that counts the number of elements read and written in each operation of a model. Combining this information with knowing what precision the operation is executed in provides the number of bytes read and written for each operation. See the fvcore documentation for more information on how it works and ways to extend it or add support for more operations.
```
import torch
from torchvision.models import resnet18
from tensorscope import ElemCountAnalysis

model = resnet18()
inputs = (torch.randn(32, 3, 224, 224))

elems = ElemCountAnalysis(model, inputs)
print(elems.total)
print(elems.by_module())
print(elems.by_module_and_operator())
```

## Analyzing Operation Limitations (Byte + FLOP counting)
As described in NVIDIA's [GPU Performance Background](https://docs.nvidia.com/deeplearning/performance/pdf/GPU-Performance-Background-User-Guide.pdf) documentation, comparing an algorithm's arithmetic intensity with a GPU's ops:bytes ratio can identify whether an operation is limited by algorithm efficiency or GPU bandwidths. Using the `analysis_model` function will output a table containing this information.
```
from torchvision.models import resnet18
from tensorscope import analyze_model

batch_size = 512
model = resnet18()
input_shape = [(batch_size, 3, 224, 224)]
gpu = 'NVIDIA GeForce GTX 1650 Ti'
precision = 'fp32'

analyze_model(model, input_shape, gpu, precision)
```

## Forward Pass Time Estimation
The `analysis_model` function provides an estimate on the time required for the forward pass. This is based on the time needed for the limiatior in each operation to completed, summed across all operations. Currently this estimate is not very accurate and I would like to improve this in the future.

## GPU Specifications
When passing the GPU name to the `analysis_model` function, there must be the corresponding information located in the `gpu_specs.json` file. If it does not already exist in there, it can easily be added by following the template provided in the file. The name of the GPU corresponds to the returned value from `torch.cuda.get_device_name()`.
