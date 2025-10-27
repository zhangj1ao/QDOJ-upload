#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from pathlib import Path
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

UPLOAD_API = "/api/admin/import_fps"
RETRY_TOTAL = 3
BACKOFF_FACTOR = 0.5
TIMEOUT = 15     # 单文件超时（秒）


def build_session(sessionid: str) -> requests.Session:
    sess = requests.Session()
    retries = Retry(total=RETRY_TOTAL,
                    backoff_factor=BACKOFF_FACTOR,
                    status_forcelist=[500, 502, 503, 504])
    sess.mount("http://", HTTPAdapter(max_retries=retries))
    sess.headers.update({
        "User-Agent": "txt2fps-uploader/1.0",
        "Accept": "*/*",
        "Origin": f"http://{HOST}",
        "Referer": f"http://{HOST}/admin/problem/batch_ops"
    })
    sess.cookies.set("sessionid", sessionid)
    return sess


def upload_one(sess: requests.Session, host: str, xml_file: Path) -> bool:
    url = f"http://{host}{UPLOAD_API}"
    files = {"file": (xml_file.name, xml_file.read_bytes(), "text/xml")}
    try:
        r = sess.post(url, files=files, timeout=TIMEOUT)
        if r.status_code != 200:
            print(f"[FAIL] {xml_file.name}  HTTP-{r.status_code}")
            return False

        json_resp = r.json()
        # 只看有没有真正导进题
        if json_resp.get("data", {}).get("import_count", 0) > 0:
            print(f"[ OK ] {xml_file.name}")
            return True
        else:
            print(f"[FAIL] {xml_file.name}  resp={json_resp}")
            return False
    except Exception as e:
        print(f"[ERROR] {xml_file.name}  exc={e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="FPS batch uploader")
    parser.add_argument("--host", required=True, help="例如 180.76.248.166")
    parser.add_argument("--session", required=True, help="sessionid=xxx")
    parser.add_argument("--dir", default="./fps_xml", help="xml 所在目录 (default: ./fps_xml)")
    args = parser.parse_args()

    global HOST
    HOST = args.host
    xml_dir = Path(args.dir)
    if not xml_dir.is_dir():
        sys.exit(f"目录不存在: {xml_dir.resolve()}")

    xml_files = sorted(xml_dir.glob("*.xml"))
    if not xml_files:
        sys.exit("未发现 .xml 文件，请先运行 txt2fps.py 生成")

    sess = build_session(args.session)
    ok = 0
    for f in xml_files:
        if upload_one(sess, HOST, f):
            ok += 1
    print(f"\n上传完成: 成功 {ok}/{len(xml_files)}")


if __name__ == "__main__":
    main()