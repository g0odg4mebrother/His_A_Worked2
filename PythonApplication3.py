import random
from collections import deque
from typing import Optional, List


class Node:
    """Узел бинарного дерева"""
    def __init__(self, value: int):
        self.value = value
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None
    
    def __str__(self) -> str:
        return str(self.value)


class BinaryTree:
    """Бинарное дерево поиска"""
    def __init__(self):
        self.root: Optional[Node] = None
    
    def insert(self, value: int) -> None:
        """Вставка элемента в дерево"""
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: Node, value: int) -> None:
        """Рекурсивная вставка элемента"""
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)
    
    def delete(self, value: int) -> None:
        """Удаление элемента из дерева"""
        self.root = self._delete_recursive(self.root, value)
    
    def _delete_recursive(self, node: Optional[Node], value: int) -> Optional[Node]:
        """Рекурсивное удаление элемента"""
        if node is None:
            return None
        
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                min_node = self._find_min(node.right)
                node.value = min_node.value
                node.right = self._delete_recursive(node.right, min_node.value)
        
        return node
    
    def _find_min(self, node: Node) -> Node:
        """Находит минимальный узел в поддереве"""
        while node.left is not None:
            node = node.left
        return node
    
    def inorder(self) -> List[int]:
        """Центрированный обход (левый, корень, правый)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[Node], result: List[int]) -> None:
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def preorder(self) -> List[int]:
        """Прямой обход (корень, левый, правый)"""
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node: Optional[Node], result: List[int]) -> None:
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def postorder(self) -> List[int]:
        """Обратный обход (левый, правый, корень)"""
        result = []
        self._postorder_recursive(self.root, result)
        return result
    
    def _postorder_recursive(self, node: Optional[Node], result: List[int]) -> None:
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)
    
    def level_order(self) -> List[List[int]]:
        """Обход по уровням (ширина)"""
        if not self.root:
            return []
        
        result = []
        queue = deque([self.root])
        
        while queue:
            level_size = len(queue)
            current_level = []
            
            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.value)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(current_level)
        
        return result
    
    def max_depth(self) -> int:
        """Возвращает максимальную глубину дерева"""
        return self._max_depth_recursive(self.root)
    
    def _max_depth_recursive(self, node: Optional[Node]) -> int:
        if node is None:
            return 0
        left_depth = self._max_depth_recursive(node.left)
        right_depth = self._max_depth_recursive(node.right)
        return max(left_depth, right_depth) + 1
    
    def count_full_nodes(self) -> int:
        """Подсчитывает количество узлов, у которых есть оба потомка"""
        return self._count_full_nodes_recursive(self.root)
    
    def _count_full_nodes_recursive(self, node: Optional[Node]) -> int:
        if node is None:
            return 0
        
        count = 0
        if node.left and node.right:
            count = 1
        
        count += self._count_full_nodes_recursive(node.left)
        count += self._count_full_nodes_recursive(node.right)
        
        return count
    
    def is_symmetric(self) -> bool:
        """Проверяет, является ли дерево симметричным"""
        if not self.root:
            return True
        return self._is_mirror(self.root.left, self.root.right)
    
    def _is_mirror(self, left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        return (left.value == right.value and 
                self._is_mirror(left.left, right.right) and 
                self._is_mirror(left.right, right.left))
    
    def print_tree(self, method: str = 'inorder') -> None:
        """Вывод дерева разными способами"""
        print(f"\nДерево (обход {method}):")
        if method == 'inorder':
            print(self.inorder())
        elif method == 'preorder':
            print(self.preorder())
        elif method == 'postorder':
            print(self.postorder())
        elif method == 'level':
            levels = self.level_order()
            for i, level in enumerate(levels):
                print(f"Уровень {i}: {level}")
        else:
            print("Неизвестный метод обхода")
    
    def visualize(self) -> None:
        """Визуализация дерева в консоли"""
        if not self.root:
            print("Дерево пустое")
            return
        
        lines = []
        self._visualize_recursive(self.root, 0, 'root', lines)
        print("\nВизуализация дерева:")
        for line in lines:
            print(line)
    
    def _visualize_recursive(self, node: Optional[Node], depth: int, prefix: str, lines: List[str]) -> None:
        if node is None:
            return
        
        indent = "  " * depth
        lines.append(f"{indent}{prefix}: {node.value}")
        
        if node.left or node.right:
            if node.left:
                self._visualize_recursive(node.left, depth + 1, 'L', lines)
            else:
                lines.append(f"{indent}  L: None")
            
            if node.right:
                self._visualize_recursive(node.right, depth + 1, 'R', lines)
            else:
                lines.append(f"{indent}  R: None")

def task1():
    print("="*60)
    print("ЗАДАЧА 1: Дерево с 7 случайными числами")
    print("="*60)
    
    tree = BinaryTree()
    random_numbers = random.sample(range(1, 100), 7)
    print(f"Случайные числа: {random_numbers}")
    
    for num in random_numbers:
        tree.insert(num)
    
    tree.visualize()
    
    print("\nРазные способы обхода:")
    print(f"Центрированный (inorder): {tree.inorder()}")
    print(f"Прямой (preorder): {tree.preorder()}")
    print(f"Обратный (postorder): {tree.postorder()}")

def task2():
    print("\n" + "="*60)
    print("ЗАДАЧА 2: Дерево с заданными элементами")
    print("="*60)
    
    tree = BinaryTree()
    elements = [50, 30, 70, 20, 40, 60, 80]
    print(f"Добавляем элементы: {elements}")
    
    for elem in elements:
        tree.insert(elem)
    
    print("\nДерево по уровням:")
    levels = tree.level_order()
    for i, level in enumerate(levels):
        print(f"Уровень {i}: {level}")
    
    tree.visualize()
    
    try:
        value_to_delete = int(input("\nВведите значение элемента для удаления: "))
        tree.delete(value_to_delete)
        print(f"\nДерево после удаления {value_to_delete}:")
        levels = tree.level_order()
        for i, level in enumerate(levels):
            print(f"Уровень {i}: {level}")
        tree.visualize()
    except ValueError:
        print("Ошибка: введите целое число")

def task3():
    print("\n" + "="*60)
    print("ЗАДАЧА 3: Дерево с заданной структурой")
    print("="*60)
    
    tree = BinaryTree()
    elements = [50, 30, 60, 20, 40, 50, 70]
    print(f"Добавляем элементы: {elements}")
    
    for elem in elements:
        tree.insert(elem)
    
    print("\nСтруктура дерева:")
    print("       50")
    print("     /    \\")
    print("   30      60")
    print("  /  \\    /  \\")
    print("20    40 50   70")
    
    print("\nРеальное дерево:")
    tree.visualize()
    
    print("\nОбход по уровням:")
    levels = tree.level_order()
    for i, level in enumerate(levels):
        print(f"Уровень {i}: {level}")

def task4():
    print("\n" + "="*60)
    print("ЗАДАЧА 4: Максимальная глубина дерева")
    print("="*60)
    
    tree = BinaryTree()
    test_values = [50, 30, 70, 20, 40, 60, 80, 10, 90]
    print(f"Создаем дерево из значений: {test_values}")
    
    for value in test_values:
        tree.insert(value)
    
    tree.visualize()
    
    max_depth = tree.max_depth()
    print(f"\nМаксимальная глубина дерева: {max_depth}")

    print("\nПоиск всех листьев и их глубины:")
    leaves_info = []
    
    def find_leaves(node, depth):
        if node is None:
            return
        if node.left is None and node.right is None:
            leaves_info.append((node.value, depth))
        find_leaves(node.left, depth + 1)
        find_leaves(node.right, depth + 1)
    
    find_leaves(tree.root, 1)
    
    for value, depth in leaves_info:
        print(f"Лист {value} на глубине {depth}")
    
    deepest_leaves = [value for value, depth in leaves_info if depth == max_depth]
    print(f"Самые глубокие листья (глубина {max_depth}): {deepest_leaves}")

def task5():
    print("\n" + "="*60)
    print("ЗАДАЧА 5: Узлы с обоими потомками")
    print("="*60)
    
    tree = BinaryTree()
    test_values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    print(f"Создаем дерево из значений: {test_values}")
    
    for value in test_values:
        tree.insert(value)
    
    tree.visualize()
    
    full_nodes_count = tree.count_full_nodes()
    print(f"\nКоличество узлов с обоими потомками: {full_nodes_count}")

    full_nodes = []
    
    def find_full_nodes(node):
        if node is None:
            return
        if node.left and node.right:
            full_nodes.append(node.value)
        find_full_nodes(node.left)
        find_full_nodes(node.right)
    
    find_full_nodes(tree.root)
    print(f"Узлы с обоими потомками: {full_nodes}")

def task6():
    print("\n" + "="*60)
    print("ЗАДАЧА 6: Проверка симметричности дерева")
    print("="*60)

    print("\n1. Симметричное дерево:")
    symmetric_tree = BinaryTree()
    symmetric_tree.root = Node(1)
    symmetric_tree.root.left = Node(2)
    symmetric_tree.root.right = Node(2)
    symmetric_tree.root.left.left = Node(3)
    symmetric_tree.root.left.right = Node(4)
    symmetric_tree.root.right.left = Node(4)
    symmetric_tree.root.right.right = Node(3)
    
    symmetric_tree.visualize()
    print(f"Дерево симметрично: {symmetric_tree.is_symmetric()}")
    
    print("\n2. Несимметричное дерево:")
    asymmetric_tree = BinaryTree()
    asymmetric_tree.root = Node(50)
    asymmetric_tree.root.left = Node(30)
    asymmetric_tree.root.right = Node(60)
    asymmetric_tree.root.left.left = Node(20)
    asymmetric_tree.root.left.right = Node(40)
    asymmetric_tree.root.right.left = Node(50)
    asymmetric_tree.root.right.right = Node(70)
    
    print("       50")
    print("     /    \\")
    print("   30      60")
    print("  /  \\    /  \\")
    print("20    40 50   70")
    
    print(f"Дерево симметрично: {asymmetric_tree.is_symmetric()}")
    
    print("\n3. Еще одно несимметричное дерево:")
    tree3 = BinaryTree()
    tree3.root = Node(1)
    tree3.root.left = Node(2)
    tree3.root.right = Node(2)
    tree3.root.left.right = Node(3)
    tree3.root.right.right = Node(3)
    
    tree3.visualize()
    print(f"Дерево симметрично: {tree3.is_symmetric()}")


def main():
    """Главная функция для выполнения всех задач"""
    print("ЛАБОРАТОРНАЯ РАБОТА: БИНАРНЫЕ ДЕРЕВЬЯ")
    print("="*60)
    
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()
    
    print("\n" + "="*60)
    print("ВСЕ ЗАДАЧИ ВЫПОЛНЕНЫ!")
    print("="*60)


if __name__ == "__main__":
    main()
