import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

print(x_train[0])
print(len(x_train[0]))
print(x_train[0][0])
print(len(x_train[0][0]))

#code from an online tutorial of convolution neural nets: https://towardsdatascience.com/
#make the data workable with Keras
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
input = (28, 28, 1)
x_train = x_train.astype("float32")
x_test = x_test.astype("float32")
x_train /= 255
x_test /= 255


print(x_train.shape,x_test.shape)
print(x_train[0])



#learning to use the keras library and tensorflow
# model = Sequential()
# model.add(Conv2D(28, kernel_size=(3,3), input_shape=input))
# model.add(MaxPooling2D(pool_size=(2,2)))
# model.add(Flatten())
# model.add(Dense(128, activation=tf.nn.relu))
# model.add(Dropout(0.2))
# model.add(Dense(10, activation=tf.nn.softmax))
#
# model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",metrics=["accuracy"])
#model.fit(x=x_train,y=y_train,epochs=20)
#model.evaluate(x_test, y_test)

