# README

## Data

### data.py

- The file has no dependencies
- This file contains the data from the table in the project description in three dictionaries
  - The features dictionary contains the headers for the data columns. The feature name maps to the index of the feature value in each entry in the data dictionary
  - The data dictionary contains the values for each feature for each row of the table, indexed starting at 1
  - The outcomes dictionary has the outcomes for each row in the table
- This allows data to be split at each level without having to recreate full subsets of the data. Only the indices are necessary for referencing the data.

## Classes

### Node (Node.py)

- The file is dependent on data.py
- Contains definitions for two different classes of Node: Head node and Node
- Both nodes represent nodes on a tree
  - HeadNode - the top node of a tree
    - The head node automatically initializes its indices and remaining features with all data rows and features from the original datases
    - Its level is set to 0
  - Node - inner or leaf nodes of a tree. It is the same as a head node but also has a variable that stores which value of the feature the parent node was split upon which the node represents. For example, if the parent was split on Temperature, it would store whether it represents remaining data rows with the value of Hot, Mild, or Cool
- Both node types store the following information
  - Indices
    - In the parent node, it contains the indices of all rows of data in the original dataset
    - In inner and leaf nodes, it contains the subset of the parent node's indices that have the value of the parent's split feature that the node represents.
  - Remaining features - the indices of features in the dataset that have not been split upon by a parent node
  - Level - the node's depth in the tree, which is used for printing the tree
  - Sorted features - the remaining features and their information gains, sorted in descending value by IG
  - Is Leaf - a boolean that is true if all remaining data indices have the same outcome and false otherwise
  - Decision - if the node is a leaf, this is "yes" or "no", otherwise it is None
- Each node also has a string method for use with the print() function that prints its information, with proper indention, based on its level in the tree

## Entry Points

### feature_rank.py

- This is the entry point for Part 1 of the project
- It depends on data.py and helpers.py
- It creates 2 lists:
  1. A list of row indices from the keys of the data dictionary
  2. A list of features from the keys of the feature dictionary
- It calls the rank_features method from helpers.py, which returns the features and their information gains.
  - The second return value of rank_features is not used
- The sorted list of features is then printed to the screen

### create_tree.py

- This is the entry point for Part 2 of the project
- It depends on data.py, helpers.py, and Node.py

#### main()

- This creates a HeadNode
- It then passes the HeadNode to split_node(), which is a recursive function.
- It then passes the HeadNode to print_tree(), which is a recursive function.

#### split_node()

- Take a node as the only parameter
- It makes a copy of the node's remanining features, as the list of features will be modified before creating child nodes, but the original list should not be modified
  - Since Python is pass by reference, this step is necessary, or a modification to the list will affect its use everywhere
- rank_features() is then called to get the entropy of the passed node and the list of remaining features, sorted by information gain
  - If any of the features has all "yes" or "no" outcomes, a decision is returned. Otherwise, decision is None
  - If there is a decision, the recursive calls stop at that level, the node is marked as a leaf, and the decision is saved
- The sorted features are saved to the node, and the top ranked feature is removed from the copied list of remaining features.
- The data rows represented in the node's indices are then split, based on their value for the top feature
  - These indices are stored in a dictionary with the feature value as the key and a list of indices with that value as the values
- The dictionary for each feature value is used to create a Node for each of these values
- Split node is called again for the new node, and the node is added to the original node's children

#### print_tree()

- Take a node as the only parameter
- This is a recursive function that performs a preorder traversal, resulting in a printed tree with proper parent-child alignment

## Helper Methods

### helpers.py

#### calculate_entropy()

- Takes two integers, the count of positive outcomes and the count of negative outcomes, as the parameters
- It returns the entropy, based on these counts, as a float

#### calculate_information_gain()

- Takes a subset of row indices, a feature name, and the entropy of the full subset as parameters
- Returns the information gain of the passed feature, based on the subset of row indices
- It iterates through all indices in the subset and calculates the number or positive and negative outcomes for each feature value
- For each feature value, it calls calculate_entropy() to get the entropy for that feature value
- It then caluculates the sum of the weighted entropies for each feature value
- The sum is subtracted from the original entropy, equalling the information gain
- The information gain for the feature is returned

#### rank_features()

- Takes a subset of row indices and a list of remaining features as parameters
- Returns a 3-tuple
  - List of lists of [feature, feature information gain]
  - A decision, yes or no, if this will be a leaf
  - The entropy of the subset of rows
- It calculates the number of positive and negative outcomes for the subset of rows and calls calculate_entropy() to get the entropy of the subset
  - If there is only one remaining feature, it returns a decision based on the count of positive and negative outcomes
    - Incase of a tie, it uses the counts of positive and negative outcomes of the original full dataset
      - If that is a tie, it defaults to a positive outcome
- If there is more than one remaining feature, it calls calculate_information_gain() for each remaining features and captures the values
- It then sorts them by information gain in descending order
- It returs the sorted list, no decision, and the entropy of the full subset
  - The subset entropy is only used for the print function after the information gains have been calculated

## Overall Flow

### Part 1

- The main() function of rank_features.py calls rank_features(), which returns the sorted list of features by information gain
  - The other two return values are not used in this part
- rank_features() calls calculate_entropy() for the original dataset
- It then calls calculate_information_gain() for each features in the original dataset
- Calculate_information_gain() calls calculate_entropy() with the outcomes of each feature value and calculates the sum of the weighted entropies for each value
  - It then calculates the information gain for each feature
- rank_features() takes the results from each feature and sorts them in descending order by information gain
- The sorted list is returned to the main() of rank_features.py adn printed to the screen in a formatted manner

### Part 2

- Part 2 starts in create_tree.py
- It uses nodes to compose a tree, built in a depth-first manner
- main() creates a HeadNode and then calls split_node()
- split_node() is a recursive function that starts similar to Part 1, but when the ranked features are returned, it removes the top ranked feature and creates child nodes
- Child nodes are created for each value of the top ranked feature
  - The get the subset of nodes that have their value for the top feature
- Once a child node is created, split_node() is called on that node
- split_node() continues recursive calls until a leaf node is found
- Once split_node() returns back to the head node and completes its calls on all of its children, script returns to main()
- main() calls print_node() with the head node as the parameter
- print_node() is another recursive function that does a pre-order traversal of the tree, calling print() on each node to print the tree
  - Each node has a string method that prints it's information
  - The result is a tree that maintains parent-child relationships, with levels of the tree represented by levels of indentation
  - Each non-leaf node prints its entropy, the information gain of the best feature, and the information gain of the other features
