from employ import *
# import zipfile


# zip = zipfile.ZipFile("C:/Program Files/Python311/Python311.zip")

# print(zip.getinfo("z/").is_dir())
# for name in zip.namelist():
#     path = name.split("/")

#     if path[0] == "z":
#         if len(path) == 2 and path[1] != "":
#             print(path[1])
#         elif len(path) == 3 and path[2] == "":
#             print(path[1])

# files = [
#     name
#     for name in zip.namelist()
#     if name.startswith("z/") and name.count("/") == "z/".count("/")
#     ]
# print(files)
# if not employ.__deps__.zippath(__zip__).is_dir(__name__):
#     __isdir__ = False

#     __filename__ = __name__+".py"
#     __io__ = __zip__.open(__filename__)
# file = zip("cashew.zip").open("cashew.py")
# print(file.read().decode())

cas = employ("jsondata", res={"xy": "Yesssss", "yz": [1,2]})
print(cas.data)
# print(cas.queue)
# cas.helloworld()
# cas.__thread__.join()
# cas.__univ__.t = False
# # cas.apple.change()
# cas.apple.view()
# cas.cashew.view()
# cas.pear.seed.view()
# print(cas.__univ__.t)
# print(cas.modules)

##dic = {}
##employ("z", name="z", on="main", res=dic)
##print(dic)
##b = json.loads(json.dumps(dic))
##print(b)

#parent = employ("a", path="C:/employrs/MichaelPells/Documents/Python/employ module/")
#print(parent.__env__)

# from requests import get as __get__
# __getoptions__ = {"allow_redirects": True, "timeout": 30}
# res = __get__("http://localhost:3000/z/__init__.py"+"/"+"__init__.py", **__getoptions__).status_code
# print(res)
# print(dir(res))
# res.name="myfile"
# print(res.name)



import json
import re

# def interpret(match):
#     code = match.group(0)[2:-1]

#     return str(eval(code, res))

# def process(value):
#     if isinstance(value, str):
#         return re.sub(r'\$\{[^}]*\}', interpret, value)

#     if isinstance(value, list):
#         return [process(item) for item in value]

#     if isinstance(value, dict):
#         return {process(key): process(val) for key, val in value.items()}

#     return value

# res = {
#     'x': 1,
#     'y': [1,2]
# }

# data = '''
# {
#     "a": [
#         "hello", 2, null, "hi", ["who"]
#     ],
#     "b": "hello",
#     "null": null,
#     "2": {},
#     "c": {
#         "x": 1,
#         "y": "${2+4} my boy ${y[1]}",
#         "z": ["a", "b"]
#     }
# }
# '''

# result = process(json.loads(data, object_hook=process))

# print(result)

# (r'(~*)\$([a-zA-Z_][a-zA-Z0-9_]*)(?=\s|\$|$)')
# (r'(~*)\$`((?:[^`~]|~~|~`)*?)`')

# (r'(~*)\$([a-zA-Z_][a-zA-Z0-9_]*)(?=\s|\$|$)')
# pattern = r'(~*)\$(`((?:[^`~]|~~|~`)*?)`|([a-zA-Z_][a-zA-Z0-9_]*)(?=\s|\$|$))'

# text = "~~$`'2+4~~$ab '` my boy $bc hi $de"

# def changer(match: re.Match):
#     print(f"{list(enumerate(match.groups(), start=1))}    --->   {match.group(4)}")
#     print()
#     return match.group()

# newtext = re.sub(pattern, changer, text)
# print(newtext)

# [(1, '~~'), (2, "`'2+4~~$ab '`"), (3, "'2+4~~$ab '"), (4, None)] # 1, 3

# [(1, ''), (2, 'bc'), (3, None), (4, 'bc')] # 1, 4

# [(1, ''), (2, 'de'), (3, None), (4, 'de')]