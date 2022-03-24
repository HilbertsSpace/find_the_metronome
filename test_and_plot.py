from sklearn.naive_bayes import GaussianNB
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
from sql_helpers import get_unlabeled_audio_data
from joblib import dump, load


PLOT_FULL_SIGNAL = True
model_filepath = 'pickle_jar/nb_classifier.joblib'
DB_NAME = 'testDB'

# connect to db
cnx = mysql.connector.connect(user='free')
cursor = cnx.cursor()

# get the data from db table using helper func
X_full = get_unlabeled_audio_data(cursor, DB_NAME)
print(len(X_full))
clf = load(model_filepath)
y_pred_full = clf.predict(X_full)

if PLOT_FULL_SIGNAL:
    step = 100
    ind = 0
    while ind+step < len(y_pred_full):
        y_pred = y_pred_full[ind:ind+step]
        X = X_full[ind:ind+step]
        X_test_joined = np.concatenate(X)

        y_x = [i*512 for i in range(len(y_pred))]
        y_maxed = [each*max(X_test_joined) for each in y_pred]

        plt.plot([i for i in range(len(X_test_joined))], X_test_joined, 'b', alpha=.5) # plots audio data
        plt.plot(y_x, y_maxed, 'r', alpha=.5)
        plt.show()
        plt.clf()
        ind+=step
