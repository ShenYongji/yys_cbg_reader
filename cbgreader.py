import requests
import re
import json
import sys
import os
import time
import json


class cbg:
    def __init__(self):
        self.base_url ='https://yys.cbg.163.com/cgi/api/get_equip_detail?'
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'}
        self.sec_soul_list = {
               'maxHpAdditionRate': {'zh':'生命加成','base':0.03}, 
               'attackAdditionRate': {'zh':'攻击加成','base':0.03},
               'defenseAdditionRate': {'zh':'防御加成','base':0.03},
               'speedAdditionVal': {'zh':'速度','base':3},
               'critRateAdditionVal': {'zh':'暴击','base':0.03}, 
               'debuffResist': {'zh':'效果抵抗','base':0.04},
               'debuffEnhance': {'zh':'效果命中','base':0.04},
               'critPowerAdditionVal': {'zh':'暴击伤害','base':0.04}, 
               'defenseAdditionVal' : {'zh':'防御','base':5},  
               'maxHpAdditionVal' : {'zh':'生命','base':114}, 
               'attackAdditionVal': {'zh':'攻击','base':27}, 
            }
        self.soul = list()
        self.name = ''
        self.server = ''
        self.count = 0

    def readurl(self,url):
        if url.startswith("https://yys.cbg.163.com/"):
            start = 'equip/'
            start_len = len(start)
            index1 = url.find(start)
            server = url[index1+start_len:index1+start_len+10].find('/')
            server_code = url[index1+start_len:index1+start_len+server]
            id = url.find('?')
            if id != -1:
                id_code = url[index1+start_len+server+1:id]
                #print(id_name)
            else:
                id_code = url[index1+start_len+server+1:]
                #print(id_name)
            print(server_code,id_code)
            result = self.check_url(server_code,id_code)

        else:
            result = [-1,[]]


        return result

    def check_url(self,serverid,ordersn):
        try:
            html = requests.get(self.base_url,params={'serverid':serverid,'ordersn':ordersn},headers = self.header)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        html = html.json()
        if 'msg' in html:
            return [0,html['msg']]
        else:
            return [1,html]

    def get_server_name(self,html_text): 
        self.name = html_text['equip']['seller_name']
        self.server = html_text['equip']['server_name']

    
    def pull_soul(self,html_text):
        self.soul = []
        soul_info = html_text['equip']['equip_desc']
        #soul_info_json = soul_info.replace("'", "\"")
        #soul_info_json = soul_info.replace("'", "\"") //need to check reason 
        soul_info_json = soul_info
        print(soul_info_json)
        info = json.loads(soul_info_json)
        for i in info['inventory']:
            if info['inventory'][i]['level'] == 15:
                self.count += 1
                soul_len = len(info['inventory'][i]['rattr'])
                tmp = dict()
                tmp['御魂ID'] = info['inventory'][i]['uuid']
                tmp['御魂类型'] = info['inventory'][i]['name']
                tmp['位置'] = info['inventory'][i]['pos']
                tmp['御魂等级'] = info['inventory'][i]['level']
                tmp['御魂星级'] = info['inventory'][i]['qua']
                
                #副属性加
                for index in range(soul_len):
                    name = info['inventory'][i]['rattr'][index][0]
                    data = float(info['inventory'][i]['rattr'][index][1])
                    name_zh = self.sec_soul_list[name]['zh']
                    base = self.sec_soul_list[name]['base']
                    #print(name,data,name_zh)
                    if name_zh in tmp:
                        tmp[name_zh] += data*base
                    else:
                        tmp[name_zh] = data*base
                
                #主属性
                main_name = info['inventory'][i]['attrs'][0][0]
                main_name_data_str = info['inventory'][i]['attrs'][0][1]
                if main_name_data_str.endswith("%"):
                    main_name_data = float(main_name_data_str.strip("%"))/100.0
                else:
                    main_name_data = float(main_name_data_str)
                if main_name in tmp:
                    tmp[main_name] += main_name_data
                else:
                    tmp[main_name] = main_name_data
                
                #首领御魂固有属性属性
                if 'single_attr' in info['inventory'][i]:
                    #print (info['inventory'][i]['single_attr'])
                    boss_name = info['inventory'][i]['single_attr'][0]
                    boss_data_str = info['inventory'][i]['single_attr'][1]
                    if boss_data_str.endswith("%"):
                        boss_data = float(boss_data_str.strip("%"))/100.0
                    else:
                        boss_data = float(boss_data_str)
                    if boss_name in tmp:
                        tmp[boss_name] += boss_data
                    else:
                        tmp[boss_name] = boss_data

                    tmp['固有属性'] = boss_name

                #Insert into a list to store all souls
                self.soul.append(tmp)
                # #Following 3 lines for checking the info only
                # print(tmp)
                # print(info['inventory'][i]['attrs'])
                # print("______________________________")
        # print(count)
        # print(len(self.soul))

    def check_soul_speed(self): 
        speed_list = [[0.0,0,'类型'],[0.0,0,'类型'],[0.0,0,'类型'],[0.0,0,'类型'],[0.0,0,'类型'],[0.0,0,'类型']]
        for soul in self.soul:
            pos = int(soul['位置'])
            index = pos -1
            if '速度' in soul:
                if (float(soul['速度']) >= speed_list[index][0]):
                    speed_list[index][0] = float(soul['速度'])
                    speed_list[index][1] = int(soul['御魂星级'])
                    speed_list[index][2] = soul['御魂类型']
        return speed_list


    def jsonfile(self):
        json_list =[]
        json_list = ["yuhun_ocr2.0"] +self.soul
        json_file = json.dumps(json_list,indent=4)
        file_name = self.server+'_'+self.name+'_from_cbg.json'
        with open(file_name,'w') as outfile:
            outfile.write(json_file)
        
    
