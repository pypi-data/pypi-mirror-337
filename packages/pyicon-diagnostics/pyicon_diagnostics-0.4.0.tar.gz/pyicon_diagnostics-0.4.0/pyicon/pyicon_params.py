import json
import os

fname = os.path.join(os.path.dirname(__file__), 'params_default.json')
#if os.path.isfile(fname):
#  with open(fname, 'r') as f:
#      params_default = json.load(f)
#else:
#  print(f'File {fname} does not exist.')
try:
  print(f"Loading default parameters from {fname}.")
  with open(fname, 'r') as f:
      params_default = json.load(f)
except:
  #print(f'Could not find {fname}. Continuingwith backup solution.')
  HOME = os.path.expanduser('~')
  params_default = {
    "path_grid": f"{HOME}/pyicon_data/grids/",
    "path_example_data": f"{HOME}/pyicon_data/icon_example_data_download/"
  }

fname = os.path.join(os.path.dirname(__file__), 'params_user.json')
if os.path.isfile(fname):
  print(f"Loading user parameters from {fname}.")
  with open(fname, 'r') as f:
      params_user = json.load(f)
else:
  #print(f'File {fname} does not exist.')
  pass

try:
  params = params_default | params_user
except:
  params = params_default

for key in ['path_grid', 'path_example_data']:
   params[key] = os.path.expanduser(params[key]) 