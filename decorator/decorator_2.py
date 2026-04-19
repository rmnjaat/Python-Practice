

# passing th arguments:

    # *args -> positonal argument
    # **kwarg ->  parametized args



def dummy(fn):
    def wraqpper( *args):
        print("before")
        print("args : ", args)
        fn(*args)
        print("after")
    return wraqpper

@dummy
def hello(a,b):
    print("Hello")
    print(a,"------",b)



# hello(1 ,2)
hello(1 ) # breaks. 
