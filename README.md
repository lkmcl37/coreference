1. Modules:
   - corpus.py: build corpus data and all mentions pairs
   - feature.py: mention class and mention pair class, feature engineering here
   - get_files.py: generate scorer readable gold and response files
   - run.py: the main module to run
  
2. Usage:
   - in command line interface, type in:
   python run.py -h to see help message
   - to run the system, follow the steps below:
   1. python run.py train : to train the model
   2. python run.py test : to test the trained model on test data
   3. perl scorers/scorer.pl all gold.txt output.txt "none" :
   to evaluate the response with all metric measurements
   