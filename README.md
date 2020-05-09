# DamageDetection
code to train and predict damages.

Convert Annotations to be able to train in pascal_voc format. 
python3 get_annotations.py dataset/train/train_multiclass.json dataset/train output
python3 get_annotations.py dataset/val/val_multiclass.json dataset/val output

The dataset created for bounding box prediction using pascal_voc format is located at 
maskrcnn-benchmark/datasets/voc/VOC2007/damage

A faster-rcnn based model with resnet-50 as backbone is used to predict boxes. 

The training is done using maskrcnn-benchmark librabry which has different configurations to train different models.

For training the configuration which was used is present in the location maskrcnn-benchmark/config.yml

python3 tools/train_net.py --config-file=config.yml

I have trained the model for 10k iterations on google colab and found that the model with 4k iterations gave better
mAP: 0.6645
rear_bumper     : 0.3909
front_bumper    : 0.8377
headlamp        : 0.5303
door            : 0.6545
hood            : 0.9091

The code to predict is maskrcnn-benchmark/demo/test.py 

python3 demo/test.py --config-file=config.yml --min-image-size=800.

I have used the same model to predict on the test set of images which were given. 
The output of the test images are at test/output*


