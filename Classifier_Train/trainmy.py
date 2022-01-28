from tensorflow.python.keras.callbacks import CSVLogger

from model import mobilenet, myconfig
import tensorflow as tf
import logging
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.mobilenet import preprocess_input
import os

# General functions
def plot_learning_curve(
        title: str, x: int, y: int, y_test: int, ylim: float = 0.6, path: str = '') -> None:
    plt.figure()
    plt.title(title)
    axes = plt.gca()
    axes.set_ylim([ylim, 1])
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    train_sizes = x
    train_scores = y
    test_scores = y_test

    plt.grid()

    plt.plot(
        train_sizes,
        train_scores,
        "o-",
        label="Training accuracy",
    )
    plt.plot(
        train_sizes,
        test_scores,
        "o-",
        label="Validation accuracy",
    )

    plt.legend(loc="best")

    plt.savefig(path + 'train_result.png', bbox_inches='tight')

def save_tflite(model, path: str):
    converter = tf.compat.v1.lite.TFLiteConverter.from_keras_model_file(path + 'weights.h5')
    tfmodel = converter.convert()
    file = open(path + 'weights.tflite', 'wb')
    file.write(tfmodel)

def plot_history(history: "History", path: str = '') -> None:
    y = history.history["accuracy"]
    y_test = history.history["val_accuracy"]
    plot_learning_curve("Training process", np.arange(1, 1 + len(y)), y, y_test, 0, path)


# pooling='avg', use around padding instead padding bottom and right for k210
base_model = mobilenet.MobileNet0(input_shape=myconfig.input_shape,
                                  alpha=0.75, depth_multiplier=1, dropout=0.001, pooling='avg',
                                  weights='imagenet', include_top=False)
# update top layer
out = base_model.output
out = tf.keras.layers.Dropout(0.001, name='dropout')(out)
preds = tf.keras.layers.Dense(len(os.listdir(myconfig.data_dir)), activation='softmax')(out)
model = tf.keras.models.Model(inputs=base_model.input, outputs=preds)

# train
# datasets process

train_gen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    brightness_range=[-20.0 , +20.0],
    rotation_range=10,
    featurewise_center=True,
    featurewise_std_normalization=True,
    channel_shift_range=50.0,
    width_shift_range=0.2, height_shift_range=0.2,
    zoom_range=0,
    shear_range=0
)

train_data = train_gen.flow_from_directory(myconfig.data_dir,
                                           target_size=(myconfig.input_shape[0], myconfig.input_shape[1]),
                                           color_mode='rgb',
                                           batch_size=myconfig.batch_size,
                                           class_mode='sparse',  # None / sparse / binary / categorical
                                           shuffle=True,
                                           subset="training"
                                           )
valid_data = train_gen.flow_from_directory(myconfig.data_dir,
                                           target_size=(myconfig.input_shape[0], myconfig.input_shape[1]),
                                           color_mode='rgb',
                                           batch_size=myconfig.batch_size,
                                           class_mode='sparse',
                                           shuffle=False,
                                           subset="validation"
                                           )

print("train data:{}, valid data:{}".format(train_data.samples, valid_data.samples))

classes = train_data.class_indices
classfile = open(myconfig.savepath + 'classnames.txt', 'w')
classfile.write(str(classes))
classfile.close()

# Save model structure to file
with open(myconfig.savepath + 'model.txt', 'w') as txtfile:
    model.summary(print_fn=lambda x: txtfile.write(x + '\n'))

# Compile and train the classifier
model.compile(
    optimizer=tf.keras.optimizers.SGD(lr=0.001, momentum=0.9, decay=0.01),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Create callback and save the model with best (=highest) validation accuracy
checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(
    filepath=myconfig.savepath + 'weights.h5',
    monitor='val_accuracy',
    save_best_only=True
)

# Create callback for saving training step info to file
csvlogger_cb = CSVLogger(myconfig.savepath + 'training_log.csv', append=True, separator=';')

history = model.fit(train_data, validation_data=valid_data,
                    steps_per_epoch=train_data.samples // myconfig.batch_size,
                    validation_steps=valid_data.samples // myconfig.batch_size,
                    epochs=myconfig.epochs,
                    callbacks=[checkpoint_cb, csvlogger_cb])

plot_history(history, myconfig.savepath)

# Save as tflite to disk
save_tflite(model, myconfig.savepath)

# Load best saved model for evaluation
model_eval = load_model(myconfig.savepath + 'weights.h5')

# Evaluate model
val_loss, val_acc = model_eval.evaluate(valid_data)

print('val_loss: ' + str(val_loss) + '  val_acc:' + str(val_acc))
