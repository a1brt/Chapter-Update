import asyncio
import time

def delay(seconds):
    def decorator(f):
        async def wrapper(*args, **kwargs):
            res = f(*args, **kwargs)  
            await asyncio.sleep(seconds)
            return res
        return wrapper
    return decorator

def timer(f):
    def wrapper(*args,**kwargs):
        start = time.time()
        res = f(*args,**kwargs)
        end = time.time()
        print(f"{time.strftime('%H:%M:%S', time.localtime())}: {end - start}")
        return res
    return wrapper
