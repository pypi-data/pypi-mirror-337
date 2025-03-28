# -*- coding: UTF-8 -*-
import logging
import os
import subprocess
import time

from logzero import logger as logger_

from kyutil.base import is_url, HTTP, HTTPS, format_slashes, acquire_lock, release_lock
from kyutil.file import ensure_dir
from kyutil.http_util import send_request
from kyutil.shell import run_get_return, run_command


def download_url2local(url, local_dir, logger=logger_) -> int:
    """
    将url地址下载到本地路径, 不具备切分目录功能。会下载所有，一般用来下载单个文件
    Args:
        url:
        local_dir:
        logger:

    Returns:

    """
    if not is_url(url):
        logger.error(f"url地址无效: {url}")
        return -1
    base_path = '/'.join(format_slashes(url).split('/')[2:])
    lock_file = os.path.join(local_dir, base_path, '.download.lock')
    success_flag = os.path.join(local_dir, base_path, '.download_success.flag')
    while True:
        lock_fd = acquire_lock(lock_file=lock_file)
        if os.path.exists(success_flag):
            return 0
        if lock_fd is not None:
            try:
                logger = logger or logging.getLogger("utils.download")
                logger.info(f"开始下载：{url}")
                cmd = f"wget -nv -c --no-check-certificate --level=0 --limit-rate=10m -r -np -nH -e robots=off -R index.html* --reject-regex '/os/','/source/','/debug/' -P {local_dir} {url}"
                logger.info(f"CMD：【 {cmd} 】")
                p = subprocess.Popen(cmd, shell=True)
                p.wait()
                if p.stderr:
                    logger.error(f"下载stderr输出是 {p.stderr.read()}")
                    release_lock(lock_fd=lock_fd)
                    return -1
                with open(success_flag, 'w') as f:
                    f.write('Download successful')
                release_lock(lock_fd=lock_fd)
                return 0
            except Exception as e:
                logger.error(f"下载失败，e:{e} URL： {url} dir: {local_dir}")
                release_lock(lock_fd=lock_fd)
                return -1
        else:
            time.sleep(5)


def download_url2local_by_curl(url, local_dir, logger=logger_) -> int:
    """
    使用curl的方式将url地址下载到本地路径, 具备切分目录功能。仅下载单个文件
    @param url:
    @param local_dir:
    @param logger:
    @return:
    """
    if is_url(url):
        try:
            logger = logger or logging.getLogger("utils.download")
            logger.info(f"开始下载：{url}")
            cmd = f"curl -o  {local_dir} {url}"
            logger.info(f"CMD：【 {cmd} 】")
            # print(f"CMD：【 {cmd} 】")
            p = subprocess.Popen(cmd, shell=True)
            p.wait()
            if p.stderr:
                logger.error(f"下载stderr输出是 {p.stderr.read()}")
                return -1
            return 0
        except Exception as e:
            logger.error(f"下载 失败，e:{e} URL： {url} dir: {local_dir}")
            return -1
    else:
        logger.error(f"url地址无效: {url}")
        return -1


def wget_remote_dirs(_logger, remote_url, local_file_path, limit_rate="10m", with_top_dir=1, timeout=3600) -> bool:
    """
    函数功能：03-高级wget解析下载，一般用来下载目录（仓库）
    函数支持：可实现httpd多层目录，且只下载指定目录
    """
    if not remote_url:
        return False
    else:
        if not remote_url.endswith("/") and "." not in remote_url[-5:]:
            remote_url = f"{remote_url}/"
        dirs_ = len((remote_url.strip(HTTP).strip(HTTPS)).split("/")) - with_top_dir
        c = f"wget -nv --timeout={timeout} --limit-rate={limit_rate or '10m'} -c -r -np -nH -L --cut-dirs {dirs_} -e robots=off -R index.html* " \
            f"--restrict-file-names=nocontrol --no-check-certificate  --reject-regex '/os/','/source/','/debug/' -P {local_file_path} {remote_url}"
        ok, _ = run_get_return(c, _logger)
        # 逐层清除index文件 TODO:优化，有可能文件就是index。
        for root, dirs, files in os.walk(local_file_path):
            for f in files:
                file_name = os.path.join(root, f)
                if 'index' in f:
                    os.remove(file_name)
        return ok


def copy_by_scp(source, dest, logger=logger_) -> bool:
    """
    通过scp同步仓库，源和目的机器都得能免密登录。
    ssh user@10.44.16.185 'mkdir -p /repo_data/private_test/history/ctdy/20241014/test//adv/lic/os/base/' && scp -pr3vr root@10.44.79.81:/mnt/iso_builder/isobuild/mash/20241014/test/7732/mash_data/x86_64 user@10.44.16.185:/repo_data/private_test/history/ctdy/20241014/test//adv/lic/os/base/
    Args:
        logger:
        source: 源地址
        dest: 目的地址

    Returns:
        目录返回值
    """
    host, fp = dest.split(":")
    cmd = f"ssh {host} 'mkdir -p {fp}' && scp -pr3vr {source} {dest}"
    return run_command(cmd, logger=logger)


def download_file(url: str, local_path: str, chunk_size: int = 10240, verify=False, logger_=logger) -> bool:
    """
    下载文件到本地 , 带有 wget 的 兼容性下载
    @param url:文件的URL地址
    @param local_path: 存储到本地的文件名称
    @param chunk_size:
    @param verify:
    @param logger_:
    @return:
    """
    from .iso_utils import mkdir

    print(f'from {url} download to {local_path}')
    try:
        ensure_dir(os.path.dirname(local_path))
        r = send_request(url, verify=verify, method="HEAD")
        if r.status_code == 200:
            with send_request(url, stream=True, verify=verify) as req:
                mkdir(os.path.split(local_path)[0])
                with open(local_path, 'wb') as f:
                    for chunk in req.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                return True
        else:
            logger_.warning(f"文件下载Head Resp not 200，code:{r.status_code}")
    except Exception as e:
        logger_.warning(f"文件下载失败，Err:{e}")
    if not os.path.isfile(local_path):
        cmd = f"cd {os.path.dirname(local_path)} && wget -nv --limit-rate=20m --no-check-certificate -e robots=off {url} -O {os.path.basename(local_path)}"
        return run_command(cmd) == 0
    return False
