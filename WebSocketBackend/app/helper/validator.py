from cerberus import Validator


class JSONValidator:
    def __init__(self) -> None:
        self.__validator = Validator()
    
    def switch(self, data):
        switch_schema = {
            "1": {"type":"boolean"},
            "2": {"type":"boolean"},
            "3": {"type":"boolean"},
            "4": {"type":"boolean"},
            "5": {"type":"boolean"},
            "6": {"type":"boolean"},
            "7": {"type":"boolean"},
            "8": {"type":"boolean"}
        }
        return self.__validator.validate(data, switch_schema)