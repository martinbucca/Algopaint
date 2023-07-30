class _Node:
    def __init__(self, element, next=None):
        self.element = element
        self.next = next


class Stack:
    def __init__(self):
        self.top = None

    def push(self, element):
        self.top = _Node(element, self.top)

    def pop(self):
        popped_element = self.top.element
        self.top = self.top.next
        return popped_element

    def get_top(self):
        return self.top.element

    def empty(self):
        return self.top is None

    def clear(self):
        while not self.empty():
            self.pop()
