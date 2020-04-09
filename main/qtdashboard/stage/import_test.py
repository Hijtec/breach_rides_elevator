import coms

bundle = {
        "name"     :    "first",
        "def_value":    0,
        "direction":    "send",
        "port"     :    5565,
        "mode"     :    "REQ_REP"
        }
bundle2 = {
        "name"     :    "second",
        "def_value":    1,
        "direction":    "recv",
        "port"     :    5566,
        "mode"     :    "PUB_SUB"
        }
bundle3 = {"name":"third", "def_value":0, "direction":"recv", "port":5566, "mode":"PUB_SUB"}

par_dict = {}
com_dict = {}

coms.create_parameter(bundle, par_dict, com_dict)
coms.create_parameter(bundle2, par_dict, com_dict)
coms.create_parameter(bundle3, par_dict, com_dict)
print(par_dict, com_dict)

params = coms.Parameters(par_dict, com_dict)
print(params)