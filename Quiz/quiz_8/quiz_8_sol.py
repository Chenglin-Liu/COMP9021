# Written by Eric Martin for COMP9021


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
        self._L = list(args)

    def __len__(self):
        return len(self._L)

    def __getitem__(self, index_or_slice):
        if type(index_or_slice) is int:
            return self._L[index_or_slice % len(self)]
        if type(index_or_slice) is slice:
            if index_or_slice.step is not None:
                if index_or_slice.step == 0:
                    raise ValueError('slice step cannot be zero')
                step = index_or_slice.step
            else:
                step = 1
            if index_or_slice.start is not None:
                start = index_or_slice.start
            else:
                start = 0 if step > 0 else -1
            if index_or_slice.stop is not None:
                stop = index_or_slice.stop
            else:
                stop = len(self._L) if step > 0 else -len(self._L) - 1
            return list(self._L[i % len(self._L)]
                            for i in range(start, stop, step)
                       )

    def __setitem__(self, index, value):
        self._L[index % len(self)] = value

    def __str__(self):
        return '[' + ', '.join(str(e) for e in self._L) + ']'

    def __repr__(self):
        return self.__str__()

