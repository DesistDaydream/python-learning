#!/usr/bin/python3
import argparse
import requests
import hashlib
import re

# 参数定义部分
parser = argparse.ArgumentParser(description='CDN curl tools')
parser.add_argument('URL', help='请求URL，必填;如含有特殊参数字符，URL使用双引号括起来', type=str)
parser.add_argument('-M', '-m', '--method',
                    help='请求方法，默认是GET，支持HEAD', default='GET')
parser.add_argument('-R', '-r', '--range', help='发送range头 格式 startbyte-endbyte，默认0-10000000', type=str,
                    default='0-10000000')
parser.add_argument('-H', '--headers', help='发送自定义请求header头，key:value格式，支持多个以逗号分隔，'
                                            '如"Accept-Encoding:gzip,key:value"', type=str)
parser.add_argument('-J', '-j', '--json', action='store_true',
                    default=False, help='结果以json形式展示')
parser.add_argument('-v', '-V', '--version',
                    action='version', version='%(prog)s 1.0')
parser.add_argument(
    '-x', '--proxy', help='代理IP地址，IP:PORT，eg : 1.1.1.1:80', type=str, default='')

User_Agent = 'HWCDN CurlTool'


def curl(url, method, range, proxy, **headers_dic):
    Range = 'bytes=%s' % range
    url_schemmatch = re.match(r'(https*://).*', url)
    if not url_schemmatch:
        url = 'http://' + url  # 如果没有输入http://则补齐
    # 格式化URL  schem domain uri
    url_re = re.match(r'(https*://)(.*?)(/.*)', url)
    url_re_1 = re.match(r'(https*://)(.*?)$', url)
    if url_re:
        schem = url_re.group(1)
        domainname = url_re.group(2)
        uri = url_re.group(3)
    elif url_re_1:
        schem = url_re_1.group(1)
        domainname = url_re_1.group(2)
        uri = ''
    if proxy != '':  # 如果有代理，则重构URL
        url = schem + proxy + uri
    headers = {'User-Agent': User_Agent, 'Range': Range, 'Host': domainname}
    headers.update(headers_dic)
    try:
        if method == 'GET':
            r = requests.get(url, timeout=3, headers=headers, verify=False)
        elif method == 'HEAD':
            r = requests.head(url, timeout=3, headers=headers, verify=False)
        else:
            print('不支持除GET/HEAD以外其他方法,转为GET方法')
            r = requests.get(url, timeout=3, headers=headers, verify=False)
        response_status_code = r.status_code
        request_headers = r.request.headers
        response_headers = r.headers
        response_content = r.content
        response_bodyLength = len(response_content)
        md = hashlib.md5()
        md.update(response_content)
        response_md5 = md.hexdigest()  # 响应md5
        # 计算下载速度
        response_time = r.elapsed.total_seconds()
        download_speed = len(response_content) / response_time
        curl_result = {'request_headers': request_headers, 'response_headers': response_headers,
                       'response_status_code': response_status_code,
                       'response_md5': response_md5, 'status': 'OK', 'request_method': method,
                       'response_time': response_time,
                       'download_speed': download_speed, 'url': schem + domainname + uri, 'method': method,
                       'proxy': proxy, 'response_bodyLength': response_bodyLength}
    except Exception as e:
        curl_result = {'error_info': e, 'status': 'error'}
        print('目标IP可能不支持https代理方式，请用其他方式重试')
    return curl_result


if __name__ == '__main__':
    args_dic = parser.parse_args().__dict__  # 将参数列转为字典
    # 转换Headers的处理，转化字符串为字典
    headers_str = args_dic['headers']  # HEADERS字符串
    url = args_dic['URL']
    headers_dict = {}
    if headers_str:
        list_a = headers_str.split(',')
        for i in list_a:
            list_b = i.split(':')
            headers_dict.update({list_b[0]: list_b[1]})
    curl_result = curl(url, args_dic['method'], args_dic['range'], args_dic['proxy'],
                       **headers_dict)
    # 响应输出
    if args_dic['json']:
        print(curl_result)
    else:
        print('请求部分:')  # 格式化输出
        print(' 请求URL:', curl_result['url'])
        print(' 请求方法:', curl_result['method'])
        print(' 代理:', curl_result['proxy'])
        print(' 请求头')
        for key in curl_result['request_headers']:
            print(" ", key, ":", curl_result['request_headers'][key])
        print('响应部分:')
        print(' 响应码:', curl_result['response_status_code'])
        print(' 内容MD5:', curl_result['response_md5'])
        print(' 响应时间:%.2f s' % (curl_result['response_time']))
        print(' 文件body大小:', curl_result['response_bodyLength'])
        print(' 下载速度:%.2f KB/s' % (curl_result['download_speed'] / 1000))
        print(' 响应头')
        for key in curl_result['response_headers']:
            print(" ", key, ":", curl_result['response_headers'][key])
