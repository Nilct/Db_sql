#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import sys, getopt


def loadSirenDataFromCSV(filename = "../data/siren_93.csv"):
    print("Read Siren data")
    df = pd.read_csv(filename, sep=';', encoding='latin-1')
    newDf = df.loc[:,["siren", "nic", "l1_normalisee", "l1_declaree", "numvoie", "indrep", "typvoie", "libvoie", "codpos", "libnatetab", "libapet"]]
    newDf["numvoie"] = pd.to_numeric(newDf["numvoie"], errors='coerce')
    return newDf

def saveSirenDataIntoDatabase(newDf):
    print("Save Siren data into database")
    engine = create_engine('postgresql:///bigdata')
    newDf.to_sql("SIREN", engine, if_exists='replace')

def loadBanoDataFromCSV(filename = "../data/bano_93.csv"):
    print("Read Bano data")
    df = pd.read_csv(filename, sep=';', encoding='latin-1')
    newDf = df.iloc[:,[1, 2, 3, 4, 6, 7]]
    newDf.columns = ['numero', 'voie', 'code_post', 'nom_comm', 'lat', 'lon']
    newDf["numero"] = pd.to_numeric(newDf["numero"], errors='coerce')
    return newDf

def saveBanoDataIntoDatabase(newDf):
    print("Save Bano data into database")
    engine = create_engine('postgresql:///bigdata')
    newDf.to_sql("BANO", engine, if_exists='replace')



def main(argv):
    tableName = ''
    try:
        opts, args = getopt.getopt(argv,"ht:",["tableName="])
    except getopt.GetoptError:
        print('dataToDatabase.py -t <tableName>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('dataToDatabase.py -t <tableName = [SIREN | BANO]>')
            sys.exit()
        elif opt in ("-t", "--tableName"):
            tableName = arg

    print("Script starting")
    if tableName == 'SIREN' or tableName == '':
        data = loadSirenDataFromCSV()
        saveSirenDataIntoDatabase(data)

    if tableName == 'BANO' or tableName == '':
        data = loadBanoDataFromCSV()
        saveBanoDataIntoDatabase(data)

if __name__ == "__main__":
    main(sys.argv[1:])
