#### Install requirements

```shell
$ pip install -r requirements.txt
```

- Flask : A simple framework to make a Rest API.

- TinyDB : We will use this as our database, as it is a simple JSON file, will be easy to read and debug

- flask_testing : This library will be used to run our tests.


#### Run the flask server

```
export FLASK_APP=server
flask run
```

- When you run the flask server, a `db.json` file for TinyDB will be created (if it doesn't already exist), and also a `known/` directory, to store the images.

- The image recognition script can run side by side and keep verifying against this `known/` folder

- If you do change the folder name, please change it in `server.py` file as well.


#### The 2 API endpoints

`login/` - This will accept a `username` and `password` as part of it's `POST` request body. If it is valid, it will return `200`

`upload_image` - This `POST` request will accept 4 strings `name` , `age`, `guardian_name` and `guardian_phone` AND a file called `file` which has to be the image file. 


#### Running tests

Run the following command - 

```shell
$ python -m unittest test_server
```

Note - The `known` folder and a `test.db` file will be created while executing the tests. You can delete them afterwords.
