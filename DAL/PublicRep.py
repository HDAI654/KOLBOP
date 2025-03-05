import json
import sqlite3
import pandas as pd
import pickle
from cryptography.fernet import Fernet
class PR:
    def Style():
        with open('Assets/Databases/Data.json', 'r') as f:
            data = json.load(f)
        css_addres = str(data["CSS_Address"])
        with open(css_addres, 'r') as c:
            return str(c.read())
    
    def DF():
        with open('Assets/Databases/Data.json', 'r') as f:
            data = json.load(f)
        res = str(data["DateFormat"])
        return res
    
    def KL():
        with open('Assets/Databases/Data.json', 'r') as f:
            data = json.load(f)
        res = [int(data["keep_login"]), data["username"], data["password"]]
        return res
    
    def set_KL(kl, user, passw):
        with open('Assets/Databases/Data.json', 'r') as f:
            data = json.load(f)
        data['keep_login'] = int(kl)
        data['username'] = str(user)
        data['password'] = str(passw)
        with open('Assets/Databases/Data.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    def Select(fields, table, where):
        con = sqlite3.connect("Assets/Databases/data.db")
        cur = con.cursor()
        data = list(cur.execute(f"SELECT {fields} FROM {table} WHERE {where}").fetchall())
        return data
    
    def Delete(table, where):
        con = sqlite3.connect("Assets/Databases/data.db")
        cur = con.cursor()
        cur.execute(f"DELETE FROM {table} WHERE {where}")
        con.commit()
        con.close()
        return True
    
    def Insert(table, fields, values):
        con = sqlite3.connect("Assets/Databases/data.db")
        cur = con.cursor()
        cur.execute(f"INSERT INTO {table} ({fields}) VALUES ({values})")
        con.commit()
        con.close()
        return True
    
    def Update(table, set_fields, where):
        conn = sqlite3.connect("Assets/Databases/data.db")
        cur = conn.cursor()
        cur.execute(f"UPDATE {table} SET {set_fields} WHERE {where}")
        conn.commit()
        conn.close()
        return True

    def SelectSuppliers(where):
        conn = sqlite3.connect("Assets/Databases/data.db")
        cur = conn.cursor()

        # Supliers Data
        data = list(cur.execute(f"SELECT * FROM Suppliers WHERE {where}").fetchall())
        data = [list(d) for d in data]

        # Supplier's Products
        for s in data:
            prs = list(cur.execute(f"SELECT Name FROM Products WHERE SC = {s[0]}").fetchall())
            prs = [str(p[0]) for p in prs]
            prs = ', '.join(prs)
            s.insert(9, prs)
            data[data.index(s)] = s
            prs = None
        cur.close()
        conn.close()
        return data

    def SelectProducts(where):
        conn = sqlite3.connect("Assets/Databases/data.db")
        cur = conn.cursor()
        data = list(cur.execute(f"SELECT * FROM Products WHERE {where}").fetchall())
        data = [list(d) for d in data]


        for p in data:
            sup = PR.SelectSuppliers(f"ID = {p[2]}")
            sup = sup[0][1]
            p[2] = str(p[2]) + ' - ' + str(sup)
            data[data.index(p)] = p




        cur.close()
        conn.close()

        return data

    def AddCustomTableToJsonFile(TableData):
        with open('Assets/Databases/Data.json', 'r') as f:
            data = json.load(f)
        data['Custom_Table']=TableData
        with open('Assets/Databases/Data.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    def GetCustomTableFromJsonFile():
        with open('Assets/Databases/Data.json', 'r') as f:
            data = json.load(f)
        return data['Custom_Table']

    def GetFields_of_a_table(table):
        conn = sqlite3.connect("Assets/Databases/data.db")
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table} LIMIT 1")
        fields_name = [field[0] for field in cur.description]
        cur.close()
        conn.close()
        return fields_name
    
    def Get_Saved_Tables():
        with open('Assets/Databases/Data.json', 'r') as f:
            data = json.load(f)
        return data['Saved_Tables']

    def add_to_Saved_Tables(td):
        with open('Assets/Databases/Data.json', 'r') as f:
            data = json.load(f)
        exist = False
        for i, t in enumerate(data['Saved_Tables']):
            if t['Table_name'] == td['Table_name']:
                exist = True
                data['Saved_Tables'][i]=td
        if exist != True:
            data['Saved_Tables'].append(td)
        with open('Assets/Databases/Data.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    def del_saved_Table_by_index(idx):
        if idx != "All":
            with open('Assets/Databases/Data.json', 'r') as f:
                data = json.load(f)
            data['Saved_Tables'].pop(idx)
            with open('Assets/Databases/Data.json', 'w') as f:
                json.dump(data, f, indent=4)
        else:
            with open('Assets/Databases/Data.json', 'r') as f:
                data = json.load(f)
            data['Saved_Tables'] = []
            with open('Assets/Databases/Data.json', 'w') as f:
                json.dump(data, f, indent=4)
                
    def get_CSPBS_tbls_dt_pd():
        res = {
            "Clients":None,
            "Suppliers":None,
            "Products":None,
            "Buy":None,
            "Sale":None,
        }
        conn = sqlite3.connect('Assets/Databases/data.db')
        for h in res.keys():
            df = pd.read_sql_query(f"SELECT * FROM {str(h)}", conn)
            df = pd.DataFrame(df)
            res[h] = df
        conn.close()
        
        return res
    
    def SQL_Table_to_custom_data(db_address, table_name, table_custom_name=None):
        table_name = table_name
        if table_custom_name is None:
            table_name = table_custom_name
        conn = sqlite3.connect(db_address)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM {}".format(table_name))
        data = cursor.fetchall()
        
        table = {
            "Table_name": table_name,
            "Columns": [],
            "Rows_data": [],
            "Primary_status": [],
            "Columns_Charts_index": []
        }
        
        # get column names
        fields = []
        cursor.execute("SELECT * FROM {} LIMIT 0".format(table_name))
        column_names = [description[0] for description in cursor.description]
        # get column types
        for column_name in column_names:
            # get column type
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns_info = cursor.fetchall()
            col_type = columns_info[column_names.index(column_name)][2]
            col_typeol_type = col_type.upper()
            col_pk = columns_info[column_names.index(column_name)][5]
            
            if col_type not in ["INTEGER", "REAL", "NUMERIC", "INT", "FLOAT", "DOUBLE", "SMALLINT", "BIGINT", "DECIMAL", "TINYINT", "BLOB", "BOOLEAN"] and col_type not in ["TEXT", "VARCHAR", "CHAR", "NVARCHAR", "NCHAR", "CLOB", "TEXT", "STRING"] and col_pk != 1:
                col_type = "Free"
            if col_type in ["INTEGER", "REAL", "NUMERIC", "INT", "FLOAT", "DOUBLE", "SMALLINT", "BIGINT", "DECIMAL", "TINYINT", "BLOB", "BOOLEAN"]:
                col_type = "Integer"
            if col_type in ["TEXT", "VARCHAR", "CHAR", "NVARCHAR", "NCHAR", "CLOB", "TEXT", "STRING"]:
                col_type = "String"
            if col_pk == 1:
                col_type = "Primary" 
            fields.append([str(column_name), str(col_type), '#343a40', '#f8f9fa'])
            
        table["Columns"] = fields
        
        # get rows data
        rows_data = []
        for row in data:
            rows_data.append(list(row))
        table['Rows_data'] = rows_data
        
        conn.close()
        return table
    
    def GetTablesOfAsqlFile(db_address):
        conn = sqlite3.connect(str(db_address))
        cur = conn.cursor()
        
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [tbl[0] for tbl in cur.fetchall()]
        
        
        return tables
    
    def GetSecretKey():
        try:
            with open('Assets/DataBases/SEC.key', 'rb') as key_file:
                key = key_file.read()
                return key
        except:
            return None
    
    def set_lock_info(lock, psw):
        data = [str(lock), str(psw)]
        key = PR.GetSecretKey()
        if key is None:
            return None
        
        else:
            cipher = Fernet(key)
            for i, d in enumerate(data):
                data[i] = cipher.encrypt(d.encode())
                with open('Assets/DataBases/data.pkl', 'wb') as dfile:
                    pickle.dump(data, dfile)
            return True
    
    def get_lock_info():
        key = PR.GetSecretKey()
        if key is None:
            return None
        
        else:
            cipher = Fernet(key)
            
            with open('Assets/DataBases/data.pkl', 'rb') as dfile:
                encrypted_data = pickle.load(dfile)
            decrypted_data = []
            for encrypted_item in encrypted_data:
                decrypted_item = cipher.decrypt(encrypted_item).decode()
                decrypted_data.append(decrypted_item)
            return decrypted_data
        

        
    
    
    
    
    
    
    
    
    