from math import log2
from data import data, features, outcomes


"""
calculates entropy based on the number of yes's and no's passed
@param positive_cnt - number of positive outcomes for the feature or value being considered
@param negative_cnt - number of negative outcomes for the features or value being considered
@returns entropy based on passed counts
"""
def calculate_entropy(positive_cnt: int, negative_cnt: int) -> float:
    total_cnt: int = positive_cnt + negative_cnt
    positive_pct: float = positive_cnt / total_cnt
    negative_pct: float = negative_cnt / total_cnt

    # prevent log2(0) errors
    if positive_cnt == 0 or negative_cnt == 0:
        return 0

    return -(positive_pct * log2(positive_pct) + negative_pct * log2(negative_pct))


"""
calculate the information gain for the passed feature based on the passed pre-split entropy
@param row_indices - a subset of the dataset to be used for the calculation
@param feature - the name of the feature having its information gain calculated
@param original_entropy - the entropy before splitting on the feature
@returns information gain for feature
"""
def calculate_information_gain(row_indices: list, feature: str, orig_entropy: float) -> float:
    # dictionary format: feature_option -> [yes_cnt, no_cnt]  
    feature_value_outcomes: dict[str, list] = {}
    yes_cnt_index = 0
    no_cnt_index = 1
    # get the index of passed feature in each data row
    feature_index = features[feature]

    # calculate the count of yes's and no's for each feature value
    for row in row_indices:
        # get the value of the feature for the current row
        row_feature_value = data[row][feature_index]
        # if the value option for that feature is in the feature outcome dictionary yet, add it
        if data[row][feature_index] not in feature_value_outcomes:
            feature_value_outcomes[data[row][feature_index]] = [0,0]
        
        # logs the outcome based on the feature option for the current row
        if outcomes[row] == 'yes':
            feature_value_outcomes[row_feature_value][yes_cnt_index] += 1
        else:
            feature_value_outcomes[row_feature_value][no_cnt_index] += 1    

    # total number of rows in the subset
    row_cnt: int = len(row_indices)
    weighted_entropy: float = 0.0
    
    # calculate weighted entropy for each feature option and add it to the overall weighted entropy for the feature 
    for value in feature_value_outcomes:
        cnt_of_value_rows: int = feature_value_outcomes[value][0] + feature_value_outcomes[value][1]
        # add the weighted entropy of each feature value to the weighted entropy for the feature
        weighted_entropy += (cnt_of_value_rows/row_cnt) * calculate_entropy(feature_value_outcomes[value][0], feature_value_outcomes[value][1])
  
    # return information gain
    return orig_entropy - weighted_entropy


"""
returns a list of lists of features and their information gain, in descending order by IG
can also determine if the node whose data was passed is a leaf
@param indices is all data rows to be considered in calculations
@param remaining_features is a subset of features that have not been split upon by an ancestor node
@returns 3-tuple
    - list of lists sorted by information gain, if more than 1 feature 
        - each list is [feature, information_gain]
    - decision, if applicable
    - entropy pre-split
"""
def rank_features(indices, remaining_features) -> tuple[list[list[str, float]] | None, str | None, float | int]:
    # calculate the pre-split entropy
    yes_cnt: int = 0
    no_cnt: int = 0

    # calculate the count of yes and no outcomes
    for i in indices:
        if outcomes[i] == 'yes':
            yes_cnt += 1
        else:
            no_cnt += 1

    # if there are no yes's or no no's, it is a leaf, so it gets a decision
    if yes_cnt == 0:
        return None, 'no', 0
    elif no_cnt == 0:
        return None, 'yes', 0

    orig_entropy: float = calculate_entropy(yes_cnt, no_cnt)

    # if this is the final feature and yes or no count isn't 0, return the most likely outcome
    # if yes's and no's are equal in count, return the most likely outcome from the original dataset
    # if that count is also equal, default to yes
    if len(remaining_features) == 1:
        if yes_cnt > no_cnt:
            return None, 'yes', 0
        elif no_cnt > yes_cnt:
            return None, 'no', 0
        else:
            orig_yes_cnt = 0
            orig_no_cnt = 0

            for outcome in list(outcomes.values()):
                if outcome == 'yes':
                    orig_yes_cnt += 1
                else:
                    orig_no_cnt += 1

            if orig_yes_cnt >= orig_no_cnt:
                return None, 'yes', 0 
            elif orig_no_cnt > orig_yes_cnt:
                return None, 'no', 0

    # dictionary of the information gain for each feature
    # features -> information gain
    information_gain: dict[str, float] = {}

    # calculate the information gain for each of the remaining features and add it to the dict
    for feature in remaining_features:
        information_gain[feature] = calculate_information_gain(indices, feature, orig_entropy)

    # convert the dictionary to a list
    sorted_features: list[list] = []
    for entry in information_gain:
        sorted_features.append([entry, information_gain[entry]])

    # sort list of lists in descending order by the second value in each list, which is the information gain
    # sort if stable, so in case of tie, the value with the lowest index will be ranked highest
    sorted_features.sort(key=lambda x: x[1], reverse=True)

    return sorted_features, None, orig_entropy
