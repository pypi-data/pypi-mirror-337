from valueapiconnector import *
from datetime import time


def test():
    connector = ValueAPIConnector("http://localhost/")
    context = connector.get_context(
        "testxxx",
        auth_token="jknafsulihfihuo3rwuierliuwehflsdcjkvslkjdlhiu787iu",
    )
    context.update_auth_token("jknafsulihfihuo3rwuierliuwehflsdcjkvslkjdlhiu787iu")
    x = context.get_value("hallo welt", ValueDataType.INTEGER_LIST)
    print(x.pull().unwrap())
    x.push([1, 2, 3])
    print(x.pull().unwrap())
    x.delete()
    x.pull().when_okay(lambda val: print(val)).when_error(
        lambda err: print("was error :/" + err)
    )

    y = context.get_value("json_test", ValueDataType.JSON)
    print(y.pull().unwrap())
    y.push({"key1": 1, "key2": "Hallo Welt"})
    print(y.url)
    print(y.pull().unwrap())

    z = context.get_value("datetest", ValueDataType.TIME)
    print(z.pull().unwrap())
    z.push(time.fromisoformat("08:11:12"))
    print(z.pull().unwrap())

    class TestDataClass(ValueABC):
        def __init__(self):
            super().__init__(context)
            self.z = "Hello World"

        def __str__(self) -> str:
            return f"{self.__dict__}"

    test_obj = TestDataClass()
    print(test_obj)
    test_obj.x = 24
    test_obj.y = [4, 5]
    print(test_obj)

    test_obj2 = TestDataClass()
    print(test_obj2)

    failure_value = context.get_value("test_failue", ValueDataType.DATETIME)
    failure_value.push("Hello world")
    failure_value.pull().when_error(
        lambda err: print("This is the error message", err)
    ).when_okay(lambda val: print("This is my value :)", val))


if __name__ == "__main__":
    test()
