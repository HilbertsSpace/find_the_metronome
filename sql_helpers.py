# This file contains has MySql statements and functions to help generate MySql statement

time_step_column_str = ','.join(['T_%s SMALLINT'%str(i) for i in range(512)])
COL_INSERT_STR = ','.join(['T_%s'%str(i) for i in range(512)])

make_audio_table = """
CREATE TABLE audio_data
(
    ID INT NOT NULL AUTO_INCREMENT,
    Y BOOLEAN,
    %s, 
    primary key (id)
);
"""%(time_step_column_str)


drop_audio_table = """
DROP TABLE IF EXISTS audio_data;
"""

def insert_audio_row(data, label=None):
    f = 0
    if type(data) is list:
        while len(data)<512:
            data.append(0)
            f = 1
    if f:
        print('padded')
    if label is None:
        label_val = 'NULL'
    else:
        label_val = label
    if len(data)==512:
        value_string = ','.join([str(d) for d in data])
        insert_rows = """
            INSERT INTO audio_data(ID, y, %s)
            VALUES (NULL, %s, %s); 
        """%(COL_INSERT_STR, label_val, value_string)
        return insert_rows
    else:
        return "Wrong Column Count"

def update_audio_row_label(id, label=None):
    if label is None:
        label_val = 'NULL'
    else:
        label_val = label
    s = """
    UPDATE audio_data 
    SET 
        y = label
    WHERE
    ID = %s;
    """%(label_val, id)
    return s

def get_labeled_audio_data(cursor, DB_NAME):
    cursor.execute("USE {};".format(DB_NAME))
    get_table = """select * from audio_data WHERE y is not NULL;"""
    cursor.execute(get_table)
    X = []
    y = []
    for each in cursor:
        y.append(int(float(each[1])))
        X.append([int(e) for e in each[2:]])
    return X,y

def get_unlabeled_audio_data(cursor, DB_NAME):
    cursor.execute("USE {};".format(DB_NAME))
    get_table = """select * from audio_data WHERE y is NULL;"""
    cursor.execute(get_table)
    X = []
    for each in cursor:
        X.append([int(e) for e in each[2:]])
    return X



