# @Coding: UTF-8
# @Time: 2024/9/22 17:15
# @Author: xieyang_ls
# @Filename: spirit_application.py
import os

import cgi

import json

import inspect

import importlib.util

from threading import Lock

from typing import Callable

from types import FunctionType, MethodType

from pyutils_spirit.style import draw_spirit_banner

from logging import info, INFO, basicConfig, exception

from http.server import BaseHTTPRequestHandler, HTTPServer

from pyutils_spirit.spirit_container.request_result import Result

from pyutils_spirit.util import Assemble, HashAssemble, Set, HashSet

from pyutils_spirit.spirit_container.multipart_file import MultipartFile

from pyutils_spirit.exception import NoneSignatureError, BusinessException, SpiritContainerServiceException

basicConfig(level=INFO)


class SpiritApplication:
    start_status: bool = None

    __unified_response_type__: bool = None

    __unique_modules: Set[object] = None

    __current_file__: str = None

    __current_work_dir__: str = None

    __signatures: tuple[str] = None

    __container: Assemble[str, object] = None

    __auto_wired_set__: set[object] = None

    __method_types: tuple[str] = None

    __interrupt_handlers: tuple[str] = None

    __lock: Lock = None

    __controller_paths_set: set[str] = None

    __interceptor_paths_set: set[str] = None

    __interceptor_function_before__: Callable[[BaseHTTPRequestHandler], tuple[int, bool]] = None

    __interceptor_function_after__: Callable[[BaseHTTPRequestHandler], None] = None

    def __init__(self, __file__):
        SpiritApplication.__lock = Lock()
        self.__unique_modules = HashSet()
        self.__current_file__ = os.path.basename(__file__)
        SpiritApplication.__signatures = ("Component", "Mapper", "Service", "Controller", "WebSocketServer")
        SpiritApplication.__container = HashAssemble()
        self.__auto_wired_set__ = set()
        SpiritApplication.__method_types = ("GET", "POST", "PUT", "DELETE")
        SpiritApplication.__controller_paths_set = set()
        SpiritApplication.__interceptor_paths_set = set()

    def start(self, host: str, port: int, unified_response_type: bool = True):
        SpiritApplication.__lock.acquire()
        try:
            if SpiritApplication.start_status is True:
                raise SpiritContainerServiceException
            SpiritApplication.start_status = True
        finally:
            SpiritApplication.__lock.release()
        SpiritApplication.__unified_response_type__ = unified_response_type
        draw_spirit_banner()
        self.__current_work_dir__ = os.getcwd()
        self.__scan_modules(self.__current_work_dir__)
        self.__start_service(host=host, port=port)

    def __scan_modules(self, work_directory: str):
        for dirpath, dirnames, filenames in os.walk(work_directory):
            for file_name in filenames:
                if file_name == "__init__.py":
                    continue
                if file_name.endswith('.py'):
                    file_path = os.path.join(dirpath, file_name)
                    self.__load_module(file_path)
        self.__auto_injected()

    def __load_module(self, file_path):
        current_file_path = os.path.abspath(self.__current_file__)
        if file_path == current_file_path:
            return None
        module_path = file_path[:-3]
        module_name = os.path.basename(module_path)
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.__analyze_module(module)

    def __analyze_module(self, module) -> None:
        for name, obj in inspect.getmembers(module):
            if self.__unique_modules.__contains__(obj) is False:
                self.__unique_modules.add(obj)
                if obj is None:
                    continue
                if isinstance(obj, FunctionType | type):
                    decorator = getattr(obj, "__decorator__", None)
                    if decorator in SpiritApplication.__signatures:
                        self.__auto_wired_set__.add(obj())
                        if decorator == "Controller":
                            params = getattr(obj, "__decorator_params__")
                            SpiritApplication.__controller_paths_set.add(params)

    def __auto_injected(self) -> None:
        for instance in self.__auto_wired_set__:
            for method_name, method in inspect.getmembers(instance):
                if isinstance(method, MethodType):
                    decorator = getattr(method, "__decorator__", None)
                    if decorator == "Resource":
                        if hasattr(method, "__self__") and isinstance(method.__self__, type):
                            method(cls=type(instance), resources={})
                        else:
                            method(self=instance, resources={})

    def __start_service(self, host: str, port: int):
        server_address: tuple[str, int] = (host, port)
        service = HTTPServer(server_address, self.RequestHandler)
        info("Spirit Container Service Startup successfully")
        info(f"Listening on Server: {host}:{port}")
        service.serve_forever()

    @classmethod
    def set_interceptor_paths(cls, interceptor_paths: set[str]) -> None:
        cls.__interceptor_paths_set = interceptor_paths

    @classmethod
    def set_interceptor_before_function(cls,
                                        interceptor_before_function:
                                        Callable[[BaseHTTPRequestHandler], tuple[int, bool]]) -> None:
        cls.__interceptor_function_before__ = interceptor_before_function

    @classmethod
    def set_interceptor_after_function(cls,
                                       interceptor_after_function:
                                       Callable[[BaseHTTPRequestHandler], None]) -> None:
        cls.__interceptor_function_after__ = interceptor_after_function

    @classmethod
    def __do_interceptor_function__(cls, request_path: str) -> bool:
        if len(cls.__interceptor_paths_set) == 0:
            return False
        for path in cls.__interceptor_paths_set:
            path_list = request_path.split(path, maxsplit=1)
            if len(path_list) == 1:
                return False
            if path_list[0] == "" and path_list[1][0] == "?":
                return True
        return False

    @classmethod
    def get_func_kwargs(cls, path: str, method_type: str) -> [object, callable, dict]:
        cls.__lock.acquire()
        try:
            for controller_path in cls.__controller_paths_set:
                path_list = path.split(controller_path, maxsplit=1)
                if len(path_list) == 1:
                    continue
                if path_list[0] != "":
                    continue
                controller_func_path = path_list[1]
                if len(path_list) == 2 and controller_func_path[0] == "/":
                    controller = cls.__container.get(controller_path)
                    for method_name, method in inspect.getmembers(controller):
                        decorator = getattr(method, "__decorator__", None)
                        if decorator == method_type:
                            func_path = getattr(method, "__decorator_path__")
                            func_path_list = controller_func_path.split(func_path, maxsplit=1)
                            if len(func_path_list) == 1:
                                continue
                            func_args = func_path_list[1]
                            if len(func_path_list) > 1:
                                if func_args == "":
                                    return method, None
                                elif func_args[0] == "?":
                                    kwargs = list()
                                    for param in func_args.split("?")[1].split("&"):
                                        if "=" in param:
                                            value = param.split("=")[1]
                                            kwargs.append(value)
                                    return method, kwargs
        finally:
            cls.__lock.release()
        raise ValueError(f"please check the path {path} of {method_type} Method")

    class RequestHandler(BaseHTTPRequestHandler):

        __data__ = None

        __response__ = None

        __is_interceptor__: bool = False

        __is_pass__: bool = False

        __response_code__: int = 200

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __request_exception_advice__(self, e: Exception):
            exception(e)
            self.__response_code__ = 500
            self.__response__ = str(e)
            if isinstance(e, BusinessException):
                if SpiritApplication.__unified_response_type__ is True:
                    self.__response__ = Result.WARN(self.__response__)
            else:
                if SpiritApplication.__unified_response_type__ is True:
                    self.__response__ = Result.ERROR(self.__response__)

        def __is_interceptor_func__(self):
            self.__is_interceptor__ = SpiritApplication.__do_interceptor_function__(self.path)
            if self.__is_interceptor__:
                if SpiritApplication.__interceptor_function_before__ is not None:
                    self.__response_code__, self.__is_pass__ = SpiritApplication.__interceptor_function_before__(self)
                    if self.__is_pass__ is False:
                        self.__response__ = Result.WARN(f"the request '{self.path}' is be intercepted")
                        return True
            return False

        def __request_end_func__(self):
            self.send_response(self.__response_code__)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.__response__).encode('utf-8'))
            if self.__is_interceptor__ and self.__is_pass__:
                if SpiritApplication.__interceptor_function_after__ is not None:
                    SpiritApplication.__interceptor_function_after__(self)

        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

        def do_GET(self):
            try:
                if self.__is_interceptor_func__():
                    return None
                func, kwargs = SpiritApplication.get_func_kwargs(self.path, "GET")
                if isinstance(kwargs, list):
                    self.__response__ = func(*kwargs)
                else:
                    self.__response__ = func()
                if SpiritApplication.__unified_response_type__ is True:
                    self.__response__ = Result.SUCCESS(self.__response__)
            except Exception as e:
                self.__request_exception_advice__(e)
            finally:
                self.__request_end_func__()

        def __get_post_file__(self, post_body_length):
            if self.headers['Content-Type'].startswith('multipart/form-data'):
                # 解析请求体
                form = cgi.FieldStorage(fp=self.rfile,
                                        headers=self.headers,
                                        environ={'REQUEST_METHOD': 'POST'})
                # print(f"form_list: {form.list}")
                # print(f"form_value: {form.value}")
                # print(f"form_keys(): {form.keys()}")
                for key in form.keys():
                    print(key, form.getvalue(key, None), type(form.getvalue(key, None)))
                    print()
                # 处理文件
                if "file" in form:
                    temp_file_handler = form["file"]
                elif "data" in form:
                    temp_file_handler = form["data"]
                else:
                    self.send_response(400)
                    self.end_headers()
                    raise FileNotFoundError("Post Method: Content-Type is multipart/form-data But No file uploaded")
                # 创建临时文件并写入上传的内容
                file = MultipartFile(temp_file_handler=temp_file_handler.file)
                return file
            else:
                data = self.rfile.read(post_body_length)
                return json.loads(data)

        def do_POST(self):
            post_body_length = int(self.headers['Content-Length'])
            try:
                if self.__is_interceptor_func__():
                    return None
                func, kwargs = SpiritApplication.get_func_kwargs(self.path, "POST")
                if post_body_length > 0:
                    self.__data__ = self.__get_post_file__(post_body_length)
                else:
                    self.__response_code__ = 400
                    raise ValueError("Post Method: Request Body must be not empty.")
                if isinstance(kwargs, list):
                    self.__response__ = func(*kwargs, self.__data__)
                else:
                    self.__response__ = func(self.__data__)
                if SpiritApplication.__unified_response_type__ is True:
                    self.__response__ = Result.SUCCESS(self.__response__)
            except Exception as e:
                self.__request_exception_advice__(e)
            finally:
                if isinstance(self.__data__, MultipartFile):
                    self.__data__.close()
                self.__request_end_func__()

        def do_PUT(self):
            put_body_length = int(self.headers['Content-Length'])
            if put_body_length > 0:
                data = self.rfile.read(put_body_length)
                self.__data__ = json.loads(data)
            else:
                self.__data__ = None
            try:
                if self.__is_interceptor_func__():
                    return None
                func, kwargs = SpiritApplication.get_func_kwargs(self.path, "PUT")
                if isinstance(kwargs, list):
                    if self.__data__ is None:
                        self.__response__ = func(*kwargs)
                    else:
                        self.__response__ = func(*kwargs, self.__data__)
                else:
                    if self.__data__ is None:
                        self.__response__ = func()
                    else:
                        self.__response__ = func(self.__data__)
                if SpiritApplication.__unified_response_type__ is True:
                    self.__response__ = Result.SUCCESS(self.__response__)
            except Exception as e:
                self.__request_exception_advice__(e)
            finally:
                self.__request_end_func__()

        def do_DELETE(self):
            content = self.headers['Content-Length']
            if content is not None:
                delete_body_length = int(content)
                if delete_body_length > 0:
                    data = self.rfile.read(delete_body_length)
                    self.__data__ = json.loads(data)
                else:
                    self.__data__ = None
            else:
                self.__data__ = None
            try:
                if self.__is_interceptor_func__():
                    return None
                func, kwargs = SpiritApplication.get_func_kwargs(self.path, "DELETE")
                if isinstance(kwargs, list):
                    if self.__data__ is None:
                        self.__response__ = func(*kwargs)
                    else:
                        self.__response__ = func(*kwargs, self.__data__)
                else:
                    if self.__data__ is None:
                        self.__response__ = func()
                    else:
                        self.__response__ = func(self.__data__)
                if SpiritApplication.__unified_response_type__ is True:
                    self.__response__ = Result.SUCCESS(self.__response__)
            except Exception as e:
                self.__request_exception_advice__(e)
            finally:
                self.__request_end_func__()

    @classmethod
    def Component(cls, signature: str) -> callable:
        if not isinstance(signature, str):
            raise NoneSignatureError
        if len(signature) == 0:
            raise ValueError("Component: Signature cannot be empty")

        def get_component_cls(other_cls):

            def get_component_instance(*args, **kwargs) -> object:
                instance = cls.__container.get(signature)
                if instance is None:
                    instance = other_cls(*args, **kwargs)
                    cls.__container.put(signature, instance)
                return instance

            get_component_instance.__decorator__ = "Component"
            get_component_instance.__decorator_params__ = signature
            return get_component_instance

        return get_component_cls

    @classmethod
    def Mapper(cls, signature: str) -> callable:
        if not isinstance(signature, str):
            raise NoneSignatureError
        if len(signature) == 0:
            raise ValueError("Mapper: Signature cannot be empty")

        def get_mapper_cls(other_cls):

            def get_mapper_instance(*args, **kwargs) -> object:
                instance = cls.__container.get(signature)
                if instance is None:
                    instance = other_cls(*args, **kwargs)
                    cls.__container.put(signature, instance)
                return instance

            get_mapper_instance.__decorator__ = "Mapper"
            get_mapper_instance.__decorator_params__ = signature
            return get_mapper_instance

        return get_mapper_cls

    @classmethod
    def Service(cls, signature: str) -> callable:
        if not isinstance(signature, str):
            raise NoneSignatureError
        if len(signature) == 0:
            raise ValueError("Service: Signature cannot be empty")

        def get_service_cls(other_cls):

            def get_service_instance(*args, **kwargs) -> object:
                instance = cls.__container.get(signature)
                if instance is None:
                    instance = other_cls(*args, **kwargs)
                    cls.__container.put(signature, instance)
                return instance

            get_service_instance.__decorator__ = "Service"
            get_service_instance.__decorator_params__ = signature
            return get_service_instance

        return get_service_cls

    @classmethod
    def Controller(cls, path: str) -> callable:
        if not isinstance(path, str):
            raise NoneSignatureError
        if len(path) == 0:
            raise ValueError("Controller: path cannot be empty")

        def get_controller_cls(other_cls):

            def get_controller_instance(*args, **kwargs) -> object:
                instance = cls.__container.get(path)
                if instance is None:
                    instance = other_cls(*args, **kwargs)
                    cls.__container.put(path, instance)
                return instance

            get_controller_instance.__decorator__ = "Controller"
            get_controller_instance.__decorator_params__ = path
            return get_controller_instance

        return get_controller_cls

    @classmethod
    def Resource(cls, names: list[str] | str) -> callable:
        if not isinstance(names, list | str):
            raise ValueError("Resource: the signature of type must be list or str")
        if not all(isinstance(name, str) for name in names):
            raise ValueError("All elements in the list must be strings")
        if len(names) == 0:
            raise ValueError("the names must not be empty")

        def decorator_func(func):
            def wrapper(*args, **kwargs):
                if isinstance(names, str):
                    resources = cls.__container.get(names)
                    if resources is None:
                        raise ValueError(f"the signature {names} does not exist")
                else:
                    resources = kwargs["resources"]
                    for name in names:
                        instance = cls.__container.get(name)
                        if instance is None:
                            raise ValueError(f"the signature {name} does not exist")
                        resources[name] = instance
                func(args[0], resources)

            wrapper.__decorator__ = "Resource"
            return wrapper

        return decorator_func


Component = SpiritApplication.Component
Mapper = SpiritApplication.Mapper
Service = SpiritApplication.Service
Controller = SpiritApplication.Controller
Resource = SpiritApplication.Resource
