
class CMAESVarSet:
    def __init__(self, index_ref):
        """
        Expects a dictionary of the form [str : tuple], where the ith key is the name of the variable being controlled by the ith bounds
        and the tuple is the (min, max) bounds for the variable.
        """
        self.named_dict = index_ref
        self.names = [k for k in index_ref]
        self.min_set = [v[0] for v in index_ref.values()]
        self.max_set = [v[1] for v in index_ref.values()]

    def __len__(self):
        return len(self.named_dict)

    def from_normalized_to_scaled(self, vector):
        out = []
        for i, elem in enumerate(vector):
            out.append(self.lerp(elem, self.min_set[i], self.max_set[i]))
        return out

    def as_dict(self):
        return self.named_dict

    @staticmethod
    def lerp(x, _min, _max):
        return (x * (_max - _min)) + _min
