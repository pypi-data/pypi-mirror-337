# Value API - Python Connector
A Python client for the [Value API Server](https://github.com/ValueAPI/Server).

## Install 
```
pip install valueapiconnector
```


## Usage
```python
from valueapiconnector import ValueApiConnector, ValueDataType, ABCValue
connector = ValueAPIConnector("https://values.my-server.com/")
# The auth token is optional
context = connector.get_context("test",
        auth_token="<my_secret_token>",
    )
context.update_auth_token("<my_secret_token>")
x = context.get_value("my_int_list", ValueDataType.INTEGER_LIST)
print(x.pull().unwrap()) # []
x.push([1, 2, 3])
print(x.pull().unwrap()) # [1, 2, 3]
x.delete()
print(x.pull().unwrap()) # []

class TestValues(ABCValue):
    def __init__(self, identifier):
        super().__init__(context, identifier)

    def __str__(self) -> str:
        return str(self.__dict__)

test_obj = TestValues(1)
print(test_obj) # {}
test_obj.x = 24
test_obj.y = [4, 5]
print(test_obj) # {x: 24, y=[4,5]}
test_obj = TestValues(1)
print(test_obj) # {x: 24, y=[4,5]}
test_obj = TestValues(2)
print(test_obj) # {}
```
