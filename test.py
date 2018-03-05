s = [1,2,3,4,5,6]
print( [ (i, t) for i ,t in reversed(list(enumerate(s)))] )

s1 = "(PERSON*"
s2 = "*)"
print(s1.strip("(*)"))
print(s2.strip("(*)"))

d = {}
a = d[1] = s
print(a)
print(d)