import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import KFold, StratifiedKFold

def run_random_forest(X_data, Y_data, rf_classifier, cross_validation):
    scores = []
    predictions = []

    for train_index, test_index in cross_validation.split(X_data, Y_data):
        print("*****")
        # Split the data into training data and test data
        x_train, x_test = X_data.iloc[train_index], X_data.iloc[test_index]
        y_train, y_test = Y_data.iloc[train_index], Y_data.iloc[test_index]
        # print out some general information about the data in this split
        print("X_train: ", x_train.shape)
        print("Y_train: " + str(y_train.shape) + " - Number of True values: " +
              str(len(y_train) - y_train["pumped"].value_counts()[False]))
        print("X_test: ", x_test.shape)
        print("Y_test: " + str(y_test.shape) + " - Number of True values: " +
              str(len(y_test) - y_test["pumped"].value_counts()[False]))

        # train the model
        rf_classifier.fit(x_train, y_train.values.ravel())
        # test with cross validation
        prediction = rf_classifier.predict(x_test)
        prediction = prediction.reshape((prediction.shape[0], 1))
        predictions.append(prediction)
        score = rf_classifier.score(x_test, y_test.values.ravel())
        print("Are predictions the same as actual values? " + str(np.array_equiv(prediction, y_test.values)))
        scores.append(score)

    return predictions, scores


# run the random forest model with the test data, and print out the result
# need to pass in the split point as parameter as which part of the data is
# considered the test data, that the model has not seen yet.
def test_model(scores, X_reg, Y_reg, split_point, rf_classifier, model_num):
    print(scores)
    print("Shape of test data: For X: " + str(X_reg[split_point:].shape) + " - For Y: " + str(Y_reg[split_point:].shape))
    X_t = X_reg[split_point:]
    X_t.fillna(0, inplace=True)
    Y_t = Y_reg[split_point:]
    Y_t.fillna(0, inplace=True)
    rf_classifier.predict(X_t)
    s = rf_classifier.score(X_t, Y_t)
    print("Number of True values in Y_test: ", len(Y_t) - Y_t["pumped"].value_counts()[False])
    print("Accuracy of model " + str(model_num) + " :" + str(s))
    print("==================")


# given the training data, we need to stratify it first with cross validation because of
# the nature of the data, where it is extremely imbalanced.
# create two different random forest models, train them with given training data.
# then test the models with the actual test data.
def predict_results(X_reg, Y_reg, X_model, Y_model):
    # Apply cross validation and stratify the data with both models
    cross_validation = StratifiedKFold(n_splits=5, shuffle=True, random_state=None)

    # create and train the first random forest model
    print("Running the 1st model...")
    rf_classifier_1 = RandomForestClassifier(n_estimators=30, criterion='gini', max_depth=5, min_samples_split=2,
                                             min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto',
                                             max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None,
                                             bootstrap=True, oob_score=False, n_jobs=-1, random_state=0, verbose=0,
                                             warm_start=False, class_weight='balanced')
    predictions_1, scores_1 = run_random_forest(X_model, Y_model, rf_classifier_1, cross_validation)
    print("Done!\n")

    print("************************\n")

    # create and train the second random forest model
    print("Running the 2nd model...")
    rf_classifier_2 = RandomForestClassifier(n_estimators=200, criterion='gini', max_depth=5, min_samples_split=2,
                                             min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto',
                                             max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None,
                                             bootstrap=True, oob_score=False, n_jobs=-1, random_state=0, verbose=0,
                                             warm_start=False, class_weight='balanced')
    predictions_2, scores_2 = run_random_forest(X_model, Y_model, rf_classifier_2, cross_validation)
    print("Done!\n")

    # TEST THE MODELS WITH TEST DATA
    # for model 1
    test_model(scores_1, X_reg, Y_reg, 3001, rf_classifier_1, 1)

    # for model 2
    test_model(scores_2, X_reg, Y_reg, 50001, rf_classifier_2, 2)