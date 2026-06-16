#!/bin/sh
## WW
mZp=2000
ms=200
mChi=200
fileName=DarkHiggsToWW_Zp${mZp}_s${ms}_Chi${mChi}_fragment.py
cp Template_DarkHiggs-fragment.py $fileName
sed -i "s|MASS_MZP|${mZp}|" ${fileName}
sed -i "s|MASS_MHS|${ms}|" ${fileName}
sed -i "s|MASS_MCHI|${mChi}|" ${fileName}
sed -i "s|sKid1|24|" ${fileName}
sed -i "s|sKid2|-24|" ${fileName}
##
mZp=2000
ms=300
mChi=200
fileName=DarkHiggsToWW_Zp${mZp}_s${ms}_Chi${mChi}_fragment.py
cp Template_DarkHiggs-fragment.py $fileName
sed -i "s|MASS_MZP|${mZp}|" ${fileName}
sed -i "s|MASS_MHS|${ms}|" ${fileName}
sed -i "s|MASS_MCHI|${mChi}|" ${fileName}
sed -i "s|sKid1|24|" ${fileName}
sed -i "s|sKid2|-24|" ${fileName}
##
mZp=2000
ms=300
mChi=500
fileName=DarkHiggsToWW_Zp${mZp}_s${ms}_Chi${mChi}_fragment.py
cp Template_DarkHiggs-fragment.py $fileName
sed -i "s|MASS_MZP|${mZp}|" ${fileName}
sed -i "s|MASS_MHS|${ms}|" ${fileName}
sed -i "s|MASS_MCHI|${mChi}|" ${fileName}
sed -i "s|sKid1|24|" ${fileName}
sed -i "s|sKid2|-24|" ${fileName}
#######################
## ZZ
mZp=2000
ms=200
mChi=200
fileName=DarkHiggsToZZ_Zp${mZp}_s${ms}_Chi${mChi}_fragment.py
cp Template_DarkHiggs-fragment.py $fileName
sed -i "s|MASS_MZP|${mZp}|" ${fileName}
sed -i "s|MASS_MHS|${ms}|" ${fileName}
sed -i "s|MASS_MCHI|${mChi}|" ${fileName}
sed -i "s|sKid1|23|" ${fileName}
sed -i "s|sKid2|23|" ${fileName}
##
mZp=2000
ms=300
mChi=200
fileName=DarkHiggsToZZ_Zp${mZp}_s${ms}_Chi${mChi}_fragment.py
cp Template_DarkHiggs-fragment.py $fileName
sed -i "s|MASS_MZP|${mZp}|" ${fileName}
sed -i "s|MASS_MHS|${ms}|" ${fileName}
sed -i "s|MASS_MCHI|${mChi}|" ${fileName}
sed -i "s|sKid1|23|" ${fileName}
sed -i "s|sKid2|23|" ${fileName}
##
mZp=2000
ms=300
mChi=500
fileName=DarkHiggsToZZ_Zp${mZp}_s${ms}_Chi${mChi}_fragment.py
cp Template_DarkHiggs-fragment.py $fileName
sed -i "s|MASS_MZP|${mZp}|" ${fileName}
sed -i "s|MASS_MHS|${ms}|" ${fileName}
sed -i "s|MASS_MCHI|${mChi}|" ${fileName}
sed -i "s|sKid1|23|" ${fileName}
sed -i "s|sKid2|23|" ${fileName}
#######################
## HH
mZp=2000
ms=300
mChi=200
fileName=DarkHiggsToHH_Zp${mZp}_s${ms}_Chi${mChi}_fragment.py
cp Template_DarkHiggs-fragment.py $fileName
sed -i "s|MASS_MZP|${mZp}|" ${fileName}
sed -i "s|MASS_MHS|${ms}|" ${fileName}
sed -i "s|MASS_MCHI|${mChi}|" ${fileName}
sed -i "s|sKid1|25|" ${fileName}
sed -i "s|sKid2|25|" ${fileName}
##
mZp=2000
ms=400
mChi=200
fileName=DarkHiggsToHH_Zp${mZp}_s${ms}_Chi${mChi}_fragment.py
cp Template_DarkHiggs-fragment.py $fileName
sed -i "s|MASS_MZP|${mZp}|" ${fileName}
sed -i "s|MASS_MHS|${ms}|" ${fileName}
sed -i "s|MASS_MCHI|${mChi}|" ${fileName}
sed -i "s|sKid1|25|" ${fileName}
sed -i "s|sKid2|25|" ${fileName}
##
mZp=2000
ms=300
mChi=500
fileName=DarkHiggsToHH_Zp${mZp}_s${ms}_Chi${mChi}_fragment.py
cp Template_DarkHiggs-fragment.py $fileName
sed -i "s|MASS_MZP|${mZp}|" ${fileName}
sed -i "s|MASS_MHS|${ms}|" ${fileName}
sed -i "s|MASS_MCHI|${mChi}|" ${fileName}
sed -i "s|sKid1|25|" ${fileName}
sed -i "s|sKid2|25|" ${fileName}



