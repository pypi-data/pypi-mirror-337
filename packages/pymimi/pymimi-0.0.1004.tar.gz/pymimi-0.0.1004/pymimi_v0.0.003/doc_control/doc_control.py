import os
import base64
from typing import List, Optional, Dict, Any
from midas_api import midasapi



def new_doc():
    response = midasapi('POST', '/doc/new',{})
    if response !={'message': 'MIDAS CIVIL NX command complete'} :
        raise ValueError(response)

def open_doc(doc_path):
    doc_open = {"Argument" :doc_path}
    response = midasapi('POST', '/doc/open',doc_open)
    if response !={'message': 'MIDAS CIVIL NX command complete'} :
        raise ValueError(response)

def close_doc():
    response = midasapi('POST', '/doc/close',{})
    if response !={'message': 'MIDAS CIVIL NX command complete'} :
        raise ValueError(response)

def proj_info():
    raise ValueError('该函数暂不可用')


def save_doc():
    response = midasapi('POST', '/doc/save',{})
    if response !={'message': 'MIDAS CIVIL NX command complete'} :
        raise ValueError(response)

def save_as(doc_path:str,doc_name:str,doc_type:int= None):
    if doc_type not in (None, 1, 2):
        raise ValueError("doc_type 必须是 1、2 或 None")

    if doc_type == 1 and not doc_name.endswith((".mcb","mgb")):
        doc_name += ".mgb"
    elif doc_type == 1 and doc_name.endswith(".mgb"):
        doc_name = doc_name

    if doc_type in (2,None) and not doc_name.endswith((".mcb","mgb")):
        doc_name += ".mcb"
    elif doc_type in (2,None) and doc_name.endswith(".mcb"):
        doc_name = doc_name

    if doc_type in (None,2) and doc_name.endswith(".mgb"):
        doc_name = doc_name

    if doc_type == 1 and doc_name.endswith(".mcb"):
        doc_name = doc_name

    print(doc_name)
    full_path = os.path.join(doc_path, doc_name)
    doc_save_as = {"Argument" :full_path}
    response = midasapi('POST', '/doc/saveas',doc_save_as)
    if response !={'message': 'MIDAS CIVIL NX command complete'}:
        raise ValueError(response)

def import_json(json_path):
    # json_import = {"Argument" :json_path}
    # response = midasapi('POST', '/doc/import',json_import)
    # if response !={'message': 'MIDAS CIVIL NX command complete'} :
    #     raise ValueError(import_json)
    raise ValueError('该函数暂不可用')
    pass

def import_mct(mct_path):
    # mct_import = {"Argument" :mct_path}
    # response = midasapi('POST', '/doc/importmxt',mct_import)
    # if response !={'message': 'MIDAS CIVIL NX command complete'} :
    #     raise ValueError(import_mct)
    raise ValueError('该函数暂不可用')
    pass

def export_json(json_path:str,name:str):
    if not name.endswith(".json"):
        name += ".json"
    full_path = os.path.join(json_path, name)
    response = {"Argument" :full_path}
    if midasapi('POST', '/doc/export') !={'message': 'MIDAS CIVIL NX command complete'} :
        raise ValueError(response)

def export_mct(mct_path:str,name:str):
    raise ValueError('该函数暂不可用')
    pass


def module_scr(
        output_path: str,
        loadcase_type: str,
        loadcase_name: str,
        load_disp_opt_list: List[str],
        bndr_disp_opt_list: List[str],
        is_pre_mode: bool,
        image_name: str = "screenshot.jpg",
        run_analysis: bool = False,

        hidden: bool = False,
        view_horizontal: float = 0,
        view_vertical: float = 0,
        load_value_label: bool = False,
        load_value_exp: bool = False,
        load_value_decimal_pt: int = 1,
        bngr_list: Optional[List[str]] = None,
) :
        # required_params = {
        #     "output_path": output_path,
        #     "loadcase_type": loadcase_type,
        #     "loadcase_name": loadcase_name,
        #     "load_disp_opt_list": load_disp_opt_list,
        #     "bndr_disp_opt_list": bndr_disp_opt_list,
        #     "is_pre_mode": is_pre_mode,
        # }
        # for param_name, param_value in required_params.items():
        #     if  param_value is None:
        #         raise ValueError(f"{param_name} 是必需参数")
        #
        # valid_loadcase_types = {"ST", "CB", "CBC", "CBS"}
        # if loadcase_type not in valid_loadcase_types:
        #     raise ValueError(f"loadcase_type 必须是 {valid_loadcase_types}")
        #
        # module_scr = {"Argument": {
        #                 "UFIG_LIST" : [{
        #                     "OUTPUT_PATH" : output_path,
        #                     "RUN_ANALYSIS" : run_analysis,
        #                     "IS_PRE_MODE" : is_pre_mode,
        #                     "HIDDEN" : hidden,
        #                     "VIEW_HORIZONTAL" : view_horizontal,
        #                     "VIEW_VERTICAL" : view_vertical,
        #                     "LOADCASE_TYPE" : loadcase_type,
        #                     "LOADCASE_NAME" : loadcase_name,
        #                     "LIAD_DISP_OPT":{
        #                         "LOAD_VALUE_LABEL": load_value_label,
        #                         "LOAD_VALUE_EXP": load_value_exp,
        #                         "LOAD_VALUE_DECIMAL_PT": load_value_decimal_pt,
        #                         "LOAD_DISP_LIST":load_disp_opt_list,
        #                     },
        #                     "BNDR_DISP_OPT":{
        #                         "BNGR_LIST": bngr_list or ["ALL"],
        #                         "BNDR_DISP_OPT_LIST": bndr_disp_opt_list,
        #                     }
        #                 }]
        #             }}
        #
        # response = midasapi('POST', '/VIEW/CAPTURE', module_scr)
        #
        # if image_name.endswith((".jpg",".ipeg")):
        #     image_name = image_name
        # else:
        #     image_name += ".jpg"
        # image_path = os.path.join(output_path, image_name)
        # response_str = response['base64String']
        # image_data = base64.b64decode(response_str)
        # with open(image_path, 'wb')as f:
        #     f.write(image_data)
        raise ValueError('该函数暂不可用')
def construction_scr():
    raise ValueError('该函数暂不可用')

def analysis():
    response = midasapi('POST', '/doc/anal',{})
    if response !={'message': 'MIDAS CIVIL NX command complete'} :
        raise ValueError(response)

