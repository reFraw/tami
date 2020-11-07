from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras.metrics import Precision, Recall, AUC


class NEDO:

    def __init__(self, num_classes, img_size, channels, name="nedo"):
        self.name = name
        self.num_classes = num_classes
        self.input_width_height = img_size
        self.channels = channels

    def build(self):
        model = models.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(self.input_width_height,
                                                                            self.input_width_height,
                                                                            self.channels)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(96, (3, 3), activation='relu'))
        model.add(layers.Conv2D(128, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Flatten())
        model.add(layers.Dropout(0.45))  # Dropout for regularization
        model.add(layers.Dense(1024, activation='relu'))
        model.add(layers.Dropout(0.40))
        model.add(layers.Dense(512, activation='relu'))
        model.add(layers.Dropout(0.35))
        model.add(layers.Dense(256, activation='relu'))
        model.add(layers.Dense(self.num_classes, activation='softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='adam',
                      metrics=['acc', Precision(name="prec"), Recall(name="rec"), AUC(name='auc')])

        return model

    def build_tuning(self, hp):

        model = models.Sequential()
        model.add(layers.Conv2D(hp.Int('filters_1', 16, 128, step=16), (3, 3), activation='relu',
                                input_shape=(self.input_width_height, self.input_width_height, self.channels)))
        model.add(layers.MaxPooling2D((2, 2)))
        for i in range(hp.Int('conv_blocks', 2, 5, default=3)):
            model.add(layers.Conv2D(hp.Int('filters_' + str(i), 32, 256, step=32), (3, 3), activation='relu'))
            model.add(layers.MaxPooling2D((2, 2)))
            #if hp.Choice('pooling_' + str(i), ['avg', 'max']) == 'max':
            #    x = tf.keras.layers.MaxPool2D()(x)
            #else:
            #    x = tf.keras.layers.AvgPool2D()(x)
        model.add(layers.Flatten())
        model.add(layers.Dropout(hp.Float('dropout', 0, 0.7, step=0.1, default=0.5)))
        model.add(layers.Dense(hp.Int('hidden_size', 512, 1024, step=128, default=512), activation='relu'))
        model.add(layers.Dropout(hp.Float('dropout', 0, 0.7, step=0.1, default=0.5)))
        model.add(layers.Dense(hp.Int('hidden_size', 128, 512, step=128, default=512), activation='relu'))
        model.add(layers.Dense(self.num_classes, activation='softmax'))
        # activation=hp.Choice('act_1', ['relu', 'tanh'])

        model.compile(loss='categorical_crossentropy', optimizer='adam',
                      metrics=['acc', Precision(name="prec"), Recall(name="rec"), AUC(name='auc')])

        return model
