-----------
| License |
-----------
GPLv3 (http://www.gnu.org/licenses/gpl.html)

----------------
| Instructions |
----------------
0) Log in to lxplus:
ssh lxplus.cern.ch

1) Check out the code:
[if needed: export CVSROOT=username@cmscvs.cern.ch:/cvs_server/repositories/CMSSW;export CVS_RSH=ssh]
cvs co -d ra1stats UserCode/elaird/ra1stats
cd ra1stats

2) Set up the environment:
source env.sh

3) Run it:
./stats.py --help

--------
| Bugs |
--------
Please send bug reports to edward.laird@cern.ch.