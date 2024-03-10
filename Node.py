class HeadNode:
    def __init__(self, indices, remaining_features, level):
        # indices of the dataset represented in this node
        self.indices: list[int] = indices
        # features that have not already been split upon in an ancestor node
        self.remaining_features: list[str] = remaining_features
        # depth in the tree
        self.level: int = level
        # nodes representing a split of this node on the split feature
        self.children: list[Node] = []
        # feature with highest information gain of the remaining features
        self.split_feature: str | None = None
        # information gain of the top feature
        self.information_gain: float = 0.00
        # this node represents all yes's or no's
        self.is_leaf: bool = False
        # if leaf, which outcome does it represent
        self.decision: str | None = None

    def __str__(self) -> str:
        return f'{self.split_feature}: {self.information_gain}'
    
# like the head node, but it also includes the feature value it represents from the 
# split of its parent
class Node(HeadNode):
    def __init__(self, indices, remaining_features, level, feature_value):
        super().__init__(indices, remaining_features, level)
        self.feature_value = feature_value

    # printouts are done based on indention to form tree
    # tabbing is based on the level in the tree with head being level 0
    # either print the feature and IG or the value and decision it represents
    def __str__(self) -> str:
        if not self.is_leaf:
            return '\t' * (self.level) + f'-{self.feature_value}\n' + '\t' * (self.level *2) + super().__str__()
        else:
            return '\t' * (self.level * 2 - 1) + f'-{self.feature_value}\n' + '\t' * (self.level * 2) + f'{self.decision}'