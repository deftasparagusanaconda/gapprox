# a dictionary that performs lookup on a key by its id, instead of its hash
# 
# AI-generated btw, because i couldnt be bothered to care about details like these.

class IdentityDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._id_map = {}
        if args:
            d = dict(*args)
            for k, v in d.items():
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def __setitem__(self, key, value):
        super().__setitem__(id(key), value)
        self._id_map[id(key)] = key  # store original key for iteration

    def __getitem__(self, key):
        return super().__getitem__(id(key))

    def __delitem__(self, key):
        super().__delitem__(id(key))
        del self._id_map[id(key)]

    def __contains__(self, key):
        return super().__contains__(id(key))

    def get(self, key, default=None):
        return super().get(id(key), default)

    def keys(self):
        return self._id_map.values()

    def items(self):
        return ((k, self[k]) for k in self._id_map.values())

    def values(self):
        return (self[k] for k in self._id_map.values())
