# -*- coding: utf-8 -*-
class Stack(object):
    def __init__(self):
        self.arr = []

    @property
    def empty(self):
        return len(self.arr) == 0

    @property
    def top(self):
        return self.arr[-1]

    def push(self, x):
        self.arr.append(x)

    def pop(self):
        return self.arr.pop()


class Counter(object):
    def __init__(self, length):
        assert length > 0
        self.length = length
        self.head = None
        self.tail = None
        self.digits_2 = Stack()
        self.insert_zeros()

    def __int__(self):
        base = 1
        result = 0
        node = self.head
        while node is not None:
            result += node.value * base
            base *= 2
            node = node.next
        return result

    def __str__(self):
        digits = []
        node = self.head
        while node is not None:
            digits.insert(0, str(node.value))
            node = node.next
        return "".join(digits)

    def __unicode__(self):
        return unicode(self)

    def insert_zeros(self):
        node = ListNode(0)
        self.head = self.tail = node

        i = self.length - 1
        while i > 0:
            next_node = ListNode(0)
            node.next = next_node
            node = node.next
            i -= 1

        self.tail = node

    def increment(self):
        if not self.digits_2.empty:
            rightmost_2 = self.digits_2.pop()
            rightmost_2.value = 0
            rightmost_2.next.value += 1
            if rightmost_2.next != self.tail and rightmost_2.next.value == 2:
                self.digits_2.push(rightmost_2.next)
        if self.head.value == 0:
            self.head.value = 1
        else:
            self.head.value = 2
            self.digits_2.push(self.head)


class ListNode(object):
    def __init__(self, x):
        self.next = None
        self.value = x


def main():
    c = Counter(10)
    i = 0
    while i <= 1024:
        print("{:s} ({:d})".format(c, i))
        if int(c) != i:
            raise ValueError("{:s} is not {:d}".format(c, i))
        c.increment()
        i += 1

if __name__ == '__main__':
    main()
