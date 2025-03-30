from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

def grid_search(model, param_grid, X_train, y_train, scoring='accuracy', cv=3):
    search = GridSearchCV(estimator=model, param_grid=param_grid,
                          cv=cv, scoring=scoring, n_jobs=-1, verbose=1)
    search.fit(X_train, y_train)
    return search

def randomized_search(model, param_distributions, X_train, y_train, n_iter=20,
                      scoring='accuracy', cv=3, random_state=42):
    search = RandomizedSearchCV(estimator=model, param_distributions=param_distributions,
                                n_iter=n_iter, cv=cv, scoring=scoring,
                                random_state=random_state, n_jobs=-1, verbose=1)
    search.fit(X_train, y_train)
    return search
