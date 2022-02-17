# AutoPylot
AutoPylot project by Autonomobile !

## How to acces our presentation website

follow this link :
https://autonomobile.github.io/

## Why this project 

Autopylot was born as an end of the school year project. Our school asks from it's student to take part in an project with a group of 4 students. We are free to create our own project, but it has to be accepted by the school's board, Autopylot was !!!
Being able to work on this project means we will be able to understand how tomorrow's car will work. Moreover, we will learn valuable skills in Python and in neural networks.

Our main objective is to make our car race against other cars and win the race !
This will require multiple intermediate milestones:

 - [x] Being able to send scripted controls to the motor and servo.
 - [x] Being able to drive the car manually using a controller.
 - [x] Develop a way to gather images and annotations and store them in a stuctured way, for example sorted by date.
 - [ ] Process those data before feeding them to the neural network.
 - [ ] Being able to train a convolutional neural network using those data.
 - [ ] Build a telemetry web application.
 - [ ] Tweak the architecture and the parameters of the chosen model to acheive the best results.
 - [ ] Test in real life the model.
 - [ ] Race against others !
 - [ ] WIN !

For more detailed infomation please read the [project specifications](https://github.com/Autonomobile/AutoPylot/blob/main/project-specifications/project-specifications.pdf) 

Enjoy,

The Autonomobile Team.


## (for the devs) How to setup the software

It is recommended to have python 3.6.X installed, as this is the python version installed on the car.

To avoid any packages conflicts with your existing python installation, we will use virtualenv
install virtualenv using:
```bash
pip install virtualenv
```

Clone the repo, and install the package and it's dependencies:
```bash
git clone https://github.com/Autonomobile/AutoPylot.git
cd AutoPylot
```
Then, create a virtual env (you need to specify the path to your python3.6:
```bash
virtualenv --python C:\Path\To\Python\python.exe venv
```
Then, every time you will be working on the project, you will need to activate this environnement,
to do so:
```bash
.\venv\Scripts\activate
```

Now, to install autopylot and its requirements (including dev requirements):
```bash
pip install -e .[dev]
```

For the code formatting, we will use something called "pre-commit", that enables us to automate stuff as linting before commiting. If the code is not well linted, it will throw an error before commiting and will lint it, you will only have to commit again to apply the changes the linter did !
Here is how to setup pre-commit:
```bash
pre-commit install
```
You are now all setup to work on the project ! Don't forget to keep the setup.py and requirements.txt up to date.

To exit the virtualenv:
```bash
deactivate
```

usefull tools:
- setup a python linter (we use flake8) : https://code.visualstudio.com/docs/python/linting
- setup the test extension of vscode : https://code.visualstudio.com/docs/python/testing
- use a docstring generator for example the vscode extension "Python Docstring Generator"
