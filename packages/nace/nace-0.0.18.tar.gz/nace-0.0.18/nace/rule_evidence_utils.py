"""
utilities for rule evidence

"""
import copy
import json
import os.path
import tempfile

import numpy as np

def _convert_tuples_to_lists(obj, index=0, collection_length=1):
    if hasattr(obj, '__iter__') and not isinstance(obj, str):
        result = []
        for i, item in enumerate(obj):
            result.append(_convert_tuples_to_lists(item, i, len(obj)))
        return result
    if index == 2 and collection_length in [3,4] and isinstance(obj, np.int64):
        obj = int(obj)
    return obj

def _convert_lists_to_tuples(obj):
    if hasattr(obj, '__iter__') and isinstance(obj, list):
        result = copy.deepcopy((obj))
        for i, item in enumerate(result):
            result[i] = _convert_lists_to_tuples(item)
        return tuple(result)
    return obj

def _convert_evidence_to_json_serialisable(rule_evidence :dict):
    # strip types, tuple -> list, dict -> list etc
    result = []
    for k ,v in rule_evidence.items():
        converted_k = _convert_tuples_to_lists(k)
        converted_v = _convert_tuples_to_lists(v)
        result.append( [converted_k ,converted_v ])
    return result


def _convert_from_json_to_dict(list_of_list_evidence):
    # add the types back in.
    result = {}
    for l in list_of_list_evidence:
        rule = _convert_lists_to_tuples(l[0])
        evidence = _convert_lists_to_tuples(l[1])

        result[rule] = evidence

    return result


def save_rule_evidence_to_disk(rule_evidence, filename= "rule_evidence.npy"):
    untyped_rule_evidence = _convert_evidence_to_json_serialisable(rule_evidence)
    with open(filename, "w") as f:
        json.dump(untyped_rule_evidence, f, indent=2)

def load_rule_evidence_from_disk(filename= "rule_evidence.npy"):
    rule_evidence = {}
    if os.path.exists(filename):
        with open(filename, "r") as f:
            untyped_rule_evidence = json.load(f)
        rule_evidence = _convert_from_json_to_dict(untyped_rule_evidence)
    return rule_evidence


def t1():
    data = {(('forward', (0, 0, 0, 0, 0, 0, 0), (0, 0, np.int64(2407174942)), (1, -1, np.int64(2407174942)), (2, 0, np.int64(2204181460))), (0, 0, np.int64(1152208772), (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (('forward', (0, 0, 0, 0, 0, 0, 0), (-1, 1, np.int64(2407174942)), (0, 0, np.int64(2407174942)), (1, 1, np.int64(2204181460))), (0, 0, np.int64(2829951097), (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (('forward', (0, 0, 0, 0, 0, 0, 0), (-2, 0, np.int64(2407174942)), (-1, -1, np.int64(2407174942)), (0, 0, np.int64(2204181460))), (0, 0, np.int64(1484579719), (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (('forward', (0, 0, 0, 0, 0, 0, 0), (0, 0, np.int64(2407174942)), (1, -1, np.int64(2407174942)), (2, 0, np.int64(2204181460))), (0, 0, 2407174942, (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (('forward', (0, 0, 0, 0, 0, 0, 0), (-1, 1, np.int64(2407174942)), (0, 0, np.int64(2407174942)), (1, 1, np.int64(2204181460))), (0, 0, 2407174942, (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (('forward', (0, 0, 0, 0, 0, 0, 0), (-2, 0, np.int64(2407174942)), (-1, -1, np.int64(2407174942)), (0, 0, np.int64(2204181460))), (0, 0, 2204181460, (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1)}
    # check it encodes and decodes correctly
    encoded = _convert_evidence_to_json_serialisable(data)
    unencoded = _convert_from_json_to_dict(encoded)
    assert unencoded == data
    # check it can serialize OK
    t = json.dumps(encoded)
    print(t)


if __name__ == "__main__":
    t1()