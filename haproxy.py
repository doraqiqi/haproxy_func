# Author：zhaoyanqi

def search(data):
    flag = False
    data_list = []
    token = 0
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
        if data_list == []:
            token = 1
    return token

def add(data):
    token = 0
    with open("haproxy","r") as f:
        for line in f:
            if "backend %s" %data == line.strip():
                token += 1
    if token > 0:
        print("已存在")
    else:
        b ={
            'backend': '',
            'record':{
                'server': '',
                'weight': 0,
                'maxconn':0
                }
        }
        # 修改字典内容:
        b['backend'] = data
        while True:
            server_update = input("请输入server的ip：")
            if server_update == "":
                print("不能为空")
            else:
                b['record']['server'] = server_update
                break
        while True:
            weight_update = input("请输入weight的值：")
            if weight_update == "":
                print("不能为空")
            else:
                if weight_update.isdigit():
                    b['record']['weight'] = int(weight_update)
                    break
                else:
                    print("请输入数字")
                    continue
        while True:
            maxconn_update = input("请输入maxconn的值：")
            if maxconn_update == "":
                print("不能为空")
            else:
                if maxconn_update.isdigit():
                    b['record']['maxconn'] = int(maxconn_update)
                    break
                else:
                    print("请输入数字")
                    continue
        # 修改完的内容写入haproxy:
        with open("haproxy", "a", encoding="utf-8") as f3:
            f3.write("backend")
            bakend_w = b.get("backend")
            f3.write(" " + bakend_w)
            t2 = b.get("record")
            server_w = t2.get("server")
            weight_w = t2.get("weight")
            maxconn_w = t2.get("maxconn")
            f3.write("\n" + "\t" + "\t")
            f3.write("server" + " " + server_w + " " + "weight" + " " + str(weight_w) + " " + "maxconn" + " " + str(
                maxconn_w) + "\n")
            print("添加完成")

def delete(data):
    token = 0
    flag = 0
    old_haproxy = []
    new_haproxy = []
    with open("haproxy","r") as f:
        for line in f:
            old_haproxy.append(line)
            if "backend %s" % data == line.strip():
                #print(line)
                flag = 1
                token = 1#说明输入内容可以找到，可以删除
                continue
            if line.startswith("backend"):
                flag = 0
            if flag == 0:
                new_haproxy.append(line)
    with open("haproxy_bak","w") as f_oldHaproxy:
        for line in old_haproxy:
            f_oldHaproxy.write(line)
    with open("haproxy","w") as f_newHaproxy:
        for line in new_haproxy:
            f_newHaproxy.write(line)
    if token == 1:
        print("已经删除，原文件内容备份在haproxy_bak里")
    else:
        print("找不到这个")

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
        if len(choice_input) == 0 and choice_input not in choice_dic:
            print("请输入正确的选项")
            continue

        if choice_input == "1":
            while True:
                data_input = input("输入你要查询的域名，输入b返回，输入q退出:").strip()
                if data_input == "b":
                    break
                if data_input == "q":
                    exit()
                else:
                    s = search(data_input)
                if s == 1:
                    print("没有找到")

        if choice_input == "2":
            while True:
                data_input = input("输入你要添加的域名，输入b返回，输入q退出:").strip()
                if len(data_input) == 0:
                    print("不能为空")
                    continue
                if data_input == "b":
                    break
                if data_input == "q":
                    exit()
                else:
                    add(data_input)

        if choice_input == "3":
            while True:
                data_input = input("输入你要删除的域名，输入b返回，输入q退出:").strip()
                if len(data_input) == 0:
                    print("不能为空")
                    continue
                if data_input == "b":
                    break
                if data_input == "q":
                    exit()
                else:
                    delete(data_input)

        if choice_input == "4":
            exit()

