# Script to be called as cibuildwheel before-all

set -e

CIBW_PLATFORM=$(uname)
CIBW_BUILD=$AUDITWHEEL_POLICY

echo D $CIBW_PLATFORM B $CIBW_BUILD

if [[ $CIBW_PLATFORM == "Linux" ]]; then
    echo "platform is Linux."
    if [[ $CIBW_BUILD == *"manylinux"* ]]; then
        echo "building manylinux"
        yum -q update && yum -q -y install gmp-devel
    else
        echo "building musllinux"
        apk add gmp-dev
    fi
    sh install-pari.sh
elif [[ $CIBW_PLATFORM == "Darwin" ]]; then
    echo "platform is macOS."
    sh install-pari-msys2.sh
    brew install libomp
elif [[ $CIBW_PLATFORM == *"MINGW64_NT"* ]]; then
    echo "platform is Windows."
    bash install-pari-msys2.sh pari64 gmp64
    ln -s /ucrt64/include/gmp.h /usr/include
else
    echo "unknown platform: $CIBW_PLATFORM"
fi
