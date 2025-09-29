class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        print(f"\n>>> insert({key})")
        if self.root is None:
            self.root = Node(key)
            print(f"Root is None -> created Node({key}) as root")
        else:
            self._insert_recursively(self.root, key, depth=0)

    def _insert_recursively(self, current_node, key, depth):
        indent = "  " * depth
        print(f"{indent}At Node({current_node.key}), inserting {key}")

        if key < current_node.key:
            print(f"{indent}{key} < {current_node.key} -> go LEFT")
            if current_node.left is None:
                current_node.left = Node(key)
                print(f"{indent}Created Node({key}) as LEFT child of Node({current_node.key})")
            else:
                self._insert_recursively(current_node.left, key, depth + 1)

        elif key > current_node.key:
            print(f"{indent}{key} > {current_node.key} -> go RIGHT")
            if current_node.right is None:
                current_node.right = Node(key)
                print(f"{indent}Created Node({key}) as RIGHT child of Node({current_node.key})")
            else:
                self._insert_recursively(current_node.right, key, depth + 1)

        else:
            print(f"{indent}{key} already exists -> ignore")

    def search(self, key):
        print(f"\n>>> search({key})")
        return self._search_recursively(self.root, key, depth=0)

    def _search_recursively(self, current_node, key, depth):
        indent = "  " * depth
        if current_node is None:
            print(f"{indent} Reached None -> {key} NOT FOUND")
            return None

        print(f"{indent}At Node({current_node.key}), searching for {key}")

        if current_node.key == key:
            print(f"{indent} Found {key} at Node({current_node.key})")
            return current_node.key
        elif key < current_node.key:
            print(f"{indent}{key} < {current_node.key} -> go LEFT")
            return self._search_recursively(current_node.left, key, depth + 1)
        else:
            print(f"{indent}{key} > {current_node.key} -> go RIGHT")
            return self._search_recursively(current_node.right, key, depth + 1)


if __name__ == "__main__":
    bst = BinarySearchTree()
    numbers = [10, 5, 15, 3, 7]
    for number in numbers:
        bst.insert(number)

    print("\n--- SEARCH DEMO ---")
    print("Result:", bst.search(7))  
    print("Result:", bst.search(4)) 
