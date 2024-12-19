# Educational-Platform
A Python-Based Educational Platform, a comprehensive and interactive learning system designed to enhance knowledge acquisition and skill development. This platform serves as an intuitive and structured space for learners, offering a seamless blend of courses, chapters, and quizzes to foster effective learning and knowledge retention.
## Features

- Can add Courses and corresponding Chapters and Videos of it.
- Can add Quizzes and corresponding Questions of current module.
- Can test their knowledge of the Course through Quizzes by getting immediate results.

## Requirements

- Python 3 or higher

## Installation

### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/pulkitsh1/Educational-Platform.git
cd Educational-Platform
```

### Installing required Libraries
Use pip to install the package globally or locally. Run the following command for installing all the dependencies of the project:<br>
Use Virtual Enviroment(Preffered).

```bash
pip install -r requirements.txt
```

### .env
Create your own .env file define the given variable given below. 

```txt
DB_USER = 'your_db_user'
DB_PASSWORD = 'your_db_password'
DB_HOST = 'your_db_host'
DB_NAME = 'name_of_your_db'

DB_PORT=3306 // use 3307 for docker 
```

### Usage
Once all dependencies are installed run the following Command for running the application:

```bash
python app.py
```
After running the application server, all table will be made automatically in your connected Database.

### API Documentation
For getting to know about the API's, what their Request and Response body contains, run the following url in browser after running the application server:

```url
http://127.0.0.1:5000/swagger
```
