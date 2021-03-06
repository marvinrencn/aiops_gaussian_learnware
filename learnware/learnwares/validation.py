

def validate_json_parameters(json_obj, parameter_list):
    for p in parameter_list:
        assert p in json_obj