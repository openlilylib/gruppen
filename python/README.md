# /python directory

This is a directory for standalone Python scripts making Gruppen functionality
available either through the command line or as part of scripts/cronjobs.

Scripts in this directory should usually *not* define substantial functionality
on their own but rather act as an interface to modules inside `/gruppen_app`.
For this to work the `init` module will add that directory to the Python path
so any module in it can be imported directly.

The basic structure of a standalone script is:

```python
import sys

# import the initialisation module for the standalone scripts
import init

# import interface to parse the command line
# this will create a "parser" object with generic arguments
import commandline

# optionally add specific arguments with parser.add_argument()

# import project management infrastructure
import project


def main():
    global project
    # parse commandline
    args = commandline.parse()
    # try to open a project
    try:
        project = project.Project(args)
    except AssertionError, e:
        print '\n', e, '\n'
        sys.exit(1)

    # interpret more arguments, import modules and do what is necessary
    # but don't implement it and call modules from `/gruppen_app` instead.
    

# ####################################
# Finally launch the program
if __name__ == "__main__":
    main()



```