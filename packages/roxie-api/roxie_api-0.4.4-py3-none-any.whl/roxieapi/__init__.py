# version as tuple for simple comparisons
VERSION = (0, 0, 15)
# string created from tuple to avoid inconsistency
__version__ = "0.4.4".join([str(x) for x in VERSION])
