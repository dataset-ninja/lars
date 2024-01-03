## Motivation

The progress in maritime obstacle detection is hindered by the lack of a diverse dataset that adequately captures the complexity of general maritime environments. **LaRS: A Diverse Panoptic Maritime Obstacle Detection Dataset and Benchmark** was created as a benchmark for panoptic maritime obstacle detection, to facilitate the development and evaluation of new panoptic (and semantic) segmentation methods for robust obstacle detection under a wide range of conditions and situations. Dataset featuring scenes from lakes, rivers and seas.

## Dataset composition

Instances in the dataset are snippets (i.e. scenes) of 10 sequential video frames (photos) depicting maritime scenarios captured with a wide range of different consumer-grade and industry-grade RGB cameras. The instance were extracted from a larger set of videos. The videos were manually selected to feature diverse scenarios and geographic locations. At least one instance was extracted from each video to ensure visual diversity. One ”key” video frame in the snippet was annotated with masks. The annotations were created by human annotators and verified by authors. LaRS is composed of over 4000 per-pixel labeled key frames with 9 preceding frames to allow exploiting temporal texture, amounting to over 40k frames. Each key frame is annotated with 11 thing and stuff classes and 12 global scene attributes.

## Dataset tasks

The dataset was intended for training and evaluation of semantic and panoptic segmentation methods. However, with minimal effort the dataset could also be used for other task such as instance segmentation and object detection.
