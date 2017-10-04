import sys

class Trie(object):
    def __init__(self):
        self.children = {}
        self.terminal = False

    def add_candidate(self, candidate):
        if not self.is_subsumed(candidate):
            self.remove_subsumed(candidate)
            self.add(candidate)

    def add(self, candidate, pos=0):
        if pos == len(candidate):
            self.terminal = True
        else:
            component = candidate[pos]

            if component in self.children:
                child = self.children[component]
            else:
                child = Trie()
                self.children[component] = child

            child.add(candidate, pos+1)

    def is_subsumed(self, candidate, pos=0):
        if self.terminal:
            return True

        for i in range(pos, len(candidate)):
            component = candidate[i]

            child = self.children.get(component)
            if child is not None:
                if child.is_subsumed(candidate, i+1):
                    return True
        return False

    def remove_subsumed(self, candidate, pos=0):
        if not candidate:
            self.children.clear()
            self.terminal = True
            return True

        if pos == len(candidate):
            self.terminal = False
            return True

        component = candidate[pos]
        remove = []

        for key in self.children:
            i = pos

            if key > component:
                continue
            elif key == component:
                i += 1

            if self.children[key].remove_subsumed(candidate, i):
                remove.append(key)

        for key in remove:
            del self.children[key]

        return not self.terminal and len(self.children) == 0

    def __iter__(self, candidate=[]):
        if self.terminal:
            yield candidate
        else:
            for component, child in self.children.items():
                for new_candidate in child.__iter__(candidate + [component]):
                    yield new_candidate

    def print_trie(self, out=sys.stdout, padding="", value=None):
        if value:
            print("%s%d(%s)" % (padding, value, self.terminal))
        else:
            print("%s(%s)" % (padding, self.terminal))
        for child in self.children:
                self.children[child].print_trie(out=out, padding=padding+"--",
                                                value=child)
