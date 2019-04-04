__author__ = 'Eytan'

from random import randint

if __name__ == "__main__":
    pass

colors = [ "aquamarine", "brown", "blue1", "brown1",  \
      "chartreuse", "chocolate2", "coral3", "cornsilk",\
      "cyan1", "darkgreen", "darkorchid1", "deeppink1", \
      "darkorange", "crimson", "gold1", "deeppink4"  \
    ]
used = set([])

#you know whos the king
def get_random_color():
    if len(colors) != len(used):
        result_index = 0
        while True:
            result_index = randint(0, len(colors)-1)
            if result_index not in used:
                used.add(result_index)
                break
        return colors[result_index]
    used.clear()
    return get_random_color()
