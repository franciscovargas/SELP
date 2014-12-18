SELP
====
The following web application is designed 
to implement a interactive map which creates semi-random walks
within edinburgh based on users ranking o streets and paths

INSTLATION
====
From DICE:
* virtualenv --system-site-packages mapov # requires matplotlib which cannot be insalled by pip
* source mapov/bin/activate
* from project root directory: SELP $ pip install -e . 

Other than DICE:
*Requires matplotlib
*all other packages be installed within the virtual env by
*pip install -e .

USAGE
====
RANDOM WALK:  enter a start point enter a end point (within edinburgh) click
the random walk button. Example:
* start point: Boys Brigade Walk, Southside,
* end point: Teviot, Charles Street Lane, Southside,
CREATE PATH: click on two points in the map then it is intuitive

