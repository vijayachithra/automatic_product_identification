from keras.preprocessing import image
from tensorflow import keras
import numpy as np
from six.moves import urllib
import os
import cv2
import numpy as np
from PIL import Image
from keras.models import load_model
from keras.preprocessing import image
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from product_size import findProductSize
#BAG NULL MarieGold COLGATE
#BAG COLGATE MarieGold SHOE

def product_detection(path):
    new_model = keras.models.load_model('products_identification.h5')
    size=150
    test_image = image.load_img(path, target_size=(size, size))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    test_image.reshape(size, size, 3)
    result = new_model.predict(test_image, batch_size=1)
    print(result)
    index = np.argmax(result)
    product_id = get_product_id(path,index+1)
    print(product_id)
    return product_id

def get_product_id(path, index):
    size = findProductSize(path)
    print('size',size)
    if index==1:
        return 1001
    elif index==2:
        if size in range(700, 800):
            return 1002
        else:
            return 1003
    elif index==3:
        return 1004
    elif index==4:
        return 1005
    elif index==5:
        return 1006
    elif index==6:
        return 1007
    elif index==7:
        if size in range(600, 800):
            return 1008
        else:
            return 1009
    elif index==8:
        return 1010
    elif index==9:
        if size in range(500, 600):
            return 1012
        else:
            return 1011
    elif index==10:
        return 1013
    else:
        pass
    