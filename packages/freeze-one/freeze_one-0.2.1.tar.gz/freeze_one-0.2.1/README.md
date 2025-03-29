# `freeze_one`

Like this:

```sh
pip freeze | grep freeze_one
```

But safer than string manipulation, like this:

```python
from freeze_one import freeze_one

print(freeze_one("freeze_one"))
```
