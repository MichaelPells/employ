module = input("Module: ")
file = open("/data/user/0/ru.iiec.pydroid3/files/arm-linux-androideabi/lib/python3.8/"+module+".py").read()
open(module.replace("/","_")+".py","w").write(file)