def dummy(fn):
    
    def wraqpper():
        print("before")
        fn()
        print("after")
    return wraqpper

@dummy
def hello():
    print("Hello")


hello()




