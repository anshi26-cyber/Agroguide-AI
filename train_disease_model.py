import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import os

dataset_path = "plant_disease_dataset"

img_size = (128, 128)
batch_size = 16

train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

model = models.Sequential([
    layers.Conv2D(
        32, (3,3),
        activation='relu',
        input_shape=(128,128,3)
    ),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(
        64, (3,3),
        activation='relu'
    ),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(
        128, (3,3),
        activation='relu'
    ),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),

    layers.Dense(
        128,
        activation='relu'
    ),

    layers.Dense(
        train_generator.num_classes,
        activation='softmax'
    )
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=5
)

model.save(
    "core/ml/disease/disease_model.h5"
)

with open(
    "core/ml/disease/labels.txt",
    "w"
) as f:
    for label in train_generator.class_indices:
        f.write(label + "\n")

print("Disease model trained successfully!")