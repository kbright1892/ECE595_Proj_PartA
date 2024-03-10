from data import data, features
from helpers import rank_features
from Node import Node, HeadNode

# split node is called recursively until all leaf nodes are found
# it calculates the information gain of all remaining features and splits on the best one
def split_node(node: Node | HeadNode) -> None:
    indices: list[int] = node.indices
    remaining_features: list[str] = node.remaining_features
    sorted_features, decision = rank_features(indices, remaining_features)

    # exit condition - all outcomes are the same
    if decision:
        node.decision = decision
        node.is_leaf = True
        return
    
    # top ranked feature based on IG
    node.split_feature = sorted_features[0][0]
    # information gain for that feature
    node.information_gain = sorted_features[0][1]

    # remove the split features so it can't be selected again by a descendant node
    remaining_features.remove(node.split_feature)

    # create dictionary for each feature value and the indices in the data subset that have that value
    # will be used to create child nodes
    feature_values: dict[str, list[int]] = dict()
    split_feature_index: int = features[node.split_feature]
    for index in indices:
        feature_value = data[index][split_feature_index]
        if feature_value not in feature_values:
            feature_values[feature_value] = [index]
        else:
            feature_values[feature_value].append(index)

    # create a child for each value of the split feature with the indices of the data rows with that value
    for feature_value in list(feature_values.keys()):
        new_node: Node = Node(feature_values[feature_value], remaining_features, node.level + 1 ,feature_value)
        split_node(new_node)
        node.children.append(new_node)

# prints the tree, tabbed in for each level with -- representing connecting lines and the assicated feature value
# uses a preorder traversal to maintain parent-child relationships
def print_tree(node: HeadNode | Node) -> None:
    print(node)

    for child in node.children:
        print_tree(child)

# entry point for full tree creation
def main():
    # indices of all rows in the dataset
    row_indices: list = list(data.keys())

    # create head node which includes all data and all features with a level of 0
    head: HeadNode = HeadNode(row_indices, list(features.keys()), 0)
    split_node(head)
    print_tree(head)


if __name__ == '__main__':
    main()