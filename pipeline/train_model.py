# INPUT: folder containing 2 embeddings files
# OUTPUT: new folder containing trained model file
import numpy as np
from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.layers import Dense
from keras.metrics import Precision, Recall
import tensorflow as tf
import os

EMB_PATH = "INPUT DIRECTORY PATH"
MODEL_NAME = "OUTPUT DIRECTORY NAME"
MODEL_PATH = f"OUTPUT DIRECTORY PATH"

K = 5

# loads numpy array of dimensions: X - (num_images, 1280, 1), y - (num_images, num_classes)
files = sorted(os.listdir(EMB_PATH))
X = np.load(f"{EMB_PATH}{files[0]}")  
y = np.load(f"{EMB_PATH}{files[1]}")

# 70-20-10 split of data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

num_classes = y.shape[1]

def k_folds_split(X, y, n=1):
    p = np.random.permutation(len(X))
    X, y = X[p], y[p]
    x_split = np.array_split(X, n)
    y_split = np.array_split(y, n)
    return (x_split, y_split)

def k_folds_join(X, y, ind=0):
    n = len(X)
    train_x, train_y = None, None
    test_x, test_y = X[ind], y[ind]

    for i in range(n):
        if i != ind:
            if type(train_x) != np.ndarray:
                train_x, train_y = X[i], y[i]
            else:
                train_x = np.concatenate((train_x, X[i]))
                train_y = np.concatenate((train_y, y[i]))
    
    return (train_x, train_y), (test_x, test_y)

def kfolds_train(X, y, K):
    results = []
    X_split, y_split = k_folds_split(X, y, K) 

    for i in range(K):
        (X_train, y_train), (X_val, y_val) = k_folds_join(X_split, y_split, i)

        model = Sequential([
            Dense(1024, input_dim=1280, activation='relu'),
            Dense(1024, activation='relu'),
            Dense(num_classes, activation='softmax')
        ])

        model.compile(loss='categorical_crossentropy', optimizer='adam', 
            metrics=['accuracy', Precision(name='precision'), Recall(name='recall')])

        model.fit(X_train, y_train, epochs=20, batch_size=128, validation_data=(X_val, y_val))

        result = model.evaluate(X_test, y_test)
        results.append(result)
    
    return model, results

model, results = kfolds_train(X_train, y_train, K)

def display_kfolds_results(results):
    mean_results = [0 for i in range(len(results[0]))]
    for i in range(K):
        for j in range(len(results[i])):
            mean_results[j] += results[i][j]
        print(f"Model {i+1}: {results[i][1]:.4f} (accuracy) {results[i][2]:.4f} (precision) {results[i][3]:.4f} (recall)")

    mean_results = [i/K for i in mean_results]
    print(f"\nMean: {mean_results[1]:.4f} (accuracy) {mean_results[2]:.4f} (precision) {mean_results[3]:.4f} (recall)")

model.save(f"{MODEL_PATH}{MODEL_NAME}.h5")