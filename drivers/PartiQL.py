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
        ret = []
        if ast[0] == 'select' :
            # get relation
            r = self.execute_ast(self.db, ast[2])
            # project relation
            ret = self.execute_ast(r, ast[1])
            # select tuples : no optimization
            if len(ast) == 4 :
                ret = self.execute_ast(ret, ast[3])
        elif ast[0] == 'from' :
            # Remark! rel means db
            # get relation name
            r_name = ast[1][2][1]
            # find relation
            ret = self.get_relation(self.db, r_name)
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
    def get_relation(self, rel, rel_name) :
        ret = {}
        for key in rel.keys() :
            if key == rel_name :
                ret = rel[key]
            # not found : rel is not dict but list
            elif type(rel[key]) == list :
                ret = None
            # find in child tree
            else :
                ret = self.get_relation(rel[key], rel_name)
        return ret

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

db = {
    'hr': {
        'employees': [
            { 'id': 3, 'name': 'Bob_Smith',   'title': None }, 
            { 'id': 4, 'name': 'Susan_Smith', 'title': 'Dev Mgr' },
            { 'id': 6, 'name': 'Jane_Smith',  'title': 'Software Eng 2'}
        ]
    }
}

pdb = PartiQL(db)
print(pdb.get_relation(db, 'hr'))
r = db['hr']['employees']
print(pdb.project(r, ['name', 'title']))
print(pdb.selection(r, ['=', ['id', 'id'], ['lit', 4]]))
print(pdb.executeQuery("SELECT name FROM employees"))
print(pdb.executeQuery("SELECT id FROM employees WHERE id = 3"))

