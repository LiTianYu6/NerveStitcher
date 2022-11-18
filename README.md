<img src=data/lab_logo2.png width="35%" height="15%">

# NerveStitcher: Corneal Confocal Microscope Images Stitching with Neural Networks

## Introduction

NerveStitcher is a deep learning based corneal confocal microscopic image stitching tool. The tool integrates the functions of microscope vignetting correction and image stitching, and can process corneal nerve images in a pipeline. Input sequential images (without pre-defined acquisition sequences) and output vignetting corrected images and stitching results. 

It has extremely high efficiency and accuracy, in our preliminary experiments: NVIDIA GeForce GTX1060 6G stitching time is about 0.331 seconds (per image pair) under GPU hardware acceleration. i5-4460 3.2GHz stitching time is about 0.945 seconds (per image pair) under CPU hardware acceleration.

NerveStitcher was developed by *Tianyu Li* of TGU-UOW Lab on the basis of [SuperGlue](https://github.com/magicleap/SuperGluePretrainedNetwork).

For more information, please read：<br>
NerveStitcher：
``
Li G, Li T, Li F, et al. NerveStitcher: Corneal confocal microscope images stitching with neural networks[J]. Computers in Biology and Medicine, 2022: 106303.
https://doi.org/10.1016/j.compbiomed.2022.106303
``<br><br>
Vignetting correction：
``
LI Tianyu,LI Guangxu,ZHANG Chen,et al.Adaptive vignetting correction of corneal nerve microscopy images[J].Optics and Precision Engineering,2022,30(20):2479-2488. DOI： 10.37188/OPE.20223020.2479.
``

Official Website: **[TGU-UOW 2022](https://www.tgu-uow.com)**

## Usage
Before running, you need to download the model file and replace it in **models/weights**, here is the link to download the weights: https://drive.google.com/drive/folders/1SgHwGcFwKbV6Bv7OgV1PbqCWmSJgx3jZ?usp=sharing

Note before use that the default image size is 384×384, use English file names and sort well (e.g. zhOD0001.jpg zhOD0002.jpg ...). <br>
NerveStitcher is compatible with **.jpg**  **.png** **.tiff** format images. <br>
We provide files to modify the file name and format, please refer to **img_rename.py**

Make sure that only numbers are sorted when sorting. As in line 14 of **make\_img\_list.py**, the current sort is zhOD0001.jpg with the number 0001 (sorted from the fourth positive character to the middle of the fourth negative character), you can modify this sorting rule to match the name of your image. The same code also appears in **correction.py** line 191. <br>
### vignetting correction
Please refer to **correction.py** , and modify the **path** and **savepath** parameters before use.

There are two methods of vignetting correction: <br>
1. Adaptive correction (**not recommended**)<br>
This method will automatically calculate the vignetting parameters for each image, but it is slow and ineffective. If you want to use this method please uncomment line 163 and add comment line 164.<br>
2. Automatic correction<br>
This method uses fixed vignetting parameters, which have been verified by our tests to ensure the accuracy of the correction. First, refer to *data/reference.jpg* to specify the histogram of the original image, and then correct it according to the preset vignetting parameters (line 164).
### image stitching
Please refer to **stitching.py** , modify **input\_dir** (the address of the image data to be stitched), **input\_pairs\_path** (the address of the list of images to be stitched), **output\_viz\_dir** (the address where the final result is saved), **force\_cpu** (whether to force the CPU or GPU) before using.<br>
The folder structure is based on the example file **data/test/stitch\_img OR stitch\_img2**, where the "match" folder holds the final stitching results and the "result" folder holds the results of each stitching.

## Contact Us
NerveStitcher can also be used to stitch other microscopy images. Some of the images we have successfully tested are: fundus vascular and thickness OCT images, fundus vascular images.

For additional questions or discussions, Please contact email:

liguangxu@tiangong.edu.cn

litianyu@tiangong.edu.cn

## BibTeX Citation
If you use any ideas from the paper or code from this repo, please consider citing:

```txt
@article{li2022nervestitcher,
  title={NerveStitcher: Corneal confocal microscope images stitching with neural networks},
  author={Li, Guangxu and Li, Tianyu and Li, Fangting and Zhang, Chen},
  journal={Computers in Biology and Medicine},
  pages={106303},
  year={2022},
  publisher={Elsevier}
}
```


## Copyright
Do not use for commercial purposes without permission. <br>
Copyright (c) 2022 TGU-UOW
