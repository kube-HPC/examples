rm -f alg.tar.gz
tar --exclude="$(basename "$0")" -zcvf alg.tar.gz *

