from data import data, features
from helpers import rank_features

def main():
    # get the values for all keys in the data dictionary
    row_indices: list = list(data.keys())

    # rank_features returns the features in descending order by information gain
    # list(features.keys()) is an array of all features
    # sorted_features is a list of lists. Each list has the feature in index 0 and the IG in index 1
    sorted_features, _, __ = rank_features(row_indices, list(features.keys()))

    print("Feature Rank (Information Gain)\n=======================================")

    # print the list of features and their information gain in a formatted way
    for i in range(0, len(sorted_features)):
        print(f'{i + 1}. {str(sorted_features[i][0]).capitalize()} - {sorted_features[i][1]}')

if __name__ == '__main__':
    main()