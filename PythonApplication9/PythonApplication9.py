class Node:
    """Узел двусвязного списка"""
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


class DoublyLinkedList:
    """Двусвязный список"""
    
    def __init__(self):
        """Инициализация пустого списка"""
        self.head = None
        self.tail = None
        self._size = 0
    
    def __len__(self):
        """Возвращает количество элементов в списке"""
        return self._size
    
    def __str__(self):
        """Строковое представление списка"""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        return " <-> ".join(elements) if elements else "Пустой список"
    
    def __repr__(self):
        return f"DoublyLinkedList({self.__str__()})"
    
    def __getitem__(self, index):
        """Получение элемента по индексу через синтаксис list[index]"""
        return self.get_at_index(index)
    
    def __setitem__(self, index, value):
        """Изменение элемента по индексу через синтаксис list[index] = value"""
        self._validate_index(index)
        current = self._traverse_to_index(index)
        current.data = value
    
    def is_empty(self):
        """Проверка на пустоту списка"""
        return self._size == 0
    
    def _validate_index(self, index):
        """Проверка корректности индекса"""
        if index < 0 or index >= self._size:
            raise IndexError(f"Индекс {index} вне диапазона. Допустимый диапазон: 0-{self._size-1}")
    
    def _traverse_to_index(self, index):
        """Перемещение к узлу по указанному индексу"""
        self._validate_index(index)
        
        if index <= self._size // 2:
            current = self.head
            for _ in range(index):
                current = current.next
        else:
            current = self.tail
            for _ in range(self._size - 1 - index):
                current = current.prev
        
        return current
    
    def insert_at_beginning(self, data):
        """Вставка элемента в начало списка"""
        new_node = Node(data)
        
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        
        self._size += 1
        return self
    
    def insert_at_end(self, data):
        """Вставка элемента в конец списка"""
        new_node = Node(data)
        
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        
        self._size += 1
        return self
    
    def insert_at_index(self, index, data):
        """Вставка элемента в произвольную позицию по индексу"""
        if index == 0:
            return self.insert_at_beginning(data)
        elif index == self._size:
            return self.insert_at_end(data)
        
        self._validate_index(index) 
        new_node = Node(data)
        
        next_node = self._traverse_to_index(index)
        prev_node = next_node.prev
        
        new_node.prev = prev_node
        new_node.next = next_node
        prev_node.next = new_node
        next_node.prev = new_node
        
        self._size += 1
        return self
    
    def find_index(self, data):
        """Поиск индекса элемента по значению. Возвращает первый найденный индекс или -1"""
        current = self.head
        index = 0
        
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        
        return -1
    
    def find_all_indices(self, data):
        """Поиск всех индексов элемента по значению"""
        current = self.head
        index = 0
        indices = []
        
        while current:
            if current.data == data:
                indices.append(index)
            current = current.next
            index += 1
        
        return indices
    
    def remove_at_index(self, index):
        """Удаление элемента по индексу"""
        self._validate_index(index)
        
        if self._size == 1: 
            data = self.head.data
            self.head = self.tail = None
        elif index == 0:  
            data = self.head.data
            self.head = self.head.next
            self.head.prev = None
        elif index == self._size - 1:  
            data = self.tail.data
            self.tail = self.tail.prev
            self.tail.next = None
        else:  
            node_to_remove = self._traverse_to_index(index)
            data = node_to_remove.data
            
            prev_node = node_to_remove.prev
            next_node = node_to_remove.next
            
            prev_node.next = next_node
            next_node.prev = prev_node
        
        self._size -= 1
        return data
    
    def remove_by_value(self, data):
        """Удаление первого найденного элемента по значению. Возвращает True если удален"""
        index = self.find_index(data)
        if index != -1:
            self.remove_at_index(index)
            return True
        return False
    
    def get_at_index(self, index):
        """Получение элемента по индексу"""
        node = self._traverse_to_index(index)
        return node.data
    
    def to_list(self):
        """Преобразование списка в обычный Python list"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def from_list(self, data_list):
        """Создание списка из обычного Python list"""
        self.clear()
        for item in data_list:
            self.insert_at_end(item)
        return self
    
    def clear(self):
        """Очистка списка"""
        self.head = None
        self.tail = None
        self._size = 0
    
    def reverse(self):
        """Разворот списка"""
        current = self.head
        self.tail = self.head
        
        while current:
            temp = current.prev
            current.prev = current.next
            current.next = temp
            
            current = current.prev
        
        if self.head:
            self.head = self.head.prev
        return self
    
    def traverse_forward(self):
        """Генератор для обхода списка от начала к концу"""
        current = self.head
        while current:
            yield current.data
            current = current.next
    
    def traverse_backward(self):
        """Генератор для обхода списка от конца к началу"""
        current = self.tail
        while current:
            yield current.data
            current = current.prev


if __name__ == "__main__":
    print("=== Демонстрация работы двусвязного списка ===")
    
    dll = DoublyLinkedList()
    print(f"Создан пустой список: {dll}")
    print(f"Длина списка: {len(dll)}")
    
    print("\n1. Вставка элементов:")
    dll.insert_at_end(10)
    dll.insert_at_end(20)
    dll.insert_at_beginning(5)
    dll.insert_at_index(1, 7)
    print(f"Список после вставок: {dll}")
    print(f"Длина списка: {len(dll)}")
    
    print("\n2. Получение элементов:")
    print(f"Элемент по индексу 0: {dll.get_at_index(0)}")
    print(f"Элемент по индексу 2: {dll.get_at_index(2)}")
    print(f"Использование синтаксиса []: dll[1] = {dll[1]}")
    
    print("\n3. Поиск элементов:")
    print(f"Индекс элемента 20: {dll.find_index(20)}")
    print(f"Индекс элемента 100 (не существует): {dll.find_index(100)}")
    
    print("\n4. Изменение элемента:")
    dll[1] = 15
    print(f"После изменения dll[1] = 15: {dll}")
    
    print("\n5. Удаление элементов:")
    print(f"Удаляем элемент с индексом 2: {dll.remove_at_index(2)}")
    print(f"Список после удаления: {dll}")
    
    print("\n6. Обход списка:")
    print("От начала к концу:", list(dll.traverse_forward()))
    print("От конца к началу:", list(dll.traverse_backward()))
    
    print("\n7. Работа с разными типами данных:")
    dll2 = DoublyLinkedList()
    dll2.insert_at_end("Hello")
    dll2.insert_at_end(3.14)
    dll2.insert_at_end([1, 2, 3])
    print(f"Список с разными типами: {dll2}")
    
    print("\n8. Разворот списка:")
    print(f"Исходный список: {dll}")
    dll.reverse()
    print(f"После разворота: {dll}")
    dll.reverse()
