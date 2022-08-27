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
 - [x] Process those data before feeding them to the neural network.
 - [x] Being able to train a convolutional neural network using those data.
 - [x] Build a telemetry web application.
 - [x] Tweak the architecture and the parameters of the chosen model to achieve the best results.
 - [x] Test in real life the model.
 - [x] Race against others !
 - [x] WIN !

For more detailed information please read the [project report](ressources/final-presentation/project-report/project-report.pdf) 

Enjoy,

The Autonomobile Team.


## How to setup the software

It is recommended to have python 3.7.X installed, as this is the python version installed on the car. But you can use any python version >= 3.7.

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
Then, every time you will be working on the project, you will need to activate this environment,
to do so:
```bash
.\venv\Scripts\activate
```

Now, to install autopylot and its requirements (including dev requirements):
```bash
pip install -e .[dev]
```

For the code formatting, we will use something called "pre-commit", that enables us to automate stuff as linting before committing. If the code is not well linted, it will throw an error before committing and will lint it, you will only have to commit again to apply the changes the linter did !
Here is how to setup pre-commit:
```bash
pre-commit install
```
You are now all setup to work on the project ! Don't forget to keep the setup.py and requirements.txt up to date.

To exit the virtualenv:
```bash
deactivate
```

useful tools:
- setup a python linter (we use flake8) : https://code.visualstudio.com/docs/python/linting
- setup the test extension of VS-Code : https://code.visualstudio.com/docs/python/testing
- use a docstring generator for example the VS-Code extension "Python Docstring Generator"

## Collect, Train and Deploy your model
Here is the three main steps in the making of a model

### Joystick config
if you want to config your joystick mapping, run:
```
python -m "autopylot.controllers.joy_config"
```
it will run you through the mapping config of your controller,
when finish, you will find your mapping file in the root of your project.

### Collect
First you need to collect some data.

You will need to select in the "settings.json" the "CAMERA_TYPE", "ACTUATOR_TYPE" and "CONTROLLER_TYPE". By default they are set for the car configuration eg "webcam", "serial" and "xbox" respectively, if you are collecting data on a PC, I suggest you using "sim", "sim" and "keyboard". This will use data coming from the simulator, inputs from the keyboard and output them (actuate) in the simulator.

Start the script with the following command (don't need to cd if you are in the right directory):
```bash
cd main_programs/examples
python3 drive_with_controller.py
```
To drive depending on the controller type you use:
- "xbox": steering: left joystick, throttle: left and right triggers
- "keyboard": steering: "q" and "d" keys, throttle: "z" and "s" keys.

To record data depending on the controller type you use:
- "xbox": hold button "a"
- "keyboard": hold key "r"

You should see the collected data your "~/collect" folder. If unsure about the location of the folder, check the "COLLECT_PATH" settings in the settings.json

Note: by default a model will be loaded, if you don't touch anything, you will enter "autonomous" mode using the predictions from this default model.

### Training
Then training !

there are plenty settings for the training script:
- "MODEL_TYPE": you need to set the type of the model you want to build. For example, if you made a new method to create a model in architectures.py in the Models class called "steering_model". You can set the "model_type" field to `steering_model` and when training your model, it will be created using this function.
- "MODEL_NAME": the name of the model you want to train, the model will be saved under this name. If you wish to retrain it later, make sure to use the same name (if you wish you can copy a model, change its name and then train it again to avoid loosing the previously trained one).
- "TRAIN_LOAD_MODEL": whether you want to load the model or create one from scratch.
- "TRAIN_BATCH_SIZE": How much data you want in one batch.
- "TRAIN_EPOCHS": How many times you want to train the model on the dataset before saving it.
- "TRAIN_SPLITS": Proportion of data in the training set and testing set. If set to 0.9, this will result in having 90% of the data going to the training set and 10% going to the testing set. 
- "TRAIN_AUGM_FREQ": How frequent we want data to be augmented using data augmentation functions.


you can now start this training script with:
```bash
cd main_programs/
python3 train.py
```
Once finished, your new model should be saved in the "models" folder at the root of your project.

### Deploy
You will need to change in the settings.json the "MODEL_NAME" field to the name of the model you just trained.
then same as for the "collect" part, start the drive_with_controller.py script and enjoy !
```bash
cd main_programs/examples
python3 drive_with_controller.py
```
