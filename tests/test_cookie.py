import requests

headers = {
    'Cookie': '_xsrf=7001324875d8a80cde36186e97361317; d_c0="AJDAuZbdQgqPTilxkWwNaPPe6mnCQxOYxSs=|1469065965"; _zap=37bd8856-eaf9-4358-b8ba-452cf197b840; _za=7844ea65-13e9-43c7-bc6c-3bcb03c7dca3; _ga=GA1.2.607256830.1476954370; l_cap_id="NWI1MTJlZjM1NGUyNGI4ZGI0M2NlOTY2ZDYwNDZmN2E=|1479716844|46b7846248032650e531fbc0fc155c42453a8a94"; cap_id="ZWI5NzRiNDZjOWJhNDAzYWIxN2ZjNDA4OGMxZGQ2YmU=|1479716844|b330d8117a0edafb18551369d290feb7bdcfde2b"; n_c=1; r_cap_id="OGQyMjM4ZWVkZTk2NDU4NzgxMGU3N2IwYzQxZWI3ZmM=|1479718515|06b55e4f653a0289cc106d4f34afa6627d25a004"; login="NGYzZjZmZWY4OGY1NDE0Yjg4MjY3MjQ2MTdiNDU4M2Y=|1479721394|21e0230a7b8d9c3a70459508502234a6c608bf52"; s-q=%E7%82%89%E7%9F%B3; s-i=1; sid=o2jj4jco; s-t=autocomplete; q_c1=6092d37c511e48dc9d911cf811084ba9|1479927016000|1469065964000; a_t="2.0AADAImEaAAAXAAAAB9hkWAAAwCJhGgAAAJDAuZbdQgoXAAAAYQJVTbJOWlgAbibnSQ7hkUDp57nExs43Zrc2rDOu9dbnvjj_ieEOs9nZQWTBvH1Ivw=="; z_c0=Mi4wQUFEQUltRWFBQUFBa01DNWx0MUNDaGNBQUFCaEFsVk5zazVhV0FCdUp1ZEpEdUdSUU9ubnVjVEd6amRtdHphc013|1480411911|12f637ad7ca33f1758bf54b4d2c6f5daf7bbcc9c; __utmt=1; __utma=51854390.607256830.1476954370.1480383298.1480411228.2; __utmb=51854390.9.9.1480411564030; __utmc=51854390; __utmz=51854390.1480383298.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.100-1|2=registration_date=20130226=1^3=entry_date=20130226=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, li'
                  'ke Gecko) Chrome/54.0.2840.99 Safari/537.36'
}

url = 'http://www.zhihu.com'
s = requests.session()
r = s.get(url, headers=headers)
print r.text