1. Modules:
   - corpus.py: build corpus data and all mentions pairs
   - feature.py: mention class and mention pair class, feature engineering here
   - get_files.py: generate scorer readable gold and response files
   - run.py: the main module to run
   - best performance: MUC - 66.14%
  
2. Usage:
   - in command line interface, type in:
   python run.py -h to see help message
   - to only quickly check the TEST evaluation result (we have the trained model and test result given):
   1. perl scorers/scorer.pl all gold.txt response.txt "none"
   - to run both TRAIN and TEST procedures, follow the steps below (may take around 20 mins to train):
   1. python run.py train : to train the model
   2. python run.py test : to test the trained model on test data
   3. perl scorers/scorer.pl all gold.txt response.txt "none" :
   to evaluate the response with all metric measurements
   - to test on DEV data with already trained model:
   1. python run.py dev
   2. perl scorers/scorer.pl all gold.txt response.txt "none"

3. For developers:
   - to improve the performance, only need to tune the feature.py and model in line 47 in run.py.

4. Notes:
   If "too many repeated mentions in the response" happens during evaluation with scorer.pl,
   please try to evaluate that failed measure metric separately. This seems to be a bug from
   the provided scorer.pl.
   