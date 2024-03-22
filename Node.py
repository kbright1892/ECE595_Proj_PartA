from data import features, data


"""
a head node is the top node on a decision tree. It is at level 0 and doesn't represent a 
particular feature, but rather the entire dataset and it's features list contains all features, 
as none have been removed for a prior split
"""
class HeadNode:
    def __init__(self, indices: list = list(data.keys()), remaining_features: list = list(features.keys()), level: int = 0):
        # indices of the dataset represented in this node
        self.indices: list[int] = indices
        # features that have not already been split upon in an ancestor node
        self.remaining_features: list[str] = remaining_features.copy()
        # depth in the tree
        self.level: int = level
        # entropy of current node
        self.entropy: int = 0
        # nodes representing a split of this node on the split feature
        self.children: list[Node] = []
        # all of the remaining features, sorted by information gain
        self.sorted_features: list[list[str, float]] = []
        # this node represents all yes's or no's
        self.is_leaf: bool = False
        # if leaf, which outcome does it represent
        self.decision: str | None = None


    def __str__(self) -> str:
        full_string = f'Entropy: {self.entropy}\n' + '\t' * (self.level *2) + f'Best - {self.sorted_features[0][0]}: {self.sorted_features[0][1]}\n' + '\t' * (self.level *2) +  'Others - '

        for feature in self.sorted_features[1:]:
            full_string += f'{feature[0]}: {feature[1]}, '

        full_string = full_string[:-2]

        # create a string of the top feature and its information gain
        return full_string
    

"""
like the head node, but it also includes the feature value it represents from the split of its parent
"""
class Node(HeadNode):
    def __init__(self, indices: list, remaining_features: list, level: int, feature_value: str):
        super().__init__(indices, remaining_features, level)
        self.feature_value = feature_value


    # printouts are done based on indention to form tree
    # tabbing is based on the level in the tree with head being level 0
    # either print the feature and IG or the value and decision it represents
    def __str__(self) -> str:
        if not self.is_leaf:
            # create string of the feature the node represents and the outcome
            return '\t' * (self.level) + f'\\_{self.feature_value}_\n' + '\t' * (self.level * 2 - 1) + ' ' * (len(self.feature_value) + 3 ) + '\\ \n' + '\t' * (self.level *2) + super().__str__()
        else:
            # create a string of hte feature the node represents and the information gain of the top remaining feaure
            return '\t' * (self.level * 2 - 1) + f'\\_{self.feature_value}_\n' + '\t' * (self.level * 2 - 1) + ' ' * (len(self.feature_value) + 3 ) + '\\ \n' + '\t' * (self.level * 2) + ' ' * (len(self.feature_value) - 4 if len(self.feature_value) > 4 else 0)  + f'{self.decision}\n'