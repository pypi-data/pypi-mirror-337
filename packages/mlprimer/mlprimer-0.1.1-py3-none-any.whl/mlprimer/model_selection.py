import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def train_models(X_train, y_train):
    models = {
        "Logistic Regression": LogisticRegression(solver='saga', max_iter=2000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42)
    }

    for name, model in models.items():
        model.fit(X_train, y_train)

    return models


def evaluate_models(models: dict, X_test, y_test) -> pd.DataFrame:
    results = []

    for name, model in models.items():
        preds = model.predict(X_test)
        results.append({
            "Model": name,
            "Accuracy": accuracy_score(y_test, preds),
            "Precision": precision_score(y_test, preds),
            "Recall": recall_score(y_test, preds),
            "F1 Score": f1_score(y_test, preds)
        })

    return pd.DataFrame(results)
