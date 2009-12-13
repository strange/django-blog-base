tests = """
>>> assert(True == False)

>>> fsdfsadfasd

"""

__test__ = { 'doctest': tests }

if __name__ == '__main__':
    import doctest
    doctest.testmod()
