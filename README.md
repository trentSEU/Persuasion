# Persuasion
- This project is a part of the persuasion tool project
- persuasion.py
  - gettingFeatures() function is the most important part of this file. This function helps us to get all the machine learning needed features of the given text. We use this function to get features for each document in the corpus and save those features in a csv file which will be used in models training.
- DecisionModels.py
  - This file is used for models training, the models will be dumped for future use.
- csv_modifier.py
  - Modify the output of persuasion.py to the format of the input of DecisionModels.py 