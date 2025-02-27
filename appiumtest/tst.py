import json

with open('fishInfo.json', 'r',encoding='utf-8') as f:
    dict_list = json.load(f)
print(dict_list)
dict_list['灵魂鱼'].sort(key=lambda x:x['size'])

dict_list['灵魂鱼'][0]['size']=23.46
print(dict_list['灵魂鱼'])