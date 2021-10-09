#!/usr/bin/env python

import os
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg19 import preprocess_input
from keras.applications.vgg19 import decode_predictions


# See if the model is available
model_exists = [c for c in os.listdir('./weights/') if c != '.gitkeep']

if not model_exists:
    print('\n ---- Loading model from tensorflow ----')
    model = tf.keras.applications.vgg19.VGG19(
        include_top=True, weights='imagenet', input_tensor=None, input_shape=None,
        pooling=None, classes=1000, classifier_activation='softmax'
    )
    print('\n ---- Saving model locally ----')
    model.save('./weights/')

else:
    print('\n ---- Loading model from local files ----')
    model = tf.keras.models.load_model('./weights/', compile=True)


def process_image(image):
    '''
    Make an image ready-to-use by VGG19
    '''
    # convert the image pixels to a numpy array
    image = img_to_array(image)
    # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # prepare the image for the VGG model
    image = preprocess_input(image)

    return image


def predict_class(image):
    '''
    Predict and render the class of a given image 
    '''
    # predict the probability across all output classes
    yhat = model.predict(image)
    # convert the probabilities to class labels
    label = decode_predictions(yhat)
    # retrieve the most likely result, e.g. highest probability
    label = label[0][0]
    # return the classification
    prediction = label[1]
    percentage = '%.2f%%' % (label[2]*100)

    return prediction, percentage


if __name__ == '__main__':
    ''' for test'''
    # load an image from file
    # image = load_img('../image.jpg', target_size=(224, 224))
    image = load_img('./static/img/image.jpg', target_size=(224, 224))
    image = process_image(image)
    prediction, percentage = predict_class(image)
    print(prediction, percentage)
