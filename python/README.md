# groupeMath
Math group repository.

## Table of contents

1. [ How to ](#1-how-to)  
    1.1. [ Get the latest codes ](#11-get-the-latest-codes)  
    1.2. [ Modify the code ](#12-modify-the-code)  
    1.3. [ Push the codes ](#13-push-the-codes)
2. [ Structure ](#2-structure)
3. [ Coding conventions ](#3-coding-conventions)  
4. [ Pics ](#5-pics)

## 1. How to

### 1.1. Get the latest codes

In a terminal, eventually the `git terminal`:
```bash
# go to your folder
cd path/to/folder
# get the latest version of the code
git pull
```

### 1.2. Modify the code

Then, in order to modify your codes, you are going to create a branch for you. It means that you are going to work on a version of the code without impacting the other branches.
In order to do so:
```bash
git branch
>> master
>> classes
# create the branch <student_name>
git branch <student_name>
# go on the branch <student_name>
git checkout <student_name>
```
Then you can modify the codes.
You only need to do this once. Then, you'll automatically be on the `<student_name>` branch (you can see it in the terminal between brackets), so no need to type this.

### 1.3. Push the codes

Once you are done, if you want to push the changes you made, type (still on your branch):
```bash
git add .
git commit -m "Message describing the changes"
git push
```
The changes you made are now on GitHub, on the branch that you previously created.
Don't forget to `git pull` each time you want to work on the codes!

## 2. Structure

- `gen.py`: trajectory generation
- `cli.py`: command line interface for the user. Comes with a `help` functionality and the possibility to choose the trajectory.
- `cable_robot.py`: test script so that the cli.py does not raise an error.
- `command.py`: discretization and motors rotation computation, main script, called by `cli.py`;
- `modules`:
    - `objects.py`: classes needed for the `command.py` script;
    - `utils.py`: tools and mathematical functions used by `command.py`.


## 3. Coding conventions

When a function is defined, we document it as follows:
```py
def fun(arg):
    """
    Blabla

    :param dimensions: blabla

    :type dimensions: np.array

    :return: blabla
    :rtype: np.array
    """
    pass
```


## 4. Pics

- motor numbering:

![Motor Numbering](./pics/motor-numbering.png)
