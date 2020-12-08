## Notebook Details

#### dataset_creation_bounding_box.ipynb
<pre> • Download datasets from kaggle medical mask (3 datasets)
 • Generate dataframe(person) on top of medical mask dataset using detectron2 baseline model
 • upload the dataframe(person) on drive
</pre>

#### covid_detectron.ipynb
<pre> • Download datasets from kaggle medical mask (3 datasets)
 • Generate dataframe(mask) from above dataset
 • Merge dataframe(mask) & dataframe(person)
 • upload the dataframe(merged) on drive
 • train detectron 2 model on dataset
 • save final model on drive
</pre> 

#### covid_deployment_notebook.ipynb
<pre> • Download model(mask + person) from drive
 • generate pipeline for model execution
 • Test pipeline on videos
</pre>
  
#### facemask_using_mobilenet.ipynb
<pre> • Download datasets from kaggle and https://github.com/chandrikadeb7/Face-Mask-Detection.git
 • Generate labelled dateset by cropping images using bbox present in annotation.
 • Dataset contains images of faces only
 • Train MobileNetV2 model using transfer learning
 • Prediction - 2 Stages
	○ Detect face using res10_300x300_ssd_iter_140000 model
   	○ On faces apply our facemask detection model
</pre>
