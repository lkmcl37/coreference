1. Modules:
   - corpus.py: build corpus data and all mentions pairs
   - feature.py: mention class and mention pair class, feature engineering here
   - get_files.py: generate scorer readable gold and response files
   - run.py: the main module to run
  
2. Usage:
   - in command line interface, type in:
   python run.py -h to see help message
   - to run both TRAIN and TEST procedures, follow the steps below (may take around 20 mins to train):
   1. python run.py train : to train the model
   2. python run.py test : to test the trained model on test data
   3. perl scorers/scorer.pl all gold.txt response.txt "none" :
   to evaluate the response with all metric measurements
   - to test on dev data with already trained model:
   1. python run.py dev
   2. perl scorers/scorer.pl all gold.txt response.txt "none"
   - to only quickly check the test evaluation result:
   1. perl scorers/scorer.pl all gold.txt response.txt "none"

3. For developers:
   - to improve the performance, only need to tune the feature.py and model in line 43 in run.py.
   