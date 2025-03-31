# **Visualization of Incomplete Datasets** #
This project focuses on visualizing incomplete datasets, where missing data is represented using shadows or other graphical elements. The goal is to facilitate the interpretation of missing values and help analysts gain a deeper understanding of the data.

# **Usage** #

import pandas as pd

from missing_data_as_shadows import make_full_analysis, scatter_with_shadows_rect_binned

# Load data with missing values
df = pd.read_csv('data.csv')

# Generate visualization
make_full_analysis(df, output_name="output_name", method="spearman")

**Method parameter is correlation method**

If you don't provide method parameter default is pearson.

The method parameter allows you to select any correlation method supported by pandas, such as:

- pearson

- kendall

- spearman