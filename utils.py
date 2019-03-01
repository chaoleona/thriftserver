#!/usr/bin/env python
# encoding: utf-8

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
    from config import *

    with open(req_data_file) as fd:
        req_data = json.loads(fd.read())

    microservice_thrift = thriftpy.load(thrift_file, module_name)
    REQ_CLASS = getattr(microservice_thrift, req_class_name)
    RESP_CLASS = getattr(microservice_thrift, resp_class_name)


    req = build_class(REQ_CLASS, req_data)
    resp = build_json(req)
    print json.dumps(resp)
