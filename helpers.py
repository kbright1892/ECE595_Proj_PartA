from math import log2
from data import data, features, outcomes


def calculate_entropy(positive_cnt: int, negative_cnt: int) -> float:
    total_cnt: int = positive_cnt + negative_cnt
    positive_pct: float = positive_cnt / total_cnt
    negative_pct: float = negative_cnt / total_cnt

    if positive_cnt == 0 or negative_cnt == 0:
        return 0

    return -(positive_pct * log2(positive_pct) + negative_pct * log2(negative_pct))


def calculate_information_gain(row_indices: list, feature: str, orig_entropy: float) -> float:
    # indices for dictionary arrays in a more understandable format 
    yes_no_enum: dict = { "yes_cnt": 0, "no_cnt": 1}
    # dictionary format: feature_option -> [yes_cnt, no_cnt]  
    feature_outcomes: dict[str, list] = {}

    for row in row_indices:
        # this is the value for the column, i.e. sunny for outlook
        # this gets the index for the feature in the data array and then checks to see
        # if the value option for that feature is in the feature outcome dictionary
        if data[row][features[feature]] not in feature_outcomes:
            feature_outcomes[data[row][features[feature]]] = [0,0]
        
        # logs the outcome based on the feature option
        if outcomes[row] == 'yes':
            feature_outcomes[data[row][features[feature]]][yes_no_enum["yes_cnt"]] += 1
        else:
            feature_outcomes[data[row][features[feature]]][yes_no_enum["no_cnt"]] += 1    

    row_cnt: int = len(row_indices)
    weighted_entropy: float = 0.0
    
    # calculate weighted entropy for each feature option    
    for value in feature_outcomes:
        cnt_of_value_rows = feature_outcomes[value][0] + feature_outcomes[value][1]
        weighted_entropy += (cnt_of_value_rows/row_cnt) * calculate_entropy(feature_outcomes[value][0], feature_outcomes[value][1])
  
    return orig_entropy - weighted_entropy


def rank_features(indices, remaining_features):
    yes_cnt: int = 0
    no_cnt: int = 0

    for i in indices:
        if outcomes[i] == 'yes':
            yes_cnt += 1
        else:
            no_cnt += 1

    if yes_cnt == 0:
        return None, 'no'
    elif no_cnt == 0:
        return None, 'yes'

    orig_entropy = calculate_entropy(yes_cnt, no_cnt)

    information_gain: dict[str, float] = {}

    # for each column, enumerate the 
    for feature in remaining_features:
        information_gain[feature] = calculate_information_gain(indices, feature, orig_entropy)

    sorted_features: list[list] = []
    for entry in information_gain:
        sorted_features.append([entry, information_gain[entry]])

    sorted_features.sort(key=lambda x: x[1], reverse=True)

    return sorted_features, None
