from data import data, features
from helpers import rank_features

def main():
    row_indices: list = []
    row_indices.extend(range(1, len(data) + 1))

    sorted_features, _ = rank_features(row_indices, list(features.keys()))

    print("Feature Rank (Information Gain)\n=======================================")

    for i in range(0, len(sorted_features)):
        print(f'{i + 1}. {str(sorted_features[i][0]).capitalize()} - {sorted_features[i][1]}')

if __name__ == '__main__':
    main()