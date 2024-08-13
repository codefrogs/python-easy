# To setup
# --------
#
# Type: 
#      source ./setup.sh
#

package_path=${PWD%/*}
PYTHONPATH=${PYTHONPATH}:${package_path}
export PYTHONPATH
