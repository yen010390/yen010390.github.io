---
title: "AI Project – Research Projects"
excerpt: "Projects focused on applied AI, ML pipelines, and research-oriented implementations."
collection: project
category: "Category 5: Others"
---

## 👉 My AI learning path — On-processing: [AIO Project](https://github.com/orgs/aio25-mix002/repositories)

---


## 🧠 Research Projects

### 📰 [**1. News Article Topic Classification (NLP)**](https://github.com/aio25-mix002/m03-p0301)
**Dataset:** arXiv abstracts (5 classes: astro-ph, cond-mat, cs, math, physics) 

**Goal:** Build an extensible NLP pipeline for topic classification.

- Compared **BoW / TF-IDF / Sentence Embeddings (+ LSA / Faiss)**  
- Evaluated across **KNN, Decision Tree, Naive Bayes, Logistic Regression, SVM, Random Forest, AdaBoost, Gradient Boost, Stacking**  
- Applied **advanced preprocessing** (lemmatization, stopword removal), **data augmentation & imbalance handling** (back-translation, synonyms, SMOTE/ADASYN, class weights)  
- Evaluated with **Accuracy, macro-F1, ROC-AUC, Confusion Matrix**  
- Deployed a **Streamlit app** for EDA, training, and live prediction with **word-level explanations** (LR/NB)  
- Modular codebase (OOP), **uv** for package management, **ruff** for linting  

---

### 🏠 [**2. House Price Prediction (Advanced Regression Techniques)**](https://github.com/aio25-mix002/m05-p0501)
**Dataset:** Kaggle - Advanced Regression Techniques.

**Goal:** Build a reproducible ML pipeline for regression on structured tabular data.

- Modular **data pipeline** with preprocessing (imputation, one-hot, scaling, polynomial features, feature selection)  
- 10 models from regularized linear (Lasso/Ridge/ElasticNet) to **tree-based ensembles** (RF, GBM, XGBoost, LightGBM, CatBoost)  
- Used **k-fold cross-validation** and **Optuna** for hyperparameter tuning  
- Evaluated by **RMSE / MAE / R² + training time**  
- Delivered a **Streamlit app** for EDA, experiment runner, live prediction  
- Added **SHAP & tree feature importance** for model interpretability  

---

### ❤️ [**3. Heart Disease Risk Prediction (Classification)**](https://github.com/orgs/aio25-mix002/repositories)
**Dataset:** UCI Heart Cleveland · 303 samples · 11 features + 1 label  

**Goal:** Predict cardiovascular risk with a robust, generalizable ML pipeline.

- **Feature engineering:** created **age-normalized ratios** (chol_per_age, trestbps_per_age)  
- **Feature selection:** top 10 by Decision Tree importance  
- **Pipeline + GridSearchCV (cv = 3, scoring = ROC-AUC)** across 9 models (LR, KNN, DT, SVM-RBF, RF, AdaBoost, GBM, LGBM, XGB)  
- **Performance:** AUC up to 0.97 (LR), ~0.95 (RF/XGB), Accuracy ~0.87  
- **Recall-oriented configs** to minimize false negatives  
- Built **Streamlit interface** for patient-level input, ROC curve, Confusion Matrix, Feature Importance visualization  

---

*© 2025 – Nguyễn Tuấn Anh et al., AIO 2025 (MIX002 Teams)*  
