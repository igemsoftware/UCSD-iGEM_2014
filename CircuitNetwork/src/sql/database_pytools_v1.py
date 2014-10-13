import sql_pytools as sqlpy
import sqlite3
import pandas as pd

def open(database):
    """Opens the specified database by making a connection to it."""
    global conn 
    conn = sqlite3.connect(database)
    conn.text_factory = str
    global sql 
    sql = conn.cursor()
    
def close():
    """Closes the mostly recently opened database."""
    conn.commit()
    sql.close()
    
def make_db():
    """Recreation of the sbider database tables. 
    	Careful! You will override the data.
    """
    plasmid = '''CREATE TABLE plasmid (pla_id VARCHAR(50), name VARCHAR(50), 
		miriam_id VARCHAR(50), title VARCHAR(50), authors VARCHAR(50), 
		journal VARCHAR(50), year VARCHAR(50));'''
	operon = '''CREATE TABLE operon (ope_id VARCHAR(50), name VARCHAR(50), 
	sbol VARCHAR(50));'''
	po = '''CREATE TABLE po (po_id VARCHAR(50), pla_id VARCHAR(50),
    	ope_id VARCHAR(50), direction VARCHAR(50));'''
    species = '''CREATE TABLE species (spe_id VARCHAR(50), name VARCHAR(50), 
	type VARCHAR(50));'''    
	oit = '''CREATE TABLE oit (it_id VARCHAR(50), ope_id VARCHAR(50));'''
	
	
	
	
	    
    oit = '''CREATE TABLE oit (ot_id VARCHAR(50), ope_id VARCHAR(50),
	tra_id VARCHAR(50));'''
    it = '''CREATE TABLE it (it_id VARCHAR(50), tra_id VARCHAR(50),
	spe_id VARCHAR(50));'''
    oot = '''CREATE TABLE output (out_id VARCHAR(50), ope_id VARCHAR(50), spe_id VARCHAR(50));'''
    login = '''CREATE TABLE login (log_id VARCHAR(50), email VARCHAR(50), 
	password VARCHAR(50));'''
	
    table_list =[plasmid, operon, species, op, ot, in_, out, login]
    for table in table_list:
		sql.execute(table)
        
def insert(table_name,cols,new_row):
    """Inserts data into the given database table
    Args:
        table_name, that table that you wish to insert into
        cols, the columns that you want to insert into
        new_row, the values that correspond to the columns
    
    Examples:
        ex 1. Inserting into plasmid table and filling in all the columns. 
    """
    command = sqlpy.sql_insert(table_name, cols,new_row)
    sql.execute(command)
    
def remove(table_name, cols
    
def select(table_name, col_names = ["ID"], w_col = None, w_opt = None,
    w_var = None,w_bool = None, group = False, h_col = None, h_bool = None, 
    h_value = None):
    """Pulls data from the corresponding table.
    Args:
        table_name: table you wish to pull data from
        col_names: list of numbers indexing the table columns
        w_col: column names for where clause
        w_opt: operator for where clause
        w_var: variable for where clause 
        w_bool: boolean for where clause
        group: group name for GROUP BY caluse
        h_col: group specifier
    """
    command = sqlpy.sql_select(table_name,col_names, w_col, w_opt, w_var,
        w_bool, group, h_col, h_bool, h_value)
    sql.execute(command)
    return sql.fetchall()
    
def update(table_name, cols, values, w_cols = [], 
	w_ops = [],w_values = [],w_conts = []):
    """Updates the values specificed by the paramaters in the connected database.
    """
    command = sqlpy.sql_update(table_name, table_name, cols, values, w_cols = [], w_ops = [],w_values = [],w_conts = [])
    sql.execute(command)
    
def custom(command):
    return sql.execute(command)
        
def print_table(table_name):
    """Prints out the specified table for visualization purposes only."""
    cur = sql.execute("SELECT * FROM " + table_name)
    table_list = cur.fetchall()
    for row in table_list:
        print row               
        
def to_network():
    """Making an input and out dictionary for the traversal."""
    
    hold = sql.execute('''SELECT ot.ope_id, input.tra_id, input.spe_id 
    	FROM ot, input WHERE ot.tra_id = input.tra_id''')
    	
    prev_ope, prev_tra, prev_spe = hold.next()
    input_dict = {}
    input_dict[prev_ope] = [[prev_spe]]
    curr_list = 0
    #print 'The initial operon', prev_ope
    #print 'The initial trans', prev_tra
    #print 'The initial spe', prev_spe
    for curr_ope, curr_tra, curr_spe in hold:
    	#print 'IN LOOP: prev operon value', prev_ope
    	#print 'IN LOOP: prev trans value', prev_tra
    	if prev_ope == curr_ope and curr_tra == prev_tra:
    		input_dict[curr_ope][curr_list].append(curr_spe)
    		#print "IN LOOP: curr spe added is", curr_spe
    	elif prev_ope == curr_ope and curr_tra != prev_tra:
    		curr_list += 1
    		input_dict[curr_ope].append([curr_spe])
    		prev_tra = curr_tra
    		#print "IN LOOP: curr spe added is", curr_spe
    	elif prev_ope != curr_ope:
    		curr_list = 0
    		prev_ope = curr_ope
    		prev_tra = curr_tra
    		input_dict[curr_ope] = [[curr_spe]]
    		#print "IN LOOP: curr spe added is", curr_spe
    	
    	#print 'IN LOOP: curr operon value', curr_ope
    	#print 'IN LOOP: curr trans value', curr_tra
    	
    output_dict = {}
    output = sql.execute("SELECT ope_id, spe_id FROM output")
    output = output.fetchall()
    for ope_id, spe_id in output:
        if ope_id in output_dict:
            output_dict[ope_id].add(spe_id)
        else:
            output_dict[ope_id] = set(spe_id)
    
    return input_dict, output_dict
    
def pull_columns(col_nums):
    """Returns a list of column names based on the index location"""
    columns= []
    for nums in col_nums:
        try:
            columns.append(col_nums[nums])
        except:
            raise Exception("Table is " + len(columns_list) + ''' long. Tried to 
                access non-existant index ''' + nums)
    return columns
    
def unlist_values(to_list):
    """Stringify values in a list that are within an inner list."""
    return [''.join(x) for x in to_list]
    
