#http://root.cern.ch/phpBB3/viewtopic.php?f=3&t=9951&p=42716&hilit=pyroot+lxplus#p42716
#http://root.cern.ch/phpBB3/viewtopic.php?f=3&t=11374&p=49129&hilit=GLIBCXX_3.4.9#p49129

TAG=x86_64-slc5-gcc43-opt

if [[ "$HOSTNAME" == *hep.ph.ic.ac.uk ]]; then
    BASEDIR=/vols/cms02/elaird1/18_root_from_afs/lcg/
    #ROOTVER="svn"
    ROOTVER="5.30.00-patches"
else
    BASEDIR=/afs/cern.ch/sw/lcg/
    ROOTVER="5.30.00/${TAG}"
fi

source ${BASEDIR}/contrib/gcc/4.3.2/${TAG}/setup.sh ${BASEDIR}/contrib
source ${BASEDIR}/app/releases/ROOT/${ROOTVER}/root/bin/thisroot.sh

export PATH=${BASEDIR}/contrib/gcc/4.3.2/${TAG}/bin:${PATH}
export LD_LIBRARY_PATH=${BASEDIR}/contrib/gcc/4.3.2/${TAG}/lib64:${LD_LIBRARY_PATH}

export PATH=${BASEDIR}/external/Python/2.6.5/${TAG}/bin:${PATH}
export LD_LIBRARY_PATH=${BASEDIR}/external/Python/2.6.5/${TAG}/lib:${LD_LIBRARY_PATH}