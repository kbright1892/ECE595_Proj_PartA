class HeadNode:
    def __init__(self, indices, remaining_features, level):
        self.indices: list[int] = indices
        self.remaining_features: list[str] = remaining_features
        self.level: int = level
        self.children: list[Node] = []
        self.split_feature: str | None = None
        self.information_gain: float = 0.00
        self.is_leaf: bool = False
        self.decision: str | None = None

    def __str__(self) -> str:
        return f'{self.split_feature}: {self.information_gain}'
    

class Node(HeadNode):
    def __init__(self, indices, remaining_features, level, feature_value):
        super().__init__(indices, remaining_features, level)
        self.feature_value = feature_value

    def __str__(self) -> str:
        if not self.is_leaf:
            return '\t' * (self.level - 1) + f'-{self.feature_value}\n' + '\t' * self.level + super().__str__()
        elif self.is_leaf and self.level == 1:
            return f'-{self.feature_value}\n\t{self.decision}'
        else:
            return '\t' * self.level + f'{self.feature_value}: {self.decision}'