#VoidBox: Free cloud files storage.
[VoidBox WEB](https://voidbox.alhasubji.store)
___

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) &nbsp;
___ 

## Free Cloud Storage Module:

[![PyPI version](https://badge.fury.io/py/voidbox.svg)](https://badge.fury.io/py/voidbox)

VoidBox is a free cloud storage library based on the API of `voidbox.alhasubji.store`. It operates on a box system, where each box can store up to 1.9 GB of data. The library allows you to interact with the API for creating boxes, uploading files, and more.
```bash
pip install VoidBox
```
### Try it now!
## An e.g
***You must have the `API_KEY` or `BearerTOKEN` to use:***
```python
from voidbox import VoidBoxAPI
from voidbox import Create
create = Create()
# Create Object 
api = VoidBoxAPI(token="API or Bearer Token")

# Signup
signup_response = create.signup("username", "password")
print(signup_response)

# Login 
login_response = create.login("username", "password")
print(login_response)

# Get my Info
me_response = api.get_me()
print(me_response)
# Create a box.
create_box_response = api.create_box("My New Box", "A description of my new box")
print(create_box_response)
#Upload a file to a box
upload_file_response = api.upload_file("boxid", "path/to/file.txt")
print(upload_file_response)
```
## It also has `signup` and `signin` functions only using the Create Integrated class .
______
______
______

[!!] *** Powered By `voidbox.alhasubji.store` website.
