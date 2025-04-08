class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            tail = self.head.prev

            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

    def remove_alarm(self, data):
        if not self.head:
            return

        current = self.head
        while True:
            if current.data == data:
                if current == self.head and current.next == self.head:
                    self.head = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    if current == self.head:
                        self.head = current.next
                return
            current = current.next
            if current == self.head:
                break

    def to_list(self):
        result = []
        if not self.head:
            return result

        current = self.head
        while True:
            result.append(current.data)
            current = current.next
            if current == self.head:
                break
        return result
