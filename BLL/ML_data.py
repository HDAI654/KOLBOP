from BLL.PublicRrep import PRR
import numpy as np

class ML_Data:
    def SaleBuy_Year_HC():
        # All Sales Data
        Sales = [list(s) for s in PRR.Select("*", "Sale", "true")]

        # Years Split
        Y_split = []
        for sl in Sales:
            Y_split.append(str(str(sl[2]).split("/")[0]).strip())
        Y_split = set(Y_split)
        Y_split = list(Y_split)

        # Years and Data Split
        Y_splited_data = {}
        for y in Y_split:
            Y_splited_data[str(y)] = []
        for s in Sales:
            Y_splited_data[str(str(str(s[2]).split("/")[0]).strip())].append(s)

        # Years Total Prices calculate
        TPs = {}
        for k, v in Y_splited_data.items():
            n = 0
            for d in v:
                n+=int(d[1])
            TPs[str(k)] = n

        ########################################

        # All Buy Data
        Buys = [list(s) for s in PRR.Select("*", "Buy", "true")]

        # Years Split
        YB_split = []
        for sl in Buys:
            YB_split.append(str(str(sl[2]).split("/")[0]).strip())
        YB_split = set(YB_split)
        YB_split = list(YB_split)

        # Years and Data Split
        YB_splited_data = {}
        for y in YB_split:
            YB_splited_data[str(y)] = []
        for b in Buys:
            YB_splited_data[str(str(str(b[2]).split("/")[0]).strip())].append(b)

        # Years Total Prices calculate
        TPb = {}
        for k, v in YB_splited_data.items():
            n = 0
            for d in v:
                n+=int(d[1])
            TPb[str(k)] = n

        # END DATA
        main_data = {}
        for key, val in TPs.items():
            if key in TPb.keys():
                main_data[key] = [val, TPb[key]]
            else:
                main_data[key] = [val, 0]
        for ky, vl in TPb.items():
            if ky not in main_data.keys() and ky not in TPs.keys():
                main_data[ky] = [0, vl]

        ready_data = {"DICT":main_data, "ML_Data":[vlu for vlu in list(main_data.values())], "GUID":"[Sale, Buy]"}
        return ready_data
    def Quarter_Years():
        old_data = ML_Data.SaleBuy_Year_HC()
        
        if old_data["DICT"] == {}:
            return "No Data 025ScniS4ecn8W"
        elif len(old_data["DICT"].keys()) < 3:
            return "Not Enough Data dneeEED2eceE5"
        elif old_data["DICT"] != {}:
            new_data = {"DICT":{}, "GUID":"Sale-Buy"}
            for key, val in old_data["DICT"].items():
                new_data["DICT"][str(key)] = int(int(val[0]) - int(val[1]))
            data_listed = []
            for k, v in new_data["DICT"].items():
                data_listed.append(int(v))
            data_listed.sort()

            # first [] to [[], []]
            mo_data_listed = np.median(data_listed)
            if mo_data_listed in data_listed:
                i = int(data_listed.index(mo_data_listed))
                l = int(len(data_listed))
                data_listed.remove(mo_data_listed)
                data_listed = [data_listed[0:i], data_listed[i:l]]
            else:
                l = int(len(data_listed))
                data_listed = [data_listed[0:int(l/2)], data_listed[int(l/2):l]]

            # range nums ready
            range_nums = [int(np.median(data_listed[0])), int(np.median(data_listed[1]))]
            range_nums.sort()

            # END
            end_data = {
                "BAD":[],
                "MEDIUM":[],
                "GOOD":[],
                "GUID":'[ [year, profit] ]'
            }
            for ky, vl in new_data["DICT"].items():
                #bad
                if int(vl) < int(range_nums[0]):
                    end_data["BAD"].append([ky, vl])
                #medium
                if int(vl) > int(range_nums[0]) and int(vl) < int(range_nums[1]):
                    end_data["MEDIUM"].append([ky, vl])
                #good
                if int(vl) > int(range_nums[1]):
                    end_data["GOOD"].append([ky, vl])
        
                
            return end_data

        
        
    