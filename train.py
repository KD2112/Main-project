import cv2
import numpy as np
from keras_squeezenet import SqueezeNet
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.applications.imagenet_utils import _obtain_input_shapepip
from keras.layers import Activation, Dropout, Convolution2D, GlobalAveragePooling2D
from keras.models import Sequential
import tensorflow as tf
import os
IMG_SAVE_PATH = 'image_data_2'

label_lst = ['A','Aa','Ah','Ai','Am','Au','Ba','Bha','Ca','Cha','D_a','D_ha','Da','Dha','E','E_','Ee','Ee_','Ga','Gha','Ha','I','Ii','Ilh','Ill','In','Irr','Ja','Ka','Kha','La','Lha','Ma','N_a','Na','Nga','Nha','Nothing','O','Oo','Pa','Pha','R','Ra','Rha','Sa','Sha','Shha','Space','T_a','T_ha','Ta','Tha','U','U_','Uu','Uu_','Va','Ya','Zha']
NUM_CLASSES = len(label_lst)
CLASS_MAP = {label_lst[i]:i for i in range(NUM_CLASSES)}

def mapper(val):
    return CLASS_MAP[val]


def get_model():
    model = Sequential([
        SqueezeNet(input_shape=(227, 227, 3), include_top=False),
        Dropout(0.5),
        Convolution2D(NUM_CLASSES, (1, 1), padding='valid'),
        Activation('relu'),
        GlobalAveragePooling2D(),
        Activation('softmax')
    ])
    return model


# load images from the directory
dataset = []
for directory in os.listdir(IMG_SAVE_PATH):
    path = os.path.join(IMG_SAVE_PATH, directory)
    if not os.path.isdir(path):
        continue
    for item in os.listdir(path):
        # to make sure no hidden files get in our way
        if item.startswith("."):
            continue
        # to make sure only jpg is extracted
        if not item.endswith(".jpg"):
            continue
        img = cv2.imread(os.path.join(path, item))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227))
        dataset.append([img, directory])

data, labels = zip(*dataset)
labels = list(map(mapper, labels))


# one hot encode the labels
labels = np_utils.to_categorical(labels)

# define the model
model = get_model()
model.compile(
    optimizer=Adam(lr=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# start training
model.fit(np.array(data), np.array(labels), epochs=10)

# save the model for later use
model.save("malayalam-sign-language-model_2(10).h5")
