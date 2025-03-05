from DAL.PublicRep import PR
from PyQt5.QtTextToSpeech import *

engine = QTextToSpeech()
def text_to_speech(text):
    engine.say(str(text))


class PRR:
    
    def Style():
        try:
            res = PR.Style()
            return res
        except Exception as e:
            return None
    
    def DF():
        try:
            res = PR.DF()
            return res
        except Exception as e:
            return None
    
    def KL():
        try:
            res = PR.KL()
            return res
        except Exception as e:
            return None
        
    def set_KL(kl, user, passw):
        try:
            PR.set_KL(kl, user, passw)
            return True
        except Exception as e:
            return False
        
    def Select(fields, table, where):
        res = PR.Select(str(fields), str(table), str(where))
        return res
        
        """try:
            res = PR.Select(str(fields), str(table), str(where))
            return res
        except Exception as e:
            notif("Error", "Selection Data Error")
            return None"""

    def Delete(table, where):
        try:
            res = PR.Delete(str(table), str(where))
            return res
        except Exception as e:
            return None

    def Insert(table, fields, values):
        try:
            res = PR.Insert(str(table), str(fields), str(values))
            return res
        except Exception as e:
            return None

    def Filter(search_text, filter_text):
        lst = len(search_text)
        if str(search_text).strip() == str(filter_text)[0:int(lst)].strip() :
            return True
        else:
            return False
        
    def Update(table, set_fields, where):
        try:
            res = PR.Update(str(table), str(set_fields), str(where))
            text_to_speech("Update Success")
            return res
        except Exception as e:
            return None
    
    def SelectSuppliers(where):
        try:
            res = PR.SelectSuppliers(str(where))
            return res
        except Exception as e:
            return None

    def SelectProducts(where):
        try:
            res = PR.SelectProducts(str(where))
            return res
        except Exception as e:
            return None

    def AddCustomTableToJsonFile(TableData):
        try:
            PR.AddCustomTableToJsonFile(TableData)
            return True
        except Exception as e:
            return None
    
    def GetCustomTableFromJsonFile():
        try:
            res = PR.GetCustomTableFromJsonFile()
            return res
        except Exception as e:
            return None

    def GetFields_of_a_table(table):
        try:
            res = PR.GetFields_of_a_table(str(table))
            return res
        except:
            return None
        
    def Get_Saved_Tables():
        try:
            return PR.Get_Saved_Tables()
        except:
            return None

    def add_to_Saved_Tables(data):
        try:
            PR.add_to_Saved_Tables(data)
            return True
        except:
            return False
    
    def del_saved_Table_by_index(idx):
        try:
            PR.del_saved_Table_by_index(idx)
            return True
        except:
            return False
    
    def get_CSPBS_tbls_dt_pd():
        try:
            res = PR.get_CSPBS_tbls_dt_pd()
            return res
        except:
            return False

    def SQL_Table_to_custom_data(db_address, table_name, table_custom_name=None):
        try:
            res = PR.SQL_Table_to_custom_data(str(db_address), str(table_name), table_custom_name)
            return res
        except:
            return False
    
    def GetTablesOfAsqlFile(db_address):
        try:
            res = PR.GetTablesOfAsqlFile(db_address)
            return res
        except:
            return False
        
    def set_lock_info(lock, psw):
        try:
            res = PR.set_lock_info(str(lock), str(psw))
            return res
        
        except:
            return False
           
    def get_lock_info():   
        try:
            res = PR.get_lock_info()
            return res
        
        except:
            return False


