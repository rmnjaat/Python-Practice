

def dummy(fn):
    print("dummy start")
    def wraqpper( *args , **kargs):
        print("before")
        print("args : ", args)
        print("kargs : ", kargs)
        fn(*args , **kargs)
        print("after")
    print("dummy ends")
    return wraqpper

@dummy
def hello(a,b):
    print("Hello") 
    print(a,"------",b)


hello(1,b=2)



## problem sttement