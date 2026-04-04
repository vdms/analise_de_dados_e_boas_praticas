# analise_de_dados_e_boas_praticas

## Dataset for MVP

This repository includes `dataset.csv`, sourced from the Kaggle dataset
"Predict students' dropout and academic success":
https://www.kaggle.com/datasets/thedevastator/higher-education-predictors-of-student-retention

### What this dataset is about

The dataset is designed for student retention analysis in higher education.
It supports classification tasks to predict whether a student will:
- `Dropout`
- `Enrolled`
- `Graduate`

Predictor variables include:
- Demographic and socioeconomic information.
- Academic path and prior qualifications.
- Performance indicators from the 1st and 2nd semesters.
- Macroeconomic context variables (for example unemployment, inflation, and GDP).

### Local file summary (`dataset.csv`)

- Records: `4,424` (excluding header)
- Columns: `35`
- Target column: `Target`

Target distribution in this file:
- `Graduate`: `2,209` (`49.93%`)
- `Dropout`: `1,421` (`32.12%`)
- `Enrolled`: `794` (`17.95%`)

### Usage in this project

This CSV is the baseline dataset for the postgraduate MVP and will be used in
data exploration, feature analysis, and initial predictive modeling experiments.
