# On memory simple RDBMS
#
# tuple: 

import sys

class MemRDB :
    # initialize
    def __init__(self, param):
        self.db = param

    # Execute partiql query
    def executeQuery(self, sql):
        result = []
        return result

    # join operator
    # r1, r2: target relations
    # index : index of join key. for example (1, 2) means key of t1 is 1, and key of t2 is 2 
    # operator : comparison operator for comparing keys: now only "eq"(=) is supported
    def join(self, r1, r2, index, operator) :
        # operator check
        if operator != "eq" :
            print('error :sorry, only equi join is supported', file=sys.stderr)
            sys.exit(1)

        # Nested loop join
        result = []
        for t1 in r1 :
            for t2 in r2 :
                if t1[index[0]] == t2[index[1]] :
                    result.append(t1 + t2)
        return result

    # projection operator
    # r: target relation
    # index : index of projected columns
    def project(self, r, index) :
        result = []
        for t in r :
            result_tuple = ()
            for idx in index :
                result_tuple = result_tuple + t[idx:idx+1]
            result.append(result_tuple)
        return result

    # function call
    # specification of function
    # - parameters of the function specified in query maps to the functions's parameters
    # - function must return tuple
    def call(self, r, func) :
        ret = []
        for t in r :
            f = getattr(self, func)(*t)
            ret.append(f)
        return ret

    # function examples
    # example: "select add('col1', 'col2') from r" return col1 + col2
    # example: "select add('col1', 3) from r" return col1 + 3
    def add(self, col1, col2) :
        return (col1 + col2,)

    # multiple constant to a one column
    # example: "select multiple('col1', 5) from r" return col1 * 5
    def multiple(self, col1, col2) :
        return (col1*col2,)