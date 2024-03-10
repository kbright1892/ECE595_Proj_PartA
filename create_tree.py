from data import data, features
from helpers import rank_features
from Node import Node, HeadNode

node_number = 0

def split_node(node: Node | HeadNode):
    indices = node.indices
    remaining_features = node.remaining_features
    sorted_features, decision = rank_features(indices, remaining_features)

    if decision:
        node.decision = decision
        node.is_leaf = True
        return
    
    node.split_feature = sorted_features[0][0]
    node.information_gain = sorted_features[0][1]

    remaining_features.remove(node.split_feature)

    # create dictionary for each feature value and the indices that have that value
    # will be used to create child nodes
    feature_values: dict[str, list[int]] = dict()
    split_feature_index = features[node.split_feature]
    for index in indices:
        feature_value = data[index][split_feature_index]
        if feature_value not in feature_values:
            feature_values[feature_value] = [index]
        else:
            feature_values[feature_value].append(index)

    for feature_value in list(feature_values.keys()):
        new_node = Node(feature_values[feature_value], remaining_features, node.level + 1 ,feature_value)
        split_node(new_node)
        node.children.append(new_node)

def print_tree(node: HeadNode | Node):
    print(node)

    for child in node.children:
        print_tree(child)

def main():
    row_indices: list = []
    row_indices.extend(range(1, len(data) + 1))

    # create head node
    head: HeadNode = HeadNode(row_indices, list(features.keys()), 0)
    split_node(head)
    print_tree(head)


if __name__ == '__main__':
    main()