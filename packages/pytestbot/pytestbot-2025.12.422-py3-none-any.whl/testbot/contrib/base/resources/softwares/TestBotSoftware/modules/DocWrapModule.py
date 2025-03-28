#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PCDevice设备原子接口模块类列表
"""

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
import types
import importlib

from testbot.contrib.base.resources.devices.Device.Device import Device
from testbot.contrib.base.resources.softwares.TestBotSoftware.TestBotSoftwareWrapModuleBase import TestBotSoftwareWrapModuleBase
from testbot.resource.ModuleBase import ModuleBase
from testbot.resource.Resource import Resource
from testbot.utils.project_utils import get_all_subclasses_in_installed_projects, get_atom_module_base_class, \
    get_wrap_module_base_class


class DocWrapModule(TestBotSoftwareWrapModuleBase):
    """
    TestBot测试软件源封装接口文档模块类
    """

    def import_modules_from_atom_pkg(self) -> list:
        """
        导入原子接口包路径下的所有模块

        :param path: 包绝对路径
        :type path: str
        :param name: 包路径
        :type name: str
        :return: 模块列表
        :rtype: list
        """
        path, name = self.resource.setting.atom_pkg
        return self.resource.DocAtomModule.import_modules_from_pkg(path=path, name=name)

    def import_modules_from_wrapper_pkg(self) -> list:
        """
        导入封装接口包路径下的所有模块

        :param path: 包绝对路径
        :type path: str
        :param name: 包路径
        :type name: str
        :return: 模块列表
        :rtype: list
        """
        path, name = self.resource.setting.wrapper_pkg
        return self.resource.DocAtomModule.import_modules_from_pkg(path=path, name=name)

    def get_module_apis(self, mod: types.ModuleType) -> dict:
        """
        获取模块的API数据

        :param mod: 模块
        :type mod: ModuleType
        :return: API数据
        :rtype: dict
        """
        MOD_API_DATA = dict()
        MOD_API_DATA["mod_name"] = mod.__name__
        # 获取模块文档
        mod_doc = self.resource.DocAtomModule.get_module_doc(mod=mod)
        MOD_API_DATA["mod_doc"] = mod_doc
        # 获取模块的所有ModuleBase子类
        modulebase_classes = self.resource.DocAtomModule.get_modulebase_sub_classes(mod=mod)
        MOD_API_DATA["classes"] = []
        for clazz in modulebase_classes:
            CLASS_API_DATA = dict()
            CLASS_API_DATA["class_name"] = clazz.__name__
            # 获取类对象文档
            class_doc = self.resource.DocAtomModule.get_class_doc(clazz=clazz)
            CLASS_API_DATA["class_doc"] = class_doc
            # 获取类对象的方法对象字典
            funcs = self.resource.DocAtomModule.get_class_funcs(clazz=clazz)
            CLASS_API_DATA["funcs"] = []
            for name,func in funcs.items():
                FUNC_API_DATA = dict()
                FUNC_API_DATA["func_name"] = func.__name__
                # 获取方法对象的文档
                func_doc = self.resource.DocAtomModule.get_func_doc(func=func)
                FUNC_API_DATA["func_doc"] = func_doc
                # 获取方法对象的参数信息，如参数名称、参数类型、参数默认值
                params = self.resource.DocAtomModule.get_func_param_info(func=func)
                FUNC_API_DATA["params"] = []
                for param_name, param_type, param_default in params:
                    PARAM_API_DATA = dict()
                    PARAM_API_DATA["param_name"] = param_name
                    PARAM_API_DATA["param_type"] = param_type
                    # PARAM_API_DATA["param_default"] = param_default
                    FUNC_API_DATA["params"].append(PARAM_API_DATA)
                # 获取方法对象的返回值类型
                func_returned_type = self.resource.DocAtomModule.get_func_returned_type(func=func)
                FUNC_API_DATA["func_returned_type"] = func_returned_type
                CLASS_API_DATA["funcs"].append(FUNC_API_DATA)
            MOD_API_DATA["classes"].append(CLASS_API_DATA)
        return MOD_API_DATA

    def get_apis(self) -> list:
        """
        获取原子接口和封装接口的API数据

        :return: API数据
        :rtype: list
        """
        API_DATA = list()
        API_DATA_ENG = list()

        # 获取所有测试资源子孙类：设备、软件、服务
        subclasses = list()
        device_subclasses = self.resource.DocAtomModule.get_subclasses(clazz=Device)
        from testbot.contrib.base.resources.softwares.Software.Software import Software
        software_subclasses = self.resource.DocAtomModule.get_subclasses(clazz=Software)
        from testbot.contrib.base.resources.services.Service.Service import Service
        service_subclasses = self.resource.DocAtomModule.get_subclasses(clazz=Service)
        subclasses.extend(device_subclasses)
        subclasses.extend(software_subclasses)
        subclasses.extend(service_subclasses)
        subclasses = set(subclasses)
        for clazz in subclasses:
            RES_CLASS_API_DATA = dict()
            RES_CLASS_API_DATA_ENG = dict()
            RES_CLASS_API_DATA["测试资源类"] = clazz.__name__
            RES_CLASS_API_DATA_ENG["resource"] = clazz.__name__
            # 获取类对象文档
            class_doc = self.resource.DocAtomModule.get_class_doc(clazz=clazz)
            RES_CLASS_API_DATA["描述"] = class_doc
            RES_CLASS_API_DATA_ENG["desc"] = class_doc
            RES_CLASS_API_DATA["接口模块"] = list()
            RES_CLASS_API_DATA_ENG["modules"] = list()
            # 获取资源类对应的模块类
            for module_base_clz in [get_atom_module_base_class(resource_class=clazz), get_wrap_module_base_class(resource_class=clazz)]:
                found_subclasses = get_all_subclasses_in_installed_projects(prj_setting=self.resource.settings_mod, parent_class=module_base_clz)
                for name, subclass in found_subclasses.items():
                    if name.endswith("ModuleBase"):
                        continue
                    MOD_CLASS_API_DATA = dict()
                    MOD_CLASS_API_DATA_ENG = dict()
                    mod_clazz = subclass
                    MOD_CLASS_API_DATA["模块类名称"] = mod_clazz.__name__
                    MOD_CLASS_API_DATA_ENG["classes"] = mod_clazz.__name__
                    # 获取类对象文档
                    class_doc = self.resource.DocAtomModule.get_class_doc(clazz=mod_clazz)
                    MOD_CLASS_API_DATA["模块类描述"] = class_doc
                    MOD_CLASS_API_DATA_ENG["desc"] = class_doc
                    # 获取类对象的方法对象字典
                    funcs = self.resource.DocAtomModule.get_class_funcs(clazz=mod_clazz)
                    MOD_CLASS_API_DATA["方法"] = list()
                    MOD_CLASS_API_DATA_ENG["funcs"] = list()
                    for name, func in funcs.items():
                        FUNC_API_DATA = dict()
                        FUNC_API_DATA_ENG = dict()
                        FUNC_API_DATA["方法名称"] = func.__name__
                        FUNC_API_DATA_ENG["name"] = func.__name__
                        # 获取方法对象的文档
                        func_doc = self.resource.DocAtomModule.get_func_doc(func=func)
                        FUNC_API_DATA["方法描述"] = func_doc
                        FUNC_API_DATA_ENG["desc"] = func_doc
                        # 获取方法对象的参数信息，如参数名称、参数类型、参数默认值
                        params = self.resource.DocAtomModule.get_func_param_info(func=func)
                        FUNC_API_DATA["方法参数"] = list()
                        FUNC_API_DATA_ENG["params"] = list()
                        for param_name, param_type, param_default in params:
                            PARAM_API_DATA = dict()
                            PARAM_API_DATA_ENG = dict()
                            PARAM_API_DATA["参数名称"] = param_name
                            PARAM_API_DATA_ENG["name"] = param_name
                            PARAM_API_DATA["参数类型"] = param_type
                            PARAM_API_DATA_ENG["type"] = param_type
                            param_desc, param_type_name, param_default = self.resource.DocAtomModule.get_func_param_info_from_func_doc(func=func, arg_name=param_name)
                            PARAM_API_DATA["参数描述"] = param_desc
                            PARAM_API_DATA_ENG["desc"] = param_desc
                            PARAM_API_DATA["参数默认值"] = param_default
                            PARAM_API_DATA_ENG["default"] = param_default
                            FUNC_API_DATA["方法参数"].append(PARAM_API_DATA)
                            FUNC_API_DATA_ENG["params"].append(PARAM_API_DATA_ENG)
                        # 获取方法对象的返回值描述
                        func_returned_type, func_returned_desc = self.resource.DocAtomModule.get_func_return_info_from_func_doc(func=func)
                        FUNC_API_DATA["返回值描述"] = func_returned_desc
                        FUNC_API_DATA_ENG["returned_desc"] = func_returned_desc
                        # 获取方法对象的返回值类型
                        func_returned_type = self.resource.DocAtomModule.get_func_returned_type(func=func)
                        FUNC_API_DATA["返回值类型"] = func_returned_type
                        FUNC_API_DATA_ENG["returned_type"] = func_returned_type
                        MOD_CLASS_API_DATA["方法"].append(FUNC_API_DATA)
                        MOD_CLASS_API_DATA_ENG["funcs"].append(FUNC_API_DATA_ENG)
                    RES_CLASS_API_DATA["接口模块"].append(MOD_CLASS_API_DATA)
                    RES_CLASS_API_DATA_ENG["modules"].append(MOD_CLASS_API_DATA_ENG)
            API_DATA.append(RES_CLASS_API_DATA)
            API_DATA_ENG.append(RES_CLASS_API_DATA_ENG)
        return API_DATA, API_DATA_ENG
