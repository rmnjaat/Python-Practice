## decorator mean function accepting other function as paramter

##ttl default 10 sec
import time
from time import sleep

# Both are the same call, should hit the same cache entry.

# Problem with tuple:


# tuple({'b': 2, 'c': 3}.items())  # → (('b',2), ('c',3))
# tuple({'c': 3, 'b': 2}.items())  # → (('c',3), ('b',2))  ❌ different key!
# With frozenset:


# frozenset({'b': 2, 'c': 3}.items())  # → frozenset({('b',2), ('c',3)})
# frozenset({'c': 3, 'b': 2}.items())  # → frozenset({('b',2), ('c',3)})  ✅ same!
# Order doesn't affect frozenset — so same kwargs always produce the same cache key.

CACHE = {}

def cache(ttl=10):
    def decorator(fun):
        def wrapper(*args, **kwargs):
            key = (fun.__name__, args, frozenset(kwargs.items()))
            if key in CACHE:
                result, expires_at = CACHE[key]
                if time.time() < expires_at:
                    return result
                del CACHE[key]
            result = fun(*args, **kwargs)
            CACHE[key] = (result, time.time() + ttl)
            return result
        return wrapper
    return decorator


@cache(3)
def f1(a, b) -> int:
    print("starting f1")
    return a + b

@cache(5)
def f2(a, b=1) -> str:
    print("starting f2")
    return str(a + b)


print(f2(1,2))
sleep(5)
print(f2(1,2))
sleep(2)
print(f2(1,2))

## now probelm is  How this wil be behaving in the fast api server ?  in parallel provcessing environment

# Server have 4 worker , then each will have there own cache  dict ,  
    #1. if sync handlers  then , multiple threasdpool threads running parallly then casue race condition 
    
    #2. if async -> then if db call is await ,   then till hat it will ruin in even loop.
        # other  option is make this             result = fun(*args, **kwargs) call  or dump this call to the  other executor , async.run_in_executor().

    ## read operations are  race condition safe , but wile writing in cache u have to a condition like  if it is locked then do not wrtie just return the call.
    ## duplicate db operations are there..