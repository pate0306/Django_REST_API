# Django_REST_API

# pdf-uploader


## Environment Setup
1. Clone the repository to the folder of your choice.
2. Open PyCharm.
3. File > Open - Point it to the pdf-uploader directory just cloned.
4. Once the project opens, Click File > Settings > Project Interpreter.
5. Click on the settings button on the top right and then click Add local. A pop-up will open.
6. Make sure Virtual Environment is selected. In that make sure New Environment is selected.
7. Specify the location anywhere except in the pdf-uploader project cloned.
8. Select the base interpreter and point it to the python.exe - It would be in the folder where you installed python.
9. Click OK and wait for the environment to get created.

## Basic Installations
Click terminal from pycharm and run the following commands for basic setup. Close and re-open to make sure you are in Virtual Environment.
1. Run `pip install -r requirements.txt`
2. Run `python manage.py migrate`
3. Run `python manage.py createsuperuser`


## Running the application
1. Once everything is setup. Click run in python. This should start up the application in few seconds
2. Go to `http://127.0.0.1:8000/admin` - This is the admin panel for django where you should be able to add users. One default super user(admin user) is added when we ran one of the command above. Credentaisl - `admin/admnin`. A super user is someone who will have access to all the PDFs that are stored in the database. Other user you add from django admin panel are just normal user (unless you provide them super user permisssion). These users will have access to only PDFs they uploaded. This way a user based classification is done in the application
3. Now once you have the credentials. You should be able to request a Bearer Authentication token from the application. To do that, make a POST request to `http://127.0.0.1:8000/api-token-auth` with `username` and `password` as the key and entering the correct credentials. You should be able to get the Token after that. Do that for each user you wish to have token for
4. GET request to `http://127.0.0.1:8000/pdf_list/` will get you a list of PDF for a particular user.
5. POST request to `http://127.0.0.1:8000/pdf_list/` will help you upload a PDF file to server. Takes `file` and `password` as parameter. where file is the PDF file and password is the password with which the file will be encrypted
6. GET request to `http://127.0.0.1:8000/download_pdf_file/` will return the encrypted file stored on the server which you can decrpty with password you provided when uploading it to server. Takes `pdf_name` as parameter where it is the name of the file. For example: "example.pdf"
