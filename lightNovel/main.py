#!/usr/bin/python3

import urllib3, collections, sys

def download_file(url, fileName="home.html"):
    http = urllib3.PoolManager()
    req = http.request("GET", url)
    if req.status != 200:
        print("%s %d", url, int(req.status))

    fp = open(fileName, "w")
    fp.write(str(req.data).replace("\\n","\n").replace("\\t","\t").replace("><", ">\n<"))
    fp.close()

    return fileName

def separate_menu(homeName, menuName="menu_xianxia.csv"):
    dict_menu_tmp = {}
    dict_menu = {}

    fp = open(homeName, "r")
    for line in fp:
        if "Xianxia &#038; More" in line:
            line = next(fp)
            while "</ul>" not in line:
                if "a href=\"" in line:
                    url = line.split("\"")[1]
                    name = line.split("\"")[2].split(">")[1].split("(")[0].replace("&#038;", "and")
                    dict_menu_tmp[name] = url
                line = next(fp)
    fp.close()

    dict_menu = collections.OrderedDict(sorted(dict_menu_tmp.items(), key=lambda t: t[0]))

    fp = open(menuName, "w")
    for item in dict_menu:
        fp.write("\""+item[:-1]+"\",\""+dict_menu[item]+"\"\n")

    fp.close()

    del dict_menu
    del dict_menu_tmp

    return menuName
# Teste Parameters
fileName = "home.html"
menuName = "menu_xianxia.csv"

# Main
# fileName = download_file("http://www.wuxiaworld.com/")
menuName = separate_menu(fileName)

with open(menuName, "r") as entry:
    for key in entry:
        name = key.split(",")[0].split("\"")[1]
        url = key.split(",")[1].split("\"")[1]
        if len(sys.argv) > 1:
            for it in range(1, len(sys.argv)):
                if sys.argv[it].lower() in name.lower():
                    print("Downloading '%s' ..." % name)
                    download_file(url, name.lower().replace(" ","_") + "_index.html")
        else:
            print("Downloading '%s' ..." % name)
            download_file(url, name.lower().replace(" ","_") + "_index.html")
