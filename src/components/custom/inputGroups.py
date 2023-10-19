# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:33:41 2023

@author: jim

Some custom functionality for column-lists of input groups which can be generated from dictionaries (inputGroup) or lists of dictionaries (inputGroupList)
requires textScripting module only for subscripts and superscripts. 
"""

from dash import html
import dash_bootstrap_components as dbc

# from . import textScripting as ts

def stripKeys(dictIn,keys):
    """Generic function which returns a copy of a dictionary with the specified keys removed.
    keys specified need not be in the inputted dictionary"""
    
    dictOut = dictIn.copy()
    for key in keys:
        if key in dictOut:
            dictOut.pop(key,None)
    return dictOut

def inputGroup(name:str, unit:str, component_id:str, value=None, varType="number",placeholder='-') -> dbc.InputGroup:
    """ A template function for a standard number input group with units. For pattern matching ids, component_id should be a dictionary"""
    
    
    # # parse for sub and super-scripting
    # if scripting:
    #     name = ts.parseAll(name)
    #     unit = ts.parseAll(unit)

    
    # build input group
    return dbc.InputGroup(
                [
                    dbc.InputGroupText(name,className='input-group-label'),
                    dbc.Input(placeholder=placeholder, type=varType,id=component_id,value=value),
                    dbc.InputGroupText(unit),
                ],
                className="mb-3",
            )


def inputGroupList(title:str, inputDicts:[dict], index:int=None, divClassName:str=None)->html.Div:
    """A template function for creating a vertical column/list of input groups given lists of dicts each having keys: 'name', 'unit',
    optional dbc.Input keywords ('type', 'placeholder', and 'value'), and any keys associated with the component id. Any keys beyond name, unit, and the above dbc keywords
    specified will be used in the component id dictionary.  If only one key besides name, unit, and value are specified, the component id will be a string (no pattern matching).
    Title can be any component (html, dbc, or dcc) type object or a string"""
    
    # pull out non-id related data for required keys ('name' and 'unit')
    names = [inputDict['name'] for inputDict in inputDicts]
    units = [inputDict['unit'] for inputDict in inputDicts]
    # pull out non-id related data for optional keys ('value', 'placeholder', and 'type')
    values = [inputDict['value'] if ('value' in inputDict) else None for inputDict in inputDicts]
    types = [inputDict['type'] if ('type' in inputDict) else "number" for inputDict in inputDicts]
    placeholders = [inputDict['placeholder'] if ('placeholder' in inputDict) else '-' for inputDict in inputDicts]
    # remove non-id data from dictionary list to leave only the id dictionary
    ids = [stripKeys(inputDict,['name','unit','value','type','placeholder']) for inputDict in inputDicts]
    
    # allow for non-str title types
    if isinstance(title,str):
        titleObj = html.H4(title)
    else:
        titleObj = title
        
    # create list of inputGroups   
    inDiv = []
    for name, unit, cid, value, varType, placeholder in zip(names,units,ids,values,types,placeholders):
        # if component id dict is length one, and no index value is given, assume id is intended to be string (i.e. no pattern matching)
        if (len(cid)==1) and (index is None):
            cid = list(cid.values())[0]
        else:
            # add index to id dictionary if supplied 
            cid['index'] = index
            
        inDiv.append(inputGroup(name,unit,cid,value=value,varType=varType,placeholder=placeholder))
        
    return html.Div(
        className=divClassName,
        children=[
            titleObj,
            html.Hr(),
            html.Div(inDiv),            
            ]
        )


def inputGroupAccordian(title:str, inputDicts:[dict], index:int=None, divClassName:str=None)->html.Div:
    """A template function for creating a vertical column/list of input groups given lists of dicts each having keys: 'name', 'unit',
    optional dbc.Input keywords ('type', 'placeholder', and 'value'), and any keys associated with the component id. Any keys beyond name, unit, and the above dbc keywords
    specified will be used in the component id dictionary.  If only one key besides name, unit, and value are specified, the component id will be a string (no pattern matching).
    Title can be any component (html, dbc, or dcc) type object or a string"""
    accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                "This is the content of the first section", title="Item 1"
            ),
            dbc.AccordionItem(
                "This is the content of the second section", title="Item 2"
            ),
            dbc.AccordionItem(
                "This is the content of the third section", title="Item 3"
            ),
        ],
        start_collapsed=True,
    ),
    )
    # pull out non-id related data for required keys ('name' and 'unit')
    names = [inputDict['name'] for inputDict in inputDicts]
    units = [inputDict['unit'] for inputDict in inputDicts]
    # pull out non-id related data for optional keys ('value', 'placeholder', and 'type')
    values = [inputDict['value'] if ('value' in inputDict) else None for inputDict in inputDicts]
    types = [inputDict['type'] if ('type' in inputDict) else "number" for inputDict in inputDicts]
    placeholders = [inputDict['placeholder'] if ('placeholder' in inputDict) else '-' for inputDict in inputDicts]
    # remove non-id data from dictionary list to leave only the id dictionary
    ids = [stripKeys(inputDict,['name','unit','value','type','placeholder']) for inputDict in inputDicts]
    
    # allow for non-str title types
    if isinstance(title,str):
        titleObj = html.H4(title)
    else:
        titleObj = title
        
    # create list of inputGroups   
    items = []
    print(names)
    for name, unit, cid, value, varType, placeholder in zip(names,units,ids,values,types,placeholders):
        print(name)
        # if component id dict is length one, and no index value is given, assume id is intended to be string (i.e. no pattern matching)
        if (len(cid)==1) and (index is None):
            cid = list(cid.values())[0]
        else:
            # add index to id dictionary if supplied 
            cid['index'] = index
        ig = inputGroup(name,unit,cid,value=value,varType=varType,placeholder=placeholder)
        items.append(dbc.AccordionItem(ig,title=name))
        
    return html.Div(
        className=divClassName,
        children=[
            titleObj,
            html.Hr(),
            html.Div(dbc.Accordion(
                items,
                
                start_collapsed=True,
            )),
            accordion,            
            ]
        )





