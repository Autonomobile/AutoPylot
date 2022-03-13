# AutoPylot
AutoPylot project by Autonomobile !

## How to acces our presentation website

follow this link :
https://autonomobile.github.io/

## Why this project 

AutoPylot was born as an end of the school year project. Our school asks from its student to take part in a project with a group of 4 students. We are free to create our own project, but it has to be accepted by the school's board, AutoPylot was !!!
Being able to work on this project means we will be able to understand how tomorrow's car will work. Moreover, we will learn valuable skills in Python and in neural networks.

Our main objective is to make our car race against other cars and win the race !
This will require multiple intermediate milestones:

 - [x] Being able to send scripted controls to the motor and servo.
 - [x] Being able to drive the car manually using a controller.
 - [x] Develop a way to gather images and annotations and store them in a structured way, for example sorted by date.
 - [ ] Process those data before feeding them to the neural network.
 - [ ] Being able to train a convolutional neural network using those data.
 - [ ] Build a telemetry web application.
 - [ ] Tweak the architecture and the parameters of the chosen model to achieve the best results.
 - [ ] Test in real life the model.
 - [ ] Race against others !
 - [ ] WIN !

For more detailed information please read the [project specifications](https://github.com/Autonomobile/AutoPylot/blob/main/project-specifications/project-specifications.pdf) 

Enjoy,

The Autonomobile Team.


## How to setup the software

### Python
It is recommended to have python 3.6.X installed, as this is the python version installed on the car.

To avoid any packages conflicts with your existing python installation, we will use virtualenv
install virtualenv using:
```shell
pip install virtualenv
```

Clone the repo, and install the package and it's dependencies:
```shell
git clone https://github.com/Autonomobile/AutoPylot.git
cd AutoPylot
```
Then, create a virtual env (you need to specify the path to your python3.6:
```shell
virtualenv --python C:\Path\To\Python\python.exe venv
```
Then, every time you will be working on the project, you will need to activate this environment,
to do so:
```shell
.\venv\Scripts\activate
```

Now, to install autopylot and its requirements (including dev requirements):
```shell
pip install -e .[dev]
```

For the code formatting, we will use something called "pre-commit", that enables us to automate stuff as linting before committing. If the code is not well linted, it will throw an error before committing and will lint it, you will only have to commit again to apply the changes the linter did !
Here is how to setup pre-commit:
```shell
pre-commit install
```
You are now all setup to work on the project ! Don't forget to keep the setup.py and requirements.txt up to date.

To exit the virtualenv:
```shell
deactivate
```

useful tools:
- setup a python linter (we use flake8) : https://code.visualstudio.com/docs/python/linting
- setup the test extension of VS-Code : https://code.visualstudio.com/docs/python/testing
- use a docstring generator for example the VS-Code extension "Python Docstring Generator"

### Telemetry Server

- make sure to have NodeJS and NPM installed
- Open the telemetry/ folder in another VS-Code window

#### Installation
```shell
npm i
```

#### Start dev build
```shell
npm run dev
```
#### Start Production build
```shell
npm run build
npm run start
```
