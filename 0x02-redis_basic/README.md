## 02 - Redis basic

![What is Redis?](redis.jpeg)

### Resources

- [Redis Crash Course Tutorial](https://www.youtube.com/watch?v=Hbt56gFj998 "Redis Crash Course Tutorial")
- [Redis commands](https://redis.io/commands/ "Redis commands")
- [Redis python client](https://redis-py.readthedocs.io/en/stable/ "Redis python client")
- [How to Use Redis With Python](https://realpython.com/python-redis/ "How to Use Redis With Python")

### Learning Objectives

- Learn how to use redis for basic operations
- Learn how to use redis as a simple cache

### Install Redis on Ubuntu 18.04

```sh
$ sudo apt-get -y install redis-server
$ pip3 install redis
$ sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
```

### Use Redis in a container

Redis server is stopped by default - when you are starting a container, you should start it with: `service redis-server start`

### Tasks

<details>
<summary>0. Writing strings to Redis</summary>

Write a class named `Cache`. In the `__init__` method, instantiate the Redis client and assign it to a private variable `_redis` (you can do this using `redis.Redis()`). Then, clear the instance using the `flushdb` method.

Next, define a `store` method that accepts an argument `data` and yields a string. This method should create a random key (for instance, by using `uuid`), save the input data in Redis using this random key, and then output the key.

Don't forget to correctly annotate the types in the `store` method. Keep in mind that `data` could be of type `str`, `bytes`, `int`, or `float`.

```sh
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
import redis

Cache = __import__('exercise').Cache

cache = Cache()

data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))

bob@dylan:~$ python3 main.py
3a3e8231-b2f6-450d-8b0e-0f38f16e8ca2
b'hello'
bob@dylan:~$
```

**File:**

- `exercise.py`
</details>

<details>
<summary>1. Reading from Redis and recovering original type</summary>

Redis permits the storage of strings, bytes, and numbers (including lists of these types). Any single elements you store will be returned as a byte string. For instance, if you store `"a"` as a UTF-8 string, it will be returned as `b"a"` when retrieved from the server.

In this task, we will develop a `get` method that accepts a `key` string argument and an optional `Callable` argument named `fn`. This callable will be utilized to transform the data back to the required format.

Ensure to maintain the original behavior of `Redis.get` if the key is not found.

Additionally, create two new methods: `get_str` and `get_int`. These methods will automatically parameterize `Cache.get` with the appropriate conversion function.

```sh
cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value
```

**File:**

- `exercise.py`
</details>

<details>
<summary>2. Incrementing values</summary>

Get to know the `INCR` command and its equivalent in Python.

In this exercise, we will develop a system to track the number of times the methods of the `Cache` class are invoked.

Above the `Cache` class, define a decorator named `count_calls` that accepts a single `method` `Callable` argument and yields a `Callable`.

Use the qualified name of the `method` (obtained using the `__qualname__` dunder method) as a key.

Construct and return a function that increases the count for that key each time the method is invoked and yields the value returned by the original method.

Keep in mind that the first argument of the wrapped function will be `self`, which is the instance itself, allowing you to access the Redis instance.

A useful tip: when defining a decorator, it's beneficial to use `functool.wraps` to preserve the original function’s name, docstring, etc. Ensure you use it as described [here](https://docs.python.org/3.7/library/functools.html#functools.wraps "here").

Apply the `count_calls` decorator to the `Cache.store` method.

```sh
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache

cache = Cache()

cache.store(b"first")
print(cache.get(cache.store.__qualname__))

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))

bob@dylan:~$ ./main.py
b'1'
b'3'
bob@dylan:~$
```

**File:**

- `exercise.py`
</details>

<details>
<summary>3. Storing lists</summary>

Get acquainted with Redis commands such as `RPUSH`, `LPUSH`, `LRANGE`, and so on.

In this task, we will construct a decorator named `call_history` to keep a record of the inputs and outputs for a specific function.

Each time the original function is invoked, we will add its input parameters to one list in Redis, and store its output in another list.

In `call_history`, use the decorated function’s qualified name and append `":inputs"` and `":outputs"` to form keys for the input and output lists, respectively.

`call_history` takes a single parameter named `method` that is a `Callable` and returns a `Callable`.

In the new function that the decorator will return, use `rpush` to append the input arguments. Keep in mind that Redis can only store strings, bytes, and numbers. Therefore, we can simply use `str(args)` to normalize. We can disregard potential `kwargs` for now.

Run the wrapped function to get the output. Store the output using `rpush` in the `"...:outputs"` list, then return the output.

Decorate `Cache.store` with `call_history`.

```sh
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache

cache = Cache()

s1 = cache.store("first")
print(s1)
s2 = cache.store("secont")
print(s2)
s3 = cache.store("third")
print(s3)

inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))

bob@dylan:~$ ./main.py
04f8dcaa-d354-4221-87f3-4923393a25ad
a160a8a8-06dc-4934-8e95-df0cb839644b
15a8fd87-1f55-4059-86aa-9d1a0d4f2aea
inputs: [b"('first',)", b"('secont',)", b"('third',)"]
outputs: [b'04f8dcaa-d354-4221-87f3-4923393a25ad', b'a160a8a8-06dc-4934-8e95-df0cb839644b', b'15a8fd87-1f55-4059-86aa-9d1a0d4f2aea']
bob@dylan:~$
```

**File:**

- `exercise.py`
</details>

<details>
<summary>4. Retrieving lists</summary>

In this task, we will develop a `replay` function to showcase the call history of a specific function.

Utilize the keys created in previous tasks to produce the following output:

```sh
>>> cache = Cache()
>>> cache.store("foo")
>>> cache.store("bar")
>>> cache.store(42)
>>> replay(cache.store)
Cache.store was called 3 times:
Cache.store(*('foo',)) -> 13bf32a9-a249-4664-95fc-b1062db2038f
Cache.store(*('bar',)) -> dcddd00c-4219-4dd7-8877-66afbe8e7df8
Cache.store(*(42,)) -> 5e752f2b-ecd8-4925-a3ce-e2efdee08d20
```

**File:**

- `exercise.py`
</details>

<details>
<summary>5. Implementing an expiring web cache and tracker</summary>

In this exercise, we will develop a `get_page` function (prototype: `def get_page(url: str) -> str:`). The essence of the function is quite straightforward. It employs the `requests` module to fetch the HTML content of a specific URL and returns it.

Begin in a fresh file named `web.py` and avoid reusing the code written in `exercise.py`.

Within `get_page`, keep track of the number of times a specific URL was accessed in the key `"count:{url}"` and cache the result with a lifespan of 10 seconds.

Tip: Use `http://slowwly.robertomurray.co.uk` to mimic a slow response and test your caching mechanism.

Bonus: Implement this use case using decorators.

**File:**

- `web.py`
</details>
