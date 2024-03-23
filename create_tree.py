from data import data, features
from helpers import rank_features
from Node import Node, HeadNode

"""
split node is called recursively until all leaf nodes are found
it calculates the information gain of all remaining features and splits on the best one
@param node - a Node or Node object
"""
def split_node(node: Node | HeadNode) -> None:
    remaining_features: list[str] = node.remaining_features.copy()
    sorted_features, decision, node.entropy = rank_features(node.indices, remaining_features)
    
    # remaining features sorted in descending order by information gain
    node.sorted_features = sorted_features

    # exit condition - all outcomes are the same or only one feature remaining
    if decision:
        node.decision = decision
        node.is_leaf = True
        return

    # remove the top ranked feature so it can't be selected again by a descendant node
    remaining_features.remove(sorted_features[0][0])

    # create dictionary for each feature value and the indices in the data subset that have that value
    # will be used to create child nodes
    feature_values: dict[str, list[int]] = dict()
    split_feature_index: int = features[sorted_features[0][0]]
    for index in node.indices:
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


"""
prints the tree, tabbed in for each level with -- representing connecting lines and the assicated feature value
uses a preorder traversal to maintain parent-child relationships
@param node - the node to be printed
"""
def print_tree(node: HeadNode | Node) -> None:
    print(node)

    for child in node.children:
        print_tree(child)



# entry point for full tree creation
def main():
    # create head node which includes all data and all features with a level of 0
    head: HeadNode = HeadNode()
    split_node(head)
    print_tree(head)


if __name__ == '__main__':
    main()