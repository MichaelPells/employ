if __name__ == "__main__":
    names = "bcdefghijklmnopqrst"

    a = open("a.py").read()

    for x in names:
        open(x+".py", "w").write(a)
