# JoinsDB: Simple poly-dbms for experimental and educational purpose

## Target storage engine

* On memory graph
* Simple graph database: built on Neo4j but only has the ability to get adjecent nodes
  * for experiment of distributed graph algorithm...
* Neo4j

## Now implemented

* Dijkstra search on memory graph and on simple graph database
* JoinsDB is (only) wrapper of the target storage engines.

## Will be implemented

* Query across to heterogeneous databases
* Trip plannning query on distributed environment

## Usage

* Please read example.py

## Sample Neo4j database

* Please execute ./test/sample_db.cypher on Neo4j browser
