## Motivation

The authors present the first maritime panoptic obstacle detection benchmark **LaRS: Lakes Rivers and Seas dataset** , featuring scenes from lakes, rivers and seas. The progress in maritime obstacle detection is hindered by the lack of a diverse dataset that adequately captures the complexity of general maritime environments. Today over 90% of goods being moved over water, substantial efforts are being invested in development of autonomous unmanned surface vessels(USV). The autonomy of USVs critically depends on obstacle detection capability for timely collision avoidance. There are several challenges associated with maritime obstacle detection. The appearance of the navigable surface (water) is dynamic and reflects the environment, often
containing strong mirroring and sun glitter.

<img src="https://github.com/dataset-ninja/lars/assets/120389559/f8432129-a491-4caa-85d7-138a68e2cf2d" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">LaRS features diverse and challenging USV-centric scenes with per-pixel panoptic annotations (right).</span>

Although modern detectors can accurately detect common dynamic obstacles such as ships and boats, the appearance of obstacles such as buoys, people and animals
can vary significantly, bringing the task closer to anomaly detection. Furthermore, background static obstacles, such as shorelines and piers, cannot be addressed by these methods. The currently dominant approach instead employs semantic segmentation to decompose the scene into three semantic classes (water, obstacles and sky), which jointly address static and dynamic obstacles. The recent detection benchmark indicates that segmentation methods could benefit from the detection approach. A natural approach that combines these two principles is panoptic segmentation, which has proven highly effective in the related field of autonomous ground vehicles. Unfortunately, panoptic segmentation has not been fully explored for maritime perception, primarily due to the lack of a diverse, publicly available, curated panoptic dataset.

## Dataset creation and description

The authors proposes the first maritime panoptic obstacle detection benchmark. LaRS surpasses existing datasets in terms of diversity, obstacle types and acquisition conditions. The dataset is composed of over 4000 key frames with panoptic labels for 3 stuff and 8 thing categories, and 19 global scene attributes. Each key frame is equipped with the preceding nine frames to facilitate the development of methods that exploit temporal texture. To ensure equal attribute distribution, the training, validation, and test splits were carefully constructed.

A wide range of sources was considered to ensure the visual diversity of LaRS. Specifically, the authors collected scenes from public online videos featuring various activities captured from boats around the world, recorded new sequences in a number of different geographic locations ourselves and included the most challenging scenes from existing maritime datasets. The collection of public videos was guided using search prompts related to underrepresented scenes in the existing datasets. This includes canals (e.g. ”canal tour”), exotic locations (e.g. ”tropic boat tour”, ”polar kayaking”), crowded scenes (e.g. ”boat parade”), strong reflections (e.g. ”still lake”), and poor visibility conditions (e.g. ”boat ride in the rain”, ”night-time boat ride”). At least one key frame was extracted from each of the collected 396 sequences, to ensure visual diversity. The authors manually inspected the predicted segmentation and included examples with failures such as false negative obstacle segmentation and false positives on reflections to increase the difficulty level. In this way, a set of 897 representative key frames spanning diverse and challenging scenes was selected. Next, they manually recorded videos at various locations on lakes, rivers and seas. From these, they identified 494 challenging sequences, and using the same process as for online videos, the authors identified 1354 diverse and challenging key frames. The total number of images in LaRS is thus over 40k. Faces were de-identified in all frames by running a face detector and blurring, followed by manual inspection.

<img src="https://github.com/dataset-ninja/lars/assets/120389559/3b59aa9c-ad9e-4457-9d23-f958ef4aeeaa" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;"> LaRS data sources with number of the sourced sequences, the number of selected frames and their percentage
in the final dataset.</span>

## Dataset annotation

All 4k selected key frames were manually annotated with per-pixel panoptic labels by a professional labeling company. In particular, _water_, _sky_ and
_static obstacles_ like shores and piers were annotated as stuff classes, while the dynamic obstacles instances were segmented and classified into 8 different object categories: _boat_, _row boat_, _paddle board_, _buoy_, _swimmer_, _animal_, _float_ and an open-world _other_ class to cover the remaining obstacles. Following a standard practice group labels were used to group multiple hard-to-delineate neighbouring instances of the same category. Regions that could not be reliably manually segmented were labeled with the ignore class.

<img src="https://github.com/dataset-ninja/lars/assets/120389559/7755b0cd-e318-47e6-8e5a-204de7d2e647" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;"> :LaRS frames are labeled with 19 global attributes relevant for navigation. Mutually exclusive and mutually nonexclusive groups are indicated in blue and green, respectively. The numbers indicate the amount of frames in the dataset.</span>

<img src="https://github.com/dataset-ninja/lars/assets/120389559/81d37ec8-bd77-4f01-a0e4-6333e339237e" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Statistics of dynamic obstacle classes in LaRS (left) with respect to their size (right)..</span>

Global attributes were assigned to key frames, to indicate environment type, illumination conditions, presence of reflections, surface roughness and scene conditions: _scene type_, _lighting_, _reflections_, _waves_, _extra dark_, _extra bright_, _glitter_, _dirty lens_, _wakes_, _rain_, _fog_, _plants debris_ images tags.

Annotation correctness was further analyzed to ensure the highest quality of the dataset. In the first pass, state-ofthe-art semantic segmentation and panoptic segmentatation methods were trained and run on the entire dataset to identify major annotation errors. The authors manually inspected all ground truth instance labels of the dynamic obstacles and identified and corrected approximately 3600 annotation errors.
