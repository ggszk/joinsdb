#
# Virtual database
# 
# * now only support one MemRDB

import sys
import os
from lark import Lark
from partiql_lang import Build_AST
from MemRDB import MemRDB
from Neo4j import Neo4j

class VirtualDB :
    # initialize
    def __init__(self, param):
        # load grammer
        # ** Remark! ** dupliated loading
        # file is at current dir or parent dir
        grammer_file = 'partiql_grammer.lark'
        if not os.path.exists(grammer_file) :
            grammer_file = '../' + grammer_file
        rule = open(grammer_file).read()
        self.parser = Lark(rule, start="select", parser='lalr')
        # parameter
        self.db = param['db']
        self.con = []
        # connect to all databases
        for d in self.db :
            if d['type'] == 'MemRDB' :
                self.con.append(MemRDB(d['connect']))
            elif d['type'] == 'Neo4j' :
                self.con.append(Neo4j(d['connect']))

    # Execute partiql query
    def executeQuery(self, query):
        b = Build_AST()
        tree = self.parser.parse(query)
        ast = b.visit(tree)
        # find db and table to access (only 1 table in 1 DB)
        tbl_in_query = ast[2][1][2][1]
        r = self.find_table(self.db, tbl_in_query)
        db_idx = r[0]
        local_name = r[1]
        # ast rewrite by local table name
        # execute ast
        return self.con[db_idx].execute_ast({}, ast)

    # find table
    def find_table(self, dbs, table_name) :
        db_idx = 0
        local_name = None
        for db in dbs :
            for t in db['table'] :
                if t['name'] == table_name :
                    local_name = t['local_name']
                    return (db_idx, local_name)
            db_idx = db_idx + 1


