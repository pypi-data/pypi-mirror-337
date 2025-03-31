
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_science_hack_functions import summary_dataframe, summary_column

from data_science_hack_functions.classification import run_nested_cv_classification
from data_science_hack_functions.regression import run_nested_cv_regression
from data_science_hack_functions.multiclass_classification import run_nested_cv_multiclass_classification
print("Package imported successfully!")
