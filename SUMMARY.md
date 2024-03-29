**LaRS: Lakes Rivers and Seas dataset** is a dataset for instance segmentation, semantic segmentation, and object detection tasks. It is used in the marine industry. 

The dataset consists of 53301 images with 41852 labeled objects belonging to 12 different classes including *water*, *obstacle*, *static obstacle*, and other: *sky*, *boat/ship*, *buoy*, *row boats*, *other*, *swimmer*, *paddle board*, *animal*, and *float*.

Images in the LaRS dataset have pixel-level instance segmentation and bounding box annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation task (only one mask for every class). There are 50498 (95% of the total) unlabeled images (i.e. without annotations). There are 3 splits in the dataset: *train* (32375 images), *test* (17966 images), and *val* (2960 images). Additionally, the images have ***seq name*** and ***seq id*** tags, that help associate every image with a parent sequence. Each of 8 dynamic obstacle labels has ***supercategory*** tag. The dataset was released in 2023 by the <span style="font-weight: 600; color: grey; border-bottom: 1px dashed #d3d3d3;">University of Ljubljana, Slovenia</span>.

<img src="https://github.com/dataset-ninja/lars/raw/main/visualizations/poster.png">
