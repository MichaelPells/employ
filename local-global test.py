def a():
    x = 1
    y = 2
    locals().pop("x")
    print(locals())
a()
