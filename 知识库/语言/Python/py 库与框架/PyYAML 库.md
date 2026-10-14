# PyYAML Documentation

https://pyyaml.org/wiki/PyYAMLDocumentation

停止更新

```py
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# ...

data = load(stream, Loader=Loader)

# ...

output = dump(data, Dumper=Dumper)
```

```py
import yaml
document = """
  a: 1
  b:
    c: 3
    d: 4
"""
print yaml.dump(yaml.load(document))

# a: 1
# b: {c: 3, d: 4}
```

## YAML tags and Python types

- `!!python/object/apply:module.f`
    `value of f(...)`

### ⚔️ Objects

Any pickleable object can be serialized using the !!python/object tag:

```yaml
!!python/object:module.Class { attribute: value, ... }
```

In order to support the pickle protocol, two additional forms of the !!python/object tag are provided:

```yaml
!!python/object/new:module.Class
args: [argument, ...]
kwds: {key: value, ...}
state: ...
listitems: [item, ...]
dictitems: [key: value, ...]

!!python/object/apply:module.function
args: [argument, ...]
kwds: {key: value, ...}
state: ...
listitems: [item, ...]
dictitems: [key: value, ...]
```

If only the args field is non-empty, the above records can be shortened:

```yaml
!!python/object/new:module.Class [argument, ...]

!!python/object/apply:module.function [argument, ...]
```

> 导入任意模块的语句

```yaml
!!python/object/apply:subprocess.run [["ls", "-al"]]
```