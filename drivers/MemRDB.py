# On memory simple RDBMS
#
# tuple: 

import sys
import os
from UserDefFunctions import UserDefFunctions
from lark import Lark
from partiql_lang import Build_AST

class MemRDB :
    # initialize
    def __init__(self, param):
        self.db = param
        # file is at current dir or parent dir
        grammer_file = 'partiql_grammer.lark'
        if not os.path.exists(grammer_file) :
            grammer_file = '../' + grammer_file
        rule = open(grammer_file).read()
        self.parser = Lark(rule, start="select", parser='lalr')

    # Execute partiql query
    def executeQuery(self, query):
        b = Build_AST()
        tree = self.parser.parse(query)
        ast = b.visit(tree)
        return self.execute_ast({}, ast)

    # Execute AST
    # rel: relation to apply operators for recursion (at first call, rel must be {})
    # restriction
    # * only 1 relation
    def execute_ast(self, rel, ast) :
        ret = []
        if ast[0] == 'select' :
            # get relation
            r = self.execute_ast(self.db, ast[2])
            # project relation
            ret = self.execute_ast(r, ast[1])
            # select tuples : no optimization
            if len(ast) == 4 :
                ret = self.execute_ast({'name':r['name'], 'meta':r['meta'], 'data':ret}, ast[3])
        elif ast[0] == 'from' :
            # Remark! rel means db
            # get relation name
            r_name = ast[1][2][1]
            # find relation
            ret = self.get_relation(r_name)
        elif ast[0] == 'project' :
            # get column names
            i = 0
            c_names = []
            ft_idxs = [] # position of functions in columns
            ft_results = [] # result of functions
            for c in ast[1] :
                # skip 'list'
                if i > 0 :
                    if c[0] == 'id' :
                        c_names.append(c[1])
                    if c[0] == 'path' :
                        # metadata check is not implemented
                        c_names.append(c[2][1])
                    if c[0] == 'call' :
                        ft_idxs.append(i)
                        # get relation to adapt the function
                        ii = 0
                        ft_c_names = []
                        for cc in c[2] :
                            if ii > 0 :
                                ft_c_names.append(cc[1])
                            ii = ii + 1
                        ft_rel = self.project(rel['data'], self.get_columns_index(rel['meta'], ft_c_names))
                        ft_results.append(self.execute_ast(ft_rel, c))
                i = i + 1
            # only functions case
            if len(ft_idxs) > 0 and len(c_names) == 0 :
                i = 0
                ret = ft_results[0]
                for r in ft_results :
                    if i > 0 :
                        self.insert_relation(ret, r, i)
                    i = i + 1
            # no functions case
            elif len(ft_idxs) == 0 and len(c_names) > 0 :
                ret = self.project(rel['data'], self.get_columns_index(rel['meta'], c_names))
            # function and columns are mixed
            else :              
                # execute projection
                ret = self.project(rel['data'], self.get_columns_index(rel['meta'], c_names))
                # insert function results
                j = 0
                for idx in ft_idxs :
                    ret = self.insert_relation(ret, ft_results[j], idx)
                    j = j + 1
        elif ast[0] == 'where' :
            ret = self.selection(rel, ast[1])
        elif ast[0] == 'call' :
            ret = self.call(rel, ast[1])
        
        return ret

    # insert relation to another relation at some column index (vertical union...)
    def insert_relation(self, r1, r2, idx) :
        ret = []
        i = 0
        for t1 in r1 :
            ret.append(t1[:idx] + r2[i] + t1[idx:])
            i = i + 1
        return ret

    # meta data functions
    # get column indexes from specified column names
    def get_columns_index(self, meta, col_names) :
        ret = []
        for c1 in col_names :
            i = 0
            for c2 in meta :
                if c1 == c2 :
                    ret.append(i)
                i = i + 1
        # cannot find all col_name
        if len(ret) != len(col_names) :
            print('error : column name not found', file=sys.stderr)
            sys.exit(1)
        return ret

    # get relation from specified relation name
    def get_relation(self, rel_name) :
        ret = None # None: not found
        for r in self.db :
            if r['name'] == rel_name :
                ret = r
        # cannot find relation
        if ret == None :
            print('error : relation not found', file=sys.stderr)
            sys.exit(1)
        return ret

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

    # selection operator
    # r: target relation ** with metadata **
    # cond: condition clause in AST format
    def selection(self, r, cond) :
        ret = []
        for t in r['data'] :
            if self.eval_cond(r['meta'], t, cond) :
                    ret.append(t)
        return ret
    # condition evaluation of tuple using AST
    def eval_cond(self, meta, t, ast) :
        ret = False
        if ast[0] == 'and' :
            ret = self.eval_cond(meta, t, ast[1]) and self.eval_cond(meta, t, ast[2])
            return ret
        elif ast[0] == 'or' :
            ret = self.eval_cond(meta, t, ast[1]) or self.eval_cond(meta, t, ast[2])
            return ret
        elif ast[0] == '=' :
            condition = lambda a, b : a == b
        elif ast[0] == '!=' :
            condition = lambda a, b : a != b
        elif ast[0] == '>' :
            condition = lambda a, b : a > b
        elif ast[0] == '>=' :
            condition = lambda a, b : a >= b
        elif ast[0] == '<' :
            condition = lambda a, b : a < b
        elif ast[0] == '<=' :
            condition = lambda a, b : a <= b

        c_idx = self.get_columns_index(meta, [ast[1][1]])
        # comparison two columns case
        if ast[2][0] == 'id' :
            c_idx_r = self.get_columns_index(meta, [ast[2][1]])
            ret = condition(t[c_idx[0]], t[c_idx_r[0]])
        # comparison columns and scalar
        elif ast[2][0] == 'lit' :
            ret = condition(t[c_idx[0]], ast[2][1])
        return ret

    # function call
    # specification of function
    # - parameters of the function specified in query maps to the functions's parameters
    # - function must return tuple
    def call(self, r, func) :
        ret = []
        fts = UserDefFunctions()
        for t in r :
            f = getattr(fts, func)(*t)
            ret.append(f)
        return ret