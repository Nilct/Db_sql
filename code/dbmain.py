import json
import sys
import string
from os import path
from unidecode import unidecode
from pandas import read_csv
from pandas import to_numeric
from pandas import notnull
from utils.measureduration import MeasureDuration
from sqlalchemy import create_engine, MetaData

# Globals variables
cfg = ''  # configuration
data_path = ''
VERBOSE = False
df_bano= ''
df_siren= ''

# database 
user= 'tp1'
password= 'tp1'
db='bigdata1'


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


'''
BANO :
- add columns ADD_num_voie and ADD_ind_rep to match SIREN NUMVOIE and INDREP
- add columns CAPS_voie
'''
def prepare_data_bano(verbose=VERBOSE):
    data_file = path.join(data_path, cfg['BANO'])
    print("Reading %s" % data_file)
    df = read_csv(data_file, sep=',', header=None, encoding='latin-1')
    df.columns = cfg['BANOHeader']  # all columns are kept
    # create additional columns from numero
    df['ADD_num_voie'] = df['numero'].map(lambda x: x.rstrip("TERBIS"))
    df['ADD_ind_rep'] = df['numero'].map(lambda x: x.lstrip('0123456789'))   
    df['ADD_ind_rep'] = df['ADD_ind_rep'].map(lambda x: x.replace('BIS', 'B'))
    df['ADD_ind_rep'] = df['ADD_ind_rep'].map(lambda x: x.replace('TER', 'T'))
    # additional columns : remove accent and put in caps
    df['ADD_caps_voie'] = df['voie'].map(lambda x: unidecode(x.upper()))
    df.loc[df['ADD_ind_rep'].map(len)>0,['ADD_caps_voie']] = df['ADD_ind_rep']+' '+df['voie'].map(lambda x: unidecode(x.upper()))
    df['ADD_caps_nom_comm'] = df['nom_comm'].map(lambda x: unidecode(x.upper()))
    # change lat/lon dtype
    df[['lat', 'lon']].apply(to_numeric)
    print("Kept %d rows" % df.shape[0])
    if verbose:  
        print("Quick look\n %s" % df.head(5))
    # useful before loading to dn
    df.where((notnull(df)), None)
    return df

'''
SIREN
- drop useless columns
- rename columns
- filter by department
- create full street name (
'''
def prepare_data_siren(verbose=VERBOSE):
    data_file = path.join(data_path, cfg['SIREN'])
    print("Reading %s" % data_file)
    df = read_csv(data_file, sep=';', header='infer', encoding='ISO-8859-15')  # encoding ?
    # drop columns
    if verbose:
        print("Keep following headers (%d)"%len(cfg['SIRENHeader']))
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
    # create columns for address
    di= {'ALL': 'ALLEE ', 'AV': 'AVENUE ', 'BD':'BOULEVARD ', 'CHE':'CHEMIN ', 'CHS':'CHAUSSEE ', 'FG':'FAUBOURG ', 'IMP':'IMPASSE ', 'LOT':'LOTISSEMENT ', 'PL':'PLACE ', 'QUA':'QUARTIER ', 'QUAI':'QUAI ', 'RUE': 'RUE ', 'RTE':'ROUTE '}
    df['TMP_TYPVOIE'] = df['TYPVOIE'].replace(di)  # option : inplace=True
    df['TMP_LIBVOIE'] = df['LIBVOIE'].map(lambda x: unidecode(x))
    # get ready for merging
    df['ADD_VOIE'] = df['TMP_TYPVOIE'] + df['TMP_LIBVOIE']
    df.loc[df['INDREP'].notnull(),['ADD_VOIE']] = df['INDREP']+' '+df['ADD_VOIE']
    #df[df.ADD_TYPVOIE.isin(df.ADD_LIBVOIE)==False]['ADD_VOIE']=  df['ADD_TYPVOIE']+ df['ADD_LIBVOIE']
    df['ADD_LIBCOM'] = df['LIBCOM'].map(lambda x: unidecode(x))

    # drop TMP columns
    df.drop(['TMP_TYPVOIE', 'TMP_LIBVOIE'], inplace=True, axis=1)

    # bano id
    df['BANO_ID'] = ""
    print("Kept %d rows" % df.shape[0])
    if verbose:
        print("Quick look\n %s" % df.head(5))
        #print("Quick look\n %s" % df.ADD_VOIE.head(50))

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
    unique_CP_BANO = df_bano.code_post.unique()
    unique_CP_SIREN = df_siren.CODPOS.unique()
    print(unique_CP_BANO)

    if VERBOSE:
        print("\t[BANO] Found %d unique code_post in %d rows" %(unique_CP_BANO.size, df_bano.shape[0]))
        print("\t[SIREN] Found %d unique CODPOS in %d rows" % (unique_CP_SIREN.size, df_siren.shape[0]))

    for bano_cp in unique_CP_BANO:
        # find all bano rows
        sub_bano = df_bano[df_bano['code_post'] == bano_cp]
        # find all siren rows
        sub_siren = df_siren[df_siren['CODPOS'] == bano_cp]
        if sub_siren.shape[0] > 0:
            print("Found %d siren and %d bano" % (sub_siren.shape[0] , sub_bano.shape[0]))
        #match_data_with_same_code_post(sub_siren, sub_bano)


'''
Compare BANO{numero, voie} with SIREN{NUMVOIE, INDREP, TYPEVOIE, LIBVOIE}
'''
def match_data_with_same_code_post(sub_bano):
    # match [BANO]ADD_num_voie with [SIREN]NUMVOIE
    #             ADD_ind_rep              INDREP
    #             ADD_caps_voie            ADD_VOIE
    #             code_post                CODPOS (already done)
    #             ADD_nom_comm             ADD_LIBCOM
    #df[ (df.A=='blue') & (df.B=='red') & (df.C=='square') ]['D'] = 'succeed'
    #df_siren[(sub_bano.ADD_num_voie == df_siren.NUMVOIE) & (sub_bano.ADD_caps_voie==df_siren.INDREP) & (sub_bano.ADD_nom_comm == df_siren.ADD_LIBCOM)]['BANO_ID']=

    return 0

'''
Database
'''
def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = MetaData(bind=con, reflect=True)

    print(con)
    print(meta)

    return con, meta

def importData(engine):
    df_siren.to_sql("siren", engine, if_exists='replace')
    df_bano.to_sql("bano", engine, if_exists='replace')
    
    


if __name__ == "__main__":
    init(sys.argv[1:])
    
    with MeasureDuration() as m:
        df_bano = prepare_data_bano()
    with MeasureDuration() as m:
        df_siren = prepare_data_siren()
    #join_data()
    con, meta= connect(user, password, db)
    with MeasureDuration() as m:
        importData(con)

    