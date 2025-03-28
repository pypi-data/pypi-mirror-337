# -*- coding: UTF-8 -*-
"""
@File    ：url.py
"""
import os
import re

import requests
import urllib3
from bs4 import BeautifulSoup
from logzero import logger as log_in

from kyutil.cmd import run_get_return
from kyutil.config import HTTP, HTTPS
from kyutil.http_util import send_request

urllib3.disable_warnings()


def url_reachable(url, logger=log_in):
    """判断url是否可达"""
    if url and url.startswith("http"):
        try:
            r = send_request(url, verify=False, method="HEAD", timeout=7)
            logger.info(f"URL可达性检测状态码：{r.status_code}")
            return r.status_code <= 400
        except Exception as e:
            logger.warning(f"URL {url} 不可达, {e}")


def url_filename(url_):
    if not url_:
        return ""
    return os.path.basename(url_)


def wget_remote_dirs(_logger, remote_url, local_file_path):
    """
    函数功能：03-高级wget解析下载
    函数支持：可实现httpd多层目录，且只下载指定目录
    """
    if not remote_url:
        raise RuntimeError(f"文件「{remote_url}」下载失败。")
    else:
        if not remote_url.endswith("/") and "." not in remote_url[-5:]:
            remote_url = f"{remote_url}/"
        dirs_ = len((remote_url.strip(HTTP).strip(HTTPS)).split("/")) - 1
        c = f"wget -nv --limit-rate=20m -c -r -np -nH -L --cut-dirs {dirs_} -e robots=off -R index.html* " \
            f"--restrict-file-names=nocontrol --no-check-certificate -P {local_file_path} {remote_url}"
        run_get_return(c, _logger)
        # 逐层清除index文件 TODO:优化，有可能文件就是index。
        for root, dirs, files in os.walk(local_file_path):
            for f in files:
                file_name = os.path.join(root, f)
                if 'index' in f:
                    os.remove(file_name)
        return True


def fetch_log_files(url, prefix="build", suffix='log'):
    # 发送GET请求获取页面内容
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page, status code: {response.status_code}")
        return []

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有的链接
    links = soup.find_all('a')
    # 定义正则表达式模式
    pattern = re.compile(fr'^{prefix}.*\.{suffix}$')

    # 过滤出符合模式的链接
    build_log_files = [link.get('href') for link in links if pattern.match(link.get('href', ''))]

    return build_log_files[0] if build_log_files else ''
