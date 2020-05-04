# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION


# Assignments to a CircularList object will only involve integer indexes.
#
# When the index is an integer, it is interpreted modulo the length
# of the list.
#
# When working with slices:
# - The last argument of a slice cannot be equal to 0.
# - When the last argument of a slice is not given, it is set to 1.
# - When the first argument of a slice is not given, it is set to
#   0 or to -1 depending on the sign of the last argument.
# - When the second argument of a slice is not given, it is set to
#   len(list) or to -len(list) -1 depending on the sign of the last argument.
# - Denoting by L the CircularList object, returns a list consisting of
#   all elements of the form L[i modulo len(L)] for i ranging between first
#   (included) and second (excluded) arguments of slice, in steps given by
#   third argument of slice.

class CircularList:
    def __init__(self, *args):
        self.circular_list = [element for element in args]

    def __str__(self):
        # Convert elements to string then output
        output = [str(x).replace("'", '') for x in self.circular_list]
        output_string = '[' + ', '.join(output) + ']'
        return output_string

    def __len__(self):
        return len(self.circular_list)

    def __setitem__(self, key, value):
        self.circular_list[key % len(self.circular_list)] = value

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.circular_list[item % len(self.circular_list)]

        elif isinstance(item, slice):
            start, stop, step = item.start, item.stop, item.step
            if step == 0:
                raise ValueError('slice step cannot be zero')
            elif step is None:
                step = 1

            if start is None:
                if step > 0:
                    start = 0
                else:
                    start = -1

            if stop is None:
                if step > 0:
                    stop = len(self.circular_list)
                else:
                    stop = -len(self.circular_list) - 1

            circular_list_slice = [self.circular_list[i % len(self.circular_list)] for i in range(start, stop, step)]
            return circular_list_slice

