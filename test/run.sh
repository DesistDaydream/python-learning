#! /bin/bash
set -ue
set -o pipefail
#
function help(){
    echo -e "
Usage: bash curl.sh OPTIONS

OPTIONS:
    -c, --count INT         要执行的次数
    -u, --url URL           要测试的地址
"
}

opts=`getopt -o c:f:ht:u: -l count:,file:,help,time:,url: -- "$@"`
if [ $? != 0 ] ; then echo "terminating..." >&2 ; exit 1 ; fi
eval set -- "$opts"

while true; do
    case "$1" in
    -c|--count)
        COUNT=$2; shift 2;;
    -u|--url)
        URL=$2; shift 2;;
    -h|--help)
        help; exit 0;;
    --)
        shift
        break
        ;;
    *)
        echo "internal error!"
        exit 1
        ;;
    esac
    # shift
done

function main(){
    python3 pingtool.py -c ${COUNT} -d ${URL} -f '解析后IP:%h \
发送数:%s \
接受数:%r \
丢失数:%p \
最小延迟:%m \
最大延迟:%M \
抖动:%a'
}

main