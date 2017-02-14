import json
import sys
from os import path

from pandas import read_csv

# Globals variables
cfg = ''  # configuration
data_path = ''
VERBOSE = False
df_bano= ''
df_siren= ''


def init(argv):
    global cfg, data_path, VERBOSE
    if len(argv) == 0:
        print("No config file defined")
        print("Usage : python dbmain.py setupfile.json")
        return
    config_file = str(argv[0])
    if not (path.exists(config_file)):
        print("Missing config file")

    with open(config_file, 'r') as json_file:
        cfg = json.load(json_file)
    print("Data expected in %s" % cfg['datapath'])
    VERBOSE = cfg['verbose']
    data_path = cfg['datapath']


def prepare_data_bano(verbose=VERBOSE):
    data_file = path.join(data_path, cfg['BANO'])
    if verbose: print("Reading %s" % data_file)
    df = read_csv(data_file, sep=',', header=None, encoding='latin-1')
    df.columns = cfg['BANOHeader']  # all columns are kept
    # create additional column with road type and road name
    # df['voie_type'] = ''
    # df['voie_denom'] = ''
    # TODO

    if verbose:
        print("Kept %d lines" % df.shape[0])
        print("Quick look\n %s" % df.head(5))

    return df


def prepare_data_siren(verbose=VERBOSE):
    data_file = path.join(data_path, cfg['SIREN'])
    if verbose:
        print("Reading %s" % data_file)
    df = read_csv(data_file, sep=';', header='infer', encoding='ISO-8859-15')  # encoding ?
    # drop columns
    if verbose:
        print("Keep following headers")
        print(cfg['SIRENHeader'])
    df = df[cfg['SIRENHeader']]
    # rename columns
    newnames = cfg['SIRENHEADERRename']
    df.rename(columns=newnames, inplace=True)
    # filter by dep
    if verbose:
        print("Rows before filtering by department : %d" % df.shape[0])
    filter_by = cfg["KEEP"]
    for a in filter_by:
        df = df.loc[df[a] == filter_by[a]]
    if verbose:
        print("Rows after filtering by department : %d" % df.shape[0])
    # bano id
    df['BANO_ID'] = -1

    if verbose:
        print("Kept %d rows" % df.shape[0])
        print("Quick look\n %s" % df.head(5))

    return df

'''
Populate a new column in SIREN df with the id of the corresponding BANO line
For each line of SIREN
    filter corresponding BANO with BANO.code_post == SIREN.CODPOS
        filter BANO.numero== SIREN.NUM_VOIE + f(SIREN.IND_REP)

'''
def join_data():
    if VERBOSE:
        print("-- join_data --")
    # get unique BANO.code_post
    unique_CP_BANO= df_bano.code_post.unique()
    unique_CP_SIREN= df_siren.CODPOS.unique()
    print(unique_CP_BANO)

    if VERBOSE:
        print("\t[BANO] Found %d unique code_post in %d rows" %(unique_CP_BANO.size, df_bano.shape[0]))
        print("\t[SIREN] Found %d unique CODPOS in %d rows" % (unique_CP_SIREN.size, df_siren.shape[0]))

    for bano_cp in unique_CP_BANO:
        # find all bano rows
        sub_bano= df_bano[df_bano['code_post']== bano_cp]
        # find all siren rows
        sub_siren= df_siren[df_siren['CODPOS']== bano_cp]
        if sub_siren.shape[0]>0:
            print("Found %d siren and %d bano" %(sub_siren.shape[0],sub_bano.shape[0]))
        match_data_with_same_code_post(sub_siren, sub_bano)


'''
Compare BANO{numero, voie} with SIREN{NUMVOIE, INDREP, TYPEVOIE, LIBVOIE}
'''
def match_data_with_same_code_post(sub_siren, sub_bano):
    return 0



if __name__ == "__main__":
    init(sys.argv[1:])
    df_bano = prepare_data_bano(verbose=False)
    df_siren = prepare_data_siren(verbose=True)
    #join_data()
