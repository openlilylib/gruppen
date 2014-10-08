# Gruppen

GUI application and set of tools to manage collaborative editions of
(orchestral) scores with LilyPond.  The plan is to create a one-stop
solution to project management centered around the basic idea of a score
that is ripped into a "segment grid".

The functionality can be accessed through a GUI application written in
PyQt or through a set of Python scripts. In addition there is a JavaScript
based solution for web management available.

The project name is a loose association to Karlheinz Stockhausen's
composition [Gruppen](http://en.wikipedia.org/wiki/Gruppen_(Stockhausen)) for
three orchstras.  Our concept of the segment grid has a (very) distant
relationship to the formal principles *Gruppen* is built upon, and "Gruppen"
(groups -> teams) is also a nice association to the way we conceive collaborative
music editing.

## Team

The project is initiated by Urs Liska and Peter Bjuhr, in the context of a
first proof-of-concept
[crowd-engraving project](http://lilypondblog.org/2014/10/crowd-engraving-picking-up-speed/).

If you're interested in this project (and particularly in contributing) don't
hesitate to contact ul at openlilylib.org.

## Features

There is already an amount of code that can be ported from that project, but
the goal is to go way beyond the existing possibilities. The intended features
include:

- **Administering project files**
    - generating files for new parts
    - generating files for printed parts
    - managing score structure
    - editing template files and project structure
- **Document project status and administer tasks**
    - analyze the repository and display the state of all segments
    - provide an interface to reserve work and review tasks
- **Editing annotations**
    - Display annotations entered in the score
    - Sort/group/analyze them
    - Edit them in a convenient interface
    - Exporting reports
