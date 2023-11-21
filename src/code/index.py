# -*- coding: utf-8 -*-

import logging
import os
import re
import time
import urllib.parse
import urllib.request
import oss2
import hashlib
import shutil
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential

LOGGER = logging.getLogger()
REG_URL = r'^(https?://|//)?((?:[a-zA-Z0-9-_]+\.)+(?:[a-zA-Z0-9-_:]+))((?:/[-.a-zA-Z0-9_]*?)*)((?<=/)[-_a-zA-Z0-9]+(?:\.([a-zA-Z0-9]+))+)?((?:\?[a-zA-Z0-9%&=]*)*)$'
reg_url = re.compile(REG_URL)


def parse_url(url):
    if not url:
        return
    res = reg_url.search(url)
    if res is not None:
        path = res.group(3)
        protocol = res.group(1) if res.group(1) is not None else 'http://'
        full_path = protocol + res.group(2) + res.group(3)

        if not path.endswith('/'):
            path = path + '/'
            full_path = full_path + '/'
        return dict(
            base_url=protocol + res.group(2),
            full_path=full_path,
            protocol=protocol,
            domain=res.group(2),
            path=path,
            file_name=res.group(4),
            ext=res.group(5),
            params=res.group(6)
        )


def download_file(src_url, dist_path):
    try:
        response = urllib.request.urlopen(src_url)
        if response is None or response.status != 200:
            return LOGGER.info('> download failed: %s' % src_url)
        data = response.read()

        f = open(dist_path, 'wb')
        f.write(data)
        f.close()

        LOGGER.info('>>>: %s download success' % src_url)

    except Exception as e:
        LOGGER.info('download failed: %s, %s' % (src_url, e))
        return False

    return True


def handler(event, context):
    global downloaded_list
    downloaded_list = []

    source_urls = os.environ['SOURCE_URLS']
    for source_url in source_urls.split(','):
        url = source_url.strip()
        url_dict = parse_url(url)
        domain = url_dict['domain']
        object_name = ''
        if url_dict['file_name'] is None:
            object_name = 'index.html'
            url = url_dict['full_path'] + object_name
        else:
            object_name = url_dict['file_name']
        domain_dir = '/tmp/source/' + re.sub(r':', '-', domain)
        object_dir = domain_dir + url_dict['path']
        if not os.path.exists(object_dir):
            os.makedirs(object_dir)
        object_path = object_dir + object_name
        if object_path not in downloaded_list and download_file(url, object_path):
            downloaded_list.append(object_path)
        else:
            return

    if (len(downloaded_list) > 0):
        creds = context.credentials
        oss_auth = oss2.StsAuth(
            creds.access_key_id,
            creds.access_key_secret,
            creds.security_token)
        target_domain = os.environ['TARGET_DOMAIN']
        m = re.search(r'(.*).oss-(.*).aliyuncs.com', target_domain)
        if m is None:
            LOGGER.error(
                "Target domain {} is not a valid oss domain".format(target_domain))
            raise ValueError(
                "Target domain {} is not a valid oss domain".format(target_domain))

        bucket_name = m.group(1)
        region = m.group(2)
        endpoint = 'oss-' + region + '.aliyuncs.com:'
        bucket = oss2.Bucket(oss_auth, endpoint, bucket_name)
        current_oss_dir = '/tmp/current/'
        for tmp_file in downloaded_list:
            if bucket is not None:
                object_name = "/".join(tmp_file.split("/")[4:])
                current_tmp_file = current_oss_dir + object_name
                tmp_object_dir = "/".join(current_tmp_file.split("/")[:-1])
                if not os.path.exists(tmp_object_dir):
                    os.makedirs(tmp_object_dir)
                try:
                    bucket.get_object_to_file(object_name, current_tmp_file)
                except oss2.exceptions.NoSuchKey as e:
                    LOGGER.info(
                        "no such key in the bucket = {}".format(object_name))
                if os.path.exists(current_tmp_file):
                    with open(current_tmp_file, 'rb') as current_file:
                        current_oss_file_md5 = hashlib.md5(
                            current_file.read()).hexdigest()
                    with open(tmp_file, 'rb') as file:
                        source_file_md5 = hashlib.md5(
                            file.read()).hexdigest()
                    if current_oss_file_md5 == source_file_md5:
                        LOGGER.info(
                            "skip as file not changed = {}".format(object_name))
                        continue

                LOGGER.info(
                    "start to upload file = {}".format(object_name))
                bucket.put_object_from_file(object_name, tmp_file)

                if 'CDN_DOMAIN' in os.environ and os.environ['CDN_DOMAIN'] != 'unknown':
                    cdn_domain = os.environ['CDN_DOMAIN']
                    cdn_auth = StsTokenCredential(
                        creds.access_key_id,
                        creds.access_key_secret,
                        creds.security_token)
                    client = AcsClient(region_id=context.region,
                                       credential=cdn_auth)

                    request = CommonRequest()
                    request.set_accept_format('json')
                    request.set_domain('cdn.aliyuncs.com')
                    request.set_method('POST')
                    request.set_protocol_type('https')
                    request.set_version('2018-05-10')
                    cdn_url = cdn_domain + "/" + object_name
                    request.add_query_param('ObjectPath', cdn_url)

                    request.set_action_name('RefreshObjectCaches')
                    response = client.do_action(request)
                    LOGGER.info('RefreshObjectCaches: ' + cdn_url +
                                ', and returned: ' + str(response, encoding='utf-8'))

                    request.set_action_name('PushObjectCache')
                    response = client.do_action(request)

                    LOGGER.info('PushObjectCache: ' + cdn_url +
                                ', and returned: ' + str(response, encoding='utf-8'))
    shutil.rmtree('/tmp')
    return dict(success=True)