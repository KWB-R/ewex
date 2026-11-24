import dataclasses as dtc
import gc
import pandas as pd
from pathlib import Path

from ewex.models.substance import Substance
from ewex.models.treatment import Treatment
from ewex.models.matrix import Matrix

def list_substances(export_csv: bool = True):
    sub_list = []
    for obj in gc.get_objects():
        if isinstance(obj, Substance):
            single_sub = {key: dtc.asdict(obj)[key] for key in {'CAS', 'name', 'id', 'group'}}
            single_sub["group"] = single_sub["group"].value
            sub_list += [single_sub]
    output = pd.DataFrame(sub_list)[['id', 'name', 'CAS', 'group']]
    if export_csv:
        output.to_csv("substance_list.csv", sep = ";", index = False)
        print("Saved as 'substance_list.csv' in " + str(Path.cwd()))
    else:
        return output

def list_treatments(export_csv: bool = True):
    sub_list = []
    for obj in gc.get_objects():
        if isinstance(obj, Treatment):
            single_sub = {key: dtc.asdict(obj)[key] for key in {'name', 'id', 'group'}}
            single_sub["group"] = single_sub["group"].value
            sub_list += [single_sub]
    output = pd.DataFrame(sub_list)[['id', 'name', 'group']]
    if export_csv:
        output.to_csv("treatment_list.csv", sep = ";", index = False)
        print("Saved as 'treatment_list.csv' in " + str(Path.cwd()))
    else:
        return output

def list_matrixes(export_csv: bool = True):
    mat_list = []
    for obj in gc.get_objects():
        if isinstance(obj, Matrix):
            single_mat = {key: dtc.asdict(obj)[key] for key in {'name', 'id', 'description'}}
            mat_list += [single_mat]
    output = pd.DataFrame(mat_list)[['id', 'name', 'description']]
    if export_csv:
        output.to_csv("matrix_list.csv", sep = ";", index = False)
        print("Saved as 'matrix_list.csv' in " + str(Path.cwd()))
    else:
        return output