# JoinsDB: Simple poly-dbms for experimental and educational purpose

## Target storage engine

* On memory graph
* Simple graph database: built on Neo4j but only has the ability to get adjecent nodes
  * for experiment of distributed graph algorithm...
* Neo4j
* SQLite

## Now implemented

* Wrappers of the target storage engines (SQL and Cypher execution).
* Dijkstra search on memory graph and on simple graph database
* Simple trip planning query: find path throgh one point of interest (poi)
* Simple trip planning query on Neo4j + SQLite

## Will be implemented

* Unified query interface using PartiQL
* Query across to heterogeneous databases
* Trip planning query on distributed environment

## Usage

* Please read example.py and tests in the test folder

## Sample database

* Neo4j: Please execute ./test/sample_db.cypher on Neo4j browser
* SQLite: Please execute ./test/sample_db.sql in SQLite3
