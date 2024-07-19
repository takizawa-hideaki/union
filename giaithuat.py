s = str(input())
a = "ing"
b = "ly"
if len(s)>3:
    if s[-3:-1]!= a:
        s+=a
        print(s)
    else:
        s+=b
        print(s)
        
else:
    print(s)