from sklearn.naive_bayes import GaussianNB
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sql_helpers import get_labeled_audio_data
from joblib import dump, load


PLOT_FULL_SIGNAL = True
model_filepath = 'pickle_jar/nb_classifier.joblib'
DB_NAME = 'testDB'

cnx = mysql.connector.connect(user='free')
cursor = cnx.cursor()
# get the data
X, y = get_labeled_audio_data(cursor, DB_NAME)

# spliting the data in half to train and test
X_train = X[0:1000]
X_test_full = X[1000:]
y_train = y[0:1000]
y_test_full = y[1000:]

# train a classifier
gnb = GaussianNB()
y_pred_full = gnb.fit(X_train, y_train).predict(X_test_full)
dump(gnb, model_filepath) # save it

print('saved to %s'%model_filepath)
print(confusion_matrix(y_test_full, y_pred_full))
print(classification_report(y_test_full, y_pred_full, target_names=['no_metronome', 'metronome']))

# this loop plots out all the data
# there is a red line fort the classifiers output predicition and a yellow line for the correct output
if PLOT_FULL_SIGNAL:
    step = 100
    ind = 0
    while ind+step < len(y_pred_full):
        y_pred = y_pred_full[ind:ind+step]
        y_test = y_test_full[ind:ind+step]
        X_test = X_test_full[ind:ind+step]
        X_test_joined = np.concatenate(X_test)

        y_x = [i*512 for i in range(len(y_pred))]
        y_maxed = [each*max(X_test_joined) for each in y_pred]

        yt_x = [i*512 for i in range(len(y_pred))]
        yt_maxed = [each*max(X_test_joined) for each in y_test]

        plt.plot([i for i in range(len(X_test_joined))], X_test_joined, 'b', alpha=.5) # plots audio data
        plt.plot(y_x, y_maxed, 'r', alpha=.5)
        plt.plot(yt_x, yt_maxed, 'y', alpha=.5)
        plt.show()
        plt.clf()
        ind+=step

