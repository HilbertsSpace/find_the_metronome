# Find The Metronome

This is a collection of python scripts to record audio, identify a recurring audio element (like a metronome tick), and train a Naive Bayes classifier to find it.  

## Installation
Install the packages listed in the readme, they are fairly standard.  

## Usage
To retrain this classifier on new data run the following scripts in order.  record_data.py, plot_data.py, manually_label_data.py, train_and_save_gnb.py, and test_and_plot.py.  Please read over the scripts before running them.  

##Methods
### Data Collection
I recorded 100 seconds of metronome clicks at 252 beats per minute, with background noise.  You can find this recording in the data folder. 
### Labeling
label a single metronome click manually by finding it's start and end point.  I use the plot_data.py script to visually identify a single beat.  Use the starting and ending points you find to run the manually_label_data.py script.  Using the know BPM of 252 and the audio sampling rate I find the spacing between beats and use this to label the data automatically.
### Training
I trained on around half of the labeled data.  I didn't shuffle the train and test set, I train on the first half and test on the latter.  the script 'train_and_save_gnb.py' is used for training a Gaussian NB classifier on the data.  

## Results
After training on the data included in this repo the naive bayes classifier achieved around 90% accuracy.  The classes are imbalanced and the precision on positive classes is low (around 55%), this could be improved.  Plotting the results of the classifier against the data using the test_and_plot.py script shows the kind  of mistakes the classifier makes.  It misclassifies points when the background noise is high and is likely using signal loudness as a major deciding factor.  This classifier is not resilient against noise and can definitely be improved.  

## License
[MIT](https://choosealicense.com/licenses/mit/)
