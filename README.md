## Nucon Image classification

I have attempted Task 1 of the nucon.io programming assignment. This README documents my approach to this task!

### Part 1: Training a CNN model using Keras

Considering the limited size of our dataset, I chose to approach this by finetuning the VGG16 pre-trained model for our classification task instead of building a model from scratch. After going through several iterations of tweaking with the model architecture, batch sizes, and data augmentation techniques, the model achieved a val_acc of 0.76. The code used for settting up and training the model is in 'trainModel.py'.

I selected 11 classes for this model - some were selected for their (relatively) large number of samples (eg. window, door, pipe), whereas others were chosen because they appeared to have distinct features and shapes (at least from a human pov), and I was interested in discovering whether these features would make easier for the model to distinguish them (eg. fire alarm, aircon vent, cctv).

Running the final model ('weights.05-0.83-0.76.h5') on several test cases, I found that the classes with larger datasets were classified with much better accuracy, compared to those with fewer training images. Due to the significant inbalance in the training data available for each class, the model was presumably trained to favour classes with more samples since it was designed to maximise the number of correct predictions.

Given more data and better processing capacity, the model could be trained to attain a better fit. There were also several instances in which a photo could be categorised into more than one class. For example, many 'ceiling' photos also featured 'cctv' and 'aircon vent'. With more training images, we can avoid using data augmentation as lateral translations and zooming could be causing the model to wrongly identify the main feature of each photo.

![Augmentation](augmentation.png?raw=true "Augmentation")

### Part 2: Deploying the trained model using APIs in Flask

The API endpoint '/predict' takes an image as input ('image'). Returns the classfication label and probability computed by the model .

Example request:
```
curl -X POST -F image=@michael238.jpg 'http://localhost:5000/predict'
```
Example output:
```
{
  "predictions": [
    {
      "label": "door", 
      "probability": 1.0
    }
  ], 
  "success": true
}
```



### Built With

* [Keras.io](https://keras.io/) 
* [Enthought Canopy](https://www.enthought.com/product/canopy) 
* [Flask](http://flask.pocoo.org/) 


### Version Control

*Version 1.0.0* - 08 Jan 2018
Original




### Acknowledgments

@misc{chollet2015keras,
  title={Keras},
  author={Chollet, Fran\c{c}ois and others},
  year={2015},
  howpublished={\url{https://keras.io}},
}

@article{He2015,
	author = {Kaiming He and Xiangyu Zhang and Shaoqing Ren and Jian Sun},
	title = {Deep Residual Learning for Image Recognition},
	journal = {arXiv preprint arXiv:1512.03385},
	year = {2015}
}

@Article{Simonyan14c,
 author = {Simonyan, K. and Zisserman, A.},
 title = {Very Deep Convolutional Networks for Large-Scale Image Recognition},
 journal = {CoRR},
 volume  = {abs/1409.1556},
 year    = {2014}
}
