# groupeMath

Math group repository.

## 1. How to

In a terminal:
```bash
# go to your folder
cd path/to/folder
# get the latest version of the code
git pull
```
Then you can see and eventually modify the codes.
Once you are done, if you want to push the changes you made, type:
```bash
git add .
git commit -m "Message describing the changes"
git push
```
The changes you made are now on GitHub.
Don't forget to `git pull` each time you want to work on the codes!

## 2. Structure

- `cable_robot.py`:
- `calculs.py`: discretisation and motors rotation computation, main script;
- `cli.py`:
- `command.py`:
- `decorators.py`: decorators for a cleaner code, it is ok if you don't look at it;
- `gen.py`:
- `groupeMathSquelette`: this script is outdated, was a previous version of `calculs.py`;
- `objects.py`: classes needed for the `calculs.py` script;
- `utils.py`: useful tools and functions.

### Tests

- `test/`: folder where the unittests are stored.

To run the tests, type in a terminal:
```bash
python -m unittest
```
