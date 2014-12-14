SELP
====
The following web application is designed 
to implement a interactive map which creates semi-random walks
within edinburgh based on users ranking o streets and paths

INSTLATION
====
From DICE:
	1. virtualenv --system-site-packages mapov # requires matplotlib which cannot be insalled by pip
	2. . mapov/bin/activate
	3. from project base directory:
				SELP $ pip install -e . 

Other than DICE:
	Requires matplotlib
	all other packages be installed within the virtual env by
	pip install -e .
