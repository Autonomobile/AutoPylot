class InfoParser:
    """Parse model info."""

    def __init__(self, model_info):
        self.model_info = model_info

        self.parsed = {}
        self.index_map = {"inputs": {}, "outputs": {}}
        self.parse()

        self.max_ahead = max(self.parsed.keys())

    def parse(self):
        for i, inp in enumerate(self.model_info["inputs"]):
            if "." in inp[0]:
                name, idx = inp[0].split(".")
                idx = int(idx)
            else:
                name = inp[0]
                idx = 0

            if idx not in self.parsed.keys():
                self.parsed[idx] = {"inputs": [name], "outputs": []}
            else:
                self.parsed[idx]["inputs"].append(name)

        for i, out in enumerate(self.model_info["outputs"]):
            if "." in out[0]:
                name, idx = out[0].split(".")
                idx = int(idx)
            else:
                name = out[0]
                idx = 0

            if idx not in self.parsed.keys():
                self.parsed[idx] = {"outputs": [name], "inputs": []}
            else:
                self.parsed[idx]["outputs"].append(name)

        self.index_map["inputs"] = _get_map(self.model_info["inputs"])
        self.index_map["outputs"] = _get_map(self.model_info["outputs"])


def _get_map(inpouts):
    """Get index map from alphabetic order to chronological order."""
    to_sort = []
    for i, inpout in enumerate(inpouts):
        if "." in inpout[0]:
            name, idx = inpout[0].split(".")
            idx = int(idx)
        else:
            name = inpout[0]
            idx = 0
        to_sort.append((idx, name))

    sorted_items = sorted(to_sort)

    idx_map = {}
    for i, item in enumerate(sorted_items):
        idx_before_sort = to_sort.index(item)
        idx_map[i] = idx_before_sort
    return idx_map
