
from typing import List, Optional

import os
import re

from rich import box, print
from rich.console import Console
from rich.markdown import Markdown

from pyegeria import body_slimmer
from pyegeria._globals import NO_TERMS_FOUND, NO_GLOSSARIES_FOUND, NO_TERMS_FOUND, NO_ELEMENTS_FOUND, NO_PROJECTS_FOUND, NO_CATEGORIES_FOUND
from pyegeria.egeria_tech_client import EgeriaTech
from pyegeria.md_processing_utils import extract_attribute
from pyegeria.project_manager_omvs import ProjectManager
from pyegeria.glossary_manager_omvs import GlossaryManager
ERROR = "ERROR-> "
INFO = "INFO- "
WARNING = "WARNING-> "
pre_command = "\n---\n==> Processing command:"



def process_q_name_list(egeria_client: EgeriaTech, element_type:str, txt:str )-> tuple[str,str,str,bool,bool]:
    msg = ""
    known_guid = None
    valid = True
    exists = False
    
    elements_txt = extract_attribute(txt, [element_type])

    if elements_txt is None:
        msg += f"* {INFO}No Solution Blueprints found\n"
    
    else:
        element_list = re.split(r'[,\n]+', elements_txt)
        elements = ""
        new_element_list = []
        for element in element_list:
            element_el = element.strip()
            if element_el not in element_dictionary:
                # Get the element using the generalized function

                el = get_element_by_name(egeria_client, element_type, element_el)
                if isinstance(el, str):
                    msg += (f"* {WARNING}Blueprint `{element_el}` not found -> "
                            f"Blueprints for this Solution Component won't be processed!\n")
                    el_exist = False
                    break
    
                # Extract properties using the element type name to construct property access
                properties_key = f"{element_type}Properties"
                el_qname = el[0][properties_key].get('qualifiedName', None)
    
                if el_qname not in element_dictionary:
                    el_guid = el[0]['elementHeader']['guid']
                    el_display_name = el[0][properties_key].get('displayName', None)
                    element_dictionary[el_qname] = {
                        'guid': el_guid,
                        'displayName': el_display_name
                        }
            elements = f"{el_qname}, {elements}"
            new_element_list.append(el_qname)
        if el_exist:
            elements += '\n'
            element_list = new_element_list
        else:
            elements = None