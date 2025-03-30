# @Coding: UTF-8
# @Time: 2025/3/29 23:28
# @Author: xieyang_ls
# @Filename: request_result.py

class Result:

    def __init__(self, code: int, data: object, message: str):
        self.code = code
        self.data = data
        self.message = message

    @classmethod
    def SUCCESS(cls, data: object) -> object:
        return Result(code=20001, data=data, message="Request is SUCCESS")

    @classmethod
    def WARN(cls, message: str) -> object:
        return Result(code=40001, data=None, message=message)

    @classmethod
    def ERROR(cls, message: str) -> object:
        return Result(code=50002, data=None, message=message)
