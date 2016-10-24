The folder contains the following files:
    - ./corpus.it: The training corpus
    - ./POS_hmmlearn.py: The tagging script
    - ./hmm_pretrain.pkl: The pretrained HMM model. 
Please make sure these files are in the same folder.

To execute the script, please make sure the following python packages are installed:
    - Numpy (>=0.7.0)
    - Scipy (>=0.17.0)
    - hmmlearn
    - Scikits-learn 

The code can be executed with the following command:
$> python ./POS_hmmlearn.py [-h] [-t] [-v]
optional arguments:
-h, --help     show this help message and exit
-t, --train    Train a new HMM model.
-v, --verbose  Print the original & tagged sentences.

Explanation:
I used the package "hmmlearn" to train the model and predict the hidden states (numeric states) of the corpus.
To calculate the accuracy of the tagging predictions, I stored the result into a confusion matrix "labels vs. hidden-states (numeric)". I used two methods to calculate the accuracy.
    Method 1: I used the Hungarian Algorithm in 'scipy.optimize' package to assign hidden states to labels. This algorithm can find out the maximum/minimum sum of an 'assignment problem'. With this assignment, I calculate the corresponding sum in the confusion matrix.
    Method 2: I used a greedy method to calculate the accuracy. I select the maximum value in the confusion matrix and assign the state to the corresponding label. Then I removed the column and row in the matrix. In the end we can obtain a sum.
In verbose mode, I used the calculated assignment (Method 1) to map the hidden states to the existing labels and output the decoded POS tags.