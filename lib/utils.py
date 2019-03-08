#!/usr/bin/env python
# encoding: utf-8
import types
import linecache


from thriftpy2.thrift import TType

def build_default_class_arr(req_class):
    if req_class == TType.STRING:
        value = ""
    else:
        value = 0
    return value

def build_default_class(req_class):
    set_k_v = []

    for key,value in getattr(req_class, "default_spec"):
        for _,value_arr in getattr(req_class, 'thrift_spec').items():
            if value_arr[1] == key:
                type = value_arr[0]
                k_stru = value_arr[2]

                if type == TType.STRING:
                    value = ""
                elif type == TType.STRUCT:
                    value = build_default_class(k_stru)
                elif type in [TType.LIST]:
                    value = [build_default_class_arr(k_stru)]
                elif type == TType.MAP:
                    value = {}
                else:
                    value = 0

                set_k_v.append(value)
                continue
        if value == None:
            print "ERROR ", key, value
    req = req_class(*set_k_v)
    return req

def init_func_generator(cls, method, spec):
    """Generate `method_name` function based on TPayload.default_spec
    cls: class_name

    For example::
        spec = [('name', 'Alice'), ('number', None)]
    will generate a types.FunctionType object representing::
        def method(self, name='Alice', number=None):
            self.name = name
            self.number = number
    """
    varnames, defaults = zip(*spec)

    args = ', '.join(map('{0[0]}={0[1]!r}'.format, spec))
    init = "def " + method + "(self, {}):\n".format(args)
    init += "\n".join(map('    self.{0} = {0}'.format, varnames))

    init += '\n    resp = self.gen_response("' + method + '")'

    #init += '\n    RESP_CLASS = getattr(self.service, "' + method + '_result")'
    #init += '\n    resp = build_class(RESP_CLASS, self.resp_data.get(' + method + ', None))'
    init += '\n    return resp\n'

    name = '<generated {}.' + method + '>'.format(cls)
    code = compile(init, name, 'exec')
    func = next(c for c in code.co_consts if isinstance(c, types.CodeType))

    # Add a fake linecache entry so debuggers and the traceback module can
    # better understand our generated code.
    linecache.cache[name] = (len(init), None, init.splitlines(True), name)

    return types.FunctionType(func, {}, argdefs=defaults)

def build_json_arr(arr):
    req_data = []
    for v_in_list in arr:
        if hasattr(v_in_list, "__dict__"):
            req_data.append(build_json(v_in_list))
        elif isinstance(v_in_list, list):
            req_data.append(build_json_arr(v_in_list))
        else:
            req_data.append(v_in_list)
    return req_data

def build_json(req_class):
    '''
        input: req_class is a classs object
        output: req_data  is a dict
    '''
    req_data = {}
    for key,value in req_class.__dict__.items():
        if hasattr(value, "__dict__"):
            req_data[key] = build_json(value)
        elif isinstance(value, list):
            req_data[key] = build_json_arr(value)
        else:
            req_data[key] = value
    return req_data


def build_class_arr(k_stru, arr):
    value = []
    for v_in_list in arr:
        if isinstance(v_in_list, dict):
            value.append(build_class(k_stru[1], v_in_list))
        elif isinstance(v_in_list, list):
            value.append(build_class_arr(k_stru[1], v_in_list))
        else:
            value.append(v_in_list)
    return value


def build_class(req_class, req_data):
    '''
    input: req_class is a classs object
    input: req_data  is a dict

    TODO. only consider dict, list
    '''
    if req_data == None:
        return build_default_class(req_class)

    set_k_v = []
    for key in req_class.__init__.__code__.co_varnames:
        if key == 'self':
            continue
        elif key in req_data.keys():
            if isinstance(req_data[key], dict):
                k_stru = getattr(req_class, '_tspec')[key][1][1]
                value = build_class(k_stru, req_data[key])
            elif isinstance(req_data[key], list):
                k_stru = getattr(req_class, '_tspec')[key][1][1]
                value = build_class_arr(k_stru, req_data[key])
            else:
                value = req_data[key]
        else:
            value = None
        set_k_v.append(value)
    req = req_class(*set_k_v)
    return req

if __name__ == "__main__":
    import thriftpy
    import json

    thrift_file = ""
    module_name = ""
    req_class_name = ""
    resp_class_name = ""


    with open("") as fd:
        req_data = json.loads(fd.read())

    microservice_thrift = thriftpy.load(thrift_file, module_name)
    REQ_CLASS = getattr(microservice_thrift, req_class_name)
    RESP_CLASS = getattr(microservice_thrift, resp_class_name)

    req = build_class(REQ_CLASS, req_data)
    resp = build_json(req)
    print json.dumps(resp)
