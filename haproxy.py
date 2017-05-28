# Author：zhaoyanqi
#! /usr/bin/env python
# -*- coding: utf-8 -*-


def search(data):
    flag = False
    data_list = []
    with open("haproxy","r") as f:
        for line in f:
            #print(line)
            if line.strip() == "backend %s"%data:
                flag = True
                continue
            if line.startswith("backend"):
                flag = False
            if flag:
                data_list.append(line)
        for line in data_list:
            print(line.strip())
        # if data_list == []:
        #     print("没有这个")
    return data_list
# {'backend': 'www.bb.com','record':{'server': '10.10.10.10','weight': 20,'maxconn':3000}}
def add(data):
    backend_name = data_input["backend"]
    data_list = search(backend_name) #搜索输入字典里的backend
    backend_info = "backend %s" %backend_name
    record_dic = data_input["record"]
    record_info = "server %s weight %s maxconn %s" \
                  %(record_dic["server"],\
                  record_dic["weight"],\
                  record_dic["maxconn"])
    # print(record_info)
    if data_list == []:#如果输入字典里的backend原本不存在，则执行添加
        with open("haproxy","r") as file,open("haproxy_bak","w") as bak_file:
            for line in file:
                bak_file.write(line)#将老文件备份成haproxy_bak
        with open("haproxy","a") as new_file:#将新内容覆盖老文件
            new_file.write(backend_info+"\n")
            new_file.write("\t"*2+record_info+"\n")
    else:
        token = False
        for line in data_list:#如果字典里backend原本存在
            if  line.strip() == record_info:#检查是否存在一条数据和字典里的相同
                token = True #存在则token为真
        if token:
            print("已存在")
        else:
            data_list.append("\t"*2+record_info+"\n")
            # print(data_list)
            data_list.insert(0,backend_info+"\n")#新加进去的部分写进data_list
            # for line in data_list:
            #     print(line)
            with open("haproxy", "r") as file, open("haproxy_bak", "w") as bak_file:
                for line in file:
                    bak_file.write(line)  # 将老文件备份成haproxy_bak
            with open("haproxy_bak","r") as old_file,open("haproxy","w") as new_file:
                flag2 = True#设置一个打开的token
                written = False#设置一个检验是否已经写过新data_list的标签
                for line in old_file:
                    # if flag2:
                        # new_file.write(line)
                    if line.strip() == backend_info:#当遍历到字典中的backend，把token关上
                        flag2 = False
                        continue
                    if line.startswith("backend"):#添加的backend结束，把token重新打开
                        flag2 = True
                    if flag2:#如果tonken是打开的，那么就把这一行写进去
                        new_file.write(line)
                    else:#如果token是关闭的，就把新的data_list写进去
                        if written == False:#因为不止一行flag2=false，防止多次写入新data_list，这里做一个校验
                            for line in data_list:
                                new_file.write(line)
                            written = True#当written为true时，说明已经写过了，下一次就不会再写了

def delete(data):
    backend_name = data_input["backend"]
    data_list = search(backend_name) #搜索输入字典里的backend
    backend_info = "backend %s" %backend_name
    record_dic = data_input["record"]
    record_info = "server %s weight %s maxconn %s" \
                  %(record_dic["server"],\
                  record_dic["weight"],\
                  record_dic["maxconn"])
    token = False
    for line in data_list:
        if line.strip() == record_info:
            token = True
    if token:
        data_list.remove("\t"*2+record_info+"\n")
        data_list.insert(0, backend_info + "\n")
        # print(data_list)
        # for line in data_list:
        #     print(line)
        with open("haproxy", "r") as file, open("haproxy_bak", "w") as bak_file:
            for line in file:
                bak_file.write(line)  # 将老文件备份成haproxy_bak
        with open("haproxy_bak", "r") as old_file, open("haproxy", "w") as new_file:
            flag2 = True  # 设置一个打开的token
            written = False  # 设置一个检验是否已经写过新data_list的标签
            for line in old_file:
                # if flag2:
                # new_file.write(line)
                if line.strip() == backend_info:  # 当遍历到字典中的backend，把token关上
                    flag2 = False
                    continue
                if line.startswith("backend"):  # 添加的backend结束，把token重新打开
                    flag2 = True
                if flag2:  # 如果tonken是打开的，那么就把这一行写进去
                    new_file.write(line)
                else:  # 如果token是关闭的，就把新的data_list写进去
                    if written == False:  # 因为不止一行flag2=false，防止多次写入新data_list，这里做一个校验
                        for line in data_list:
                            new_file.write(line)
                        written = True  # 当written为true时，说明已经写过了，下一次就不会再写了
        print("删除成功")
    else:
        print("没这个数据")






if __name__ == '__main__':

    choice_list = ["查询", "添加", "删除", "退出"]

    choice_dic = {
        "1":search,
        "2":add,
        "3":delete,
        "4":exit,
    }

    while True:
        for index, line in enumerate(choice_list):
            print(index + 1, line)
        choice_input = input("输入你得选择:").strip()
        if len(choice_input) == 0 or choice_input not in choice_dic:
            print("请输入正确的选项")
            continue

        if choice_input == "4":
            exit()

        data_input = input("输入内容:")
        if choice_input != "1":
            data_input = eval(data_input)

        choice_dic[choice_input](data_input)



