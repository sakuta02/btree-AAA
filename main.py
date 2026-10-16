import sys

sys.setrecursionlimit(10000)

NOT_FOUND = 'None'

def h(n):
    return n.h if n else 0

class Node:
    def __init__(self, x):
        self.key = x
        self.left = None
        self.right = None
        self.h = 1

    def _upd(self):
        self.h = 1 + max(h(self.left), h(self.right))

    def _bal(self):
        return h(self.right) - h(self.left)

    def _rot_left(self):
        b = self.right
        self.right = b.left
        b.left = self
        self._upd()
        b._upd()
        return b

    def _rot_right(self):
        b = self.left
        self.left = b.right
        b.right = self
        self._upd()
        b._upd()
        return b

    def _rebalance(self):
        self._upd()
        if self._bal() == 2:
            if self.right._bal() < 0:
                self.right = self.right._rot_right()
            return self._rot_left()
        if self._bal() == -2:
            if self.left._bal() > 0:
                self.left = self.left._rot_left()
            return self._rot_right()
        return self

    def add(self, x: int):
        if x > self.key:
            self.right = self.right.add(x) if self.right else Node(x)
        elif x < self.key:
            self.left = self.left.add(x) if self.left else Node(x)
        return self._rebalance()

    def _min(self):
        if self.left:
            return self.left._min()
        return self.key

    def _del(self, x: int):
        if self.key < x:
            if self.right:
                self.right = self.right._del(x)
        elif self.key > x:
            if self.left:
                self.left = self.left._del(x)
        else:
            if not self.left:
                return self.right
            if not self.right:
                return self.left
            k = self.right._min()
            self.right = self.right._del(k)
            self.key = k
        return self._rebalance()

    def exists(self, x):
        if self.key < x and self.right:
            return self.right.exists(x)
        elif self.key < x:
            return False

        if self.key > x and self.left:
            return self.left.exists(x)
        elif self.key > x:
            return False

        return True

    def next(self, x):
        best = None
        n = self
        while n:
            if n.key >= x:
                best = n.key
                n = n.left
            else:
                n = n.right
        return best

    def prev(self, x):
        best = None
        n = self
        while n:
            if n.key <= x:
                best = n.key
                n = n.right
            else:
                n = n.left
        return best

    def print(self):
        res = [self.key]
        if self.left:
            res.extend(self.left.print())
        if self.right:
            res.extend(self.right.print())
        return res


if __name__ == '__main__':
    root = None
    n = int(input())
    for _ in range(n):
        l = input().split()
        if len(l) == 1:
            c = l[0]
            if c == 'height':
                print(h(root))
            if c == 'root':
                print(root.key if root else 'Empty')
            if c == 'print':
                if root:
                    print(*root.print())
                else:
                    print('Empty')
        else:
            c, a = l
            a = int(a)
            if c == 'add':
                root = root.add(a) if root else Node(a)
            if c == 'del':
                if root:
                    root = root._del(a)
            if c == 'exists':
                print('YES' if root and root.exists(a) else 'NO')
            if c == 'next':
                r = root.next(a) if root else None
                print(NOT_FOUND if r is None else r)
            if c == 'prev':
                r = root.prev(a) if root else None
                print(NOT_FOUND if r is None else r)