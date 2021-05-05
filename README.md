# BRTSRD
## Overview
Source code and dataset of paper "Construction of Brazilian Regulatory Traffic Sign Recognition Dataset" presented and published at CIARP 25 (Porto, Portugal - 2021)

## Dataset
Brazilian Regulatory Traffic Sign Recognition Dataset (BRTSRD) is a dataset of more than 24,000 regulation traffic sign images in 51 classes of regulatory traffic signs. The structure being considered for the proposed dataset follows the standard used by the CIFAR10 dataset. Each image has a resolution of 32 x 32 pixels with three color channels.

## Model

The architecture used in this document was based on the version of LeNet. The CNN was developed using three convolutional sets arranged as follows: one convolutional layer, each with a batch normalization layer, an activation layer, and a max pooling layer. After the convolutional block, one fully connected layer does the classification work.

## Libraries and More

For this work we use the [TensorFlow][tf] library and the [Google Colab][gc] development environment.

## Metrics

The model presented reached a maximum accuracy of 99.31% in the training set. The accuracy achieved was 93.73% in the validation set. The best loss values obtained were 0.3737 during training and 0.5574 for the validation set.

| Metric | Training | Validation | Testing |
| ------ | ------ | ------ | ------ |
|Accuracy | 99.31% | 93.73% | 91.41% |
|Precision |  99.52% | 96.37% | 91.55% |
|Recall |  99.02% | 92.45% | 89.28% |
|F1-Score |  99.27% | 94.34% | 99.27% |

   [tf]: <https://www.tensorflow.org/>
   [gc]: <https://colab.research.google.com/>
