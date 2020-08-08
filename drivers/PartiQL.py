#
# PartiQL data model database
#
# * PartiQL data model is represented by Python data structure
# * bag is not supported

import sys
import os
from lark import Lark
from partiql_lang import Build_AST

class PartiQL :
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
        print(ast)
        ret = []
        if ast[0] == 'select' :
            # get relation
            r = self.execute_ast(self.db, ast[2])
            # select tuples : no optimization
            if len(ast) == 4 :
                r = self.execute_ast(r, ast[3])
            # project relation
            ret = self.execute_ast(r, ast[1])
        elif ast[0] == 'from' :
            # Remark! rel means db
            # get relation path (or id)
            r_path = ast[1][2]
            # find relation
            ret = self.get_relation(self.db, r_path)
        elif ast[0] == 'project' :
            # get column names
            i = 0
            c_names = []
            for c in ast[1] :
                # skip 'list'
                if i > 0 :
                    if c[0] == 'id' :
                        c_names.append(c[1])
                    if c[0] == 'path' :
                        # metadata check is not implemented
                        c_names.append(c[2][1])
                i = i + 1
            ret = self.project(rel, c_names)
        elif ast[0] == 'where' :
            ret = self.selection(rel, ast[1])
        return ret

    # find object(strucrured relation) by specifed key(relation name) recursively
    def get_relation(self, rel, rel_path) :
        # no path expression
        if rel_path[0] == 'id' :
            rel_name = rel_path[1]
        elif rel_path[0] == 'path' :
            child_rel = rel
            for id in rel_path[1:] :
                # found (name match)
                if id[1] in child_rel.keys() :
                    child_rel = child_rel[id[1]]
                # not found
                else :
                    return None
            return child_rel

    # projection operator
    # r: target relation
    # c_names : names of projected columns
    def project(self, r, c_names) :
        result = []
        for t in r :
            result_obj = {}
            for c in c_names :
                result_obj[c] = t[c]
            result.append(result_obj)
        return result

    # selection operator
    # r: target relation ** with metadata **
    # cond: condition clause in AST format
    def selection(self, r, cond) :
        ret = []
        for t in r :
            if self.eval_cond(t, cond) :
                    ret.append(t)
        return ret
    # condition evaluation of tuple using AST
    def eval_cond(self, t, ast) :
        ret = False
        if ast[0] == 'and' :
            ret = self.eval_cond(t, ast[1]) and self.eval_cond(t, ast[2])
            return ret
        elif ast[0] == 'or' :
            ret = self.eval_cond(t, ast[1]) or self.eval_cond(t, ast[2])
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

        # comparison two columns case
        if ast[2][0] == 'id' :
            ret = condition(t[ast[1][1]], t[ast[2][1]])
        # comparison columns and scalar
        elif ast[2][0] == 'lit' :
            ret = condition(t[ast[1][1]], ast[2][1])
        return ret
