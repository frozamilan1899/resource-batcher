import requests
import os
import json
import traceback
from constant import *


def get_resource_data(base_url, resource_type):
    try:
        api = resource_type + "?pageNumber=1&pageOrder=oldest&pageSize=10000"
        url = base_url + api
        print("call all " + resource_type + " resource data:", url)
        response = requests.get(url)
        data = json.loads(response.text).get('data')
        resources = data.get('resources')
        return resources
        # end for
    except Exception as e:
        print("something gets wrong:", e)
        traceback.print_exc()
    return None


def upload_preview_func(base_url, resource_type, batch_files_dir, resource_id, preview_name):
    try:
        api = resource_type + "/" + resource_id + "/preview"
        url = base_url + api
        print("check preview file")
        preview_path, fn = read_file(batch_files_dir, preview_name)
        print("preview_path:" + preview_path)
        if len(preview_path) == 0:
            print("the preview doesn't exist:", preview_name)
            return
        headers = {
            "Connection": "keep-alive"
        }
        files = {
            "preview": (fn, open(preview_path, "rb"), "application/octet-stream")
        }
        print("call preview upload url:", url)
        response = requests.put(url=url, headers=headers, files=files)
        print(response.status_code)
    except Exception as e:
        print("something gets wrong:", e)
        traceback.print_exc()


def upload_file_func(base_url, resource_type, resource_file_type, batch_files_dir, resource_id, file_name):
    try:
        api = resource_type + "/" + resource_id + "/file"
        if resource_file_type != '默认类型':
            api = api + "?fileType=" + resource_file_type
        url = base_url + api
        print("check resource file")
        if resource_file_type != res_file_types[3]:  # floor-plan不需要添加zip后缀
            file_name = file_name + ".zip"
        file_path, fn = read_file(batch_files_dir, file_name)
        print("file_path:" + file_path)
        if len(file_path) == 0:
            print("the resource file doesn't exist:", file_name)
            return
        headers = {
            "Connection": "keep-alive"
        }
        files = {
            "resource": (fn, open(file_path, "rb"), "application/octet-stream")
        }
        print("call resource file upload url:", url)
        response = requests.put(url=url, headers=headers, files=files)
        print(response.status_code)
        print('<--- uploading done')
    except Exception as e:
        print("something gets wrong:", e)
        traceback.print_exc()


def read_file(batch_files_dir, file_name):
    for fn in os.listdir(batch_files_dir):
        if fn.lower() == file_name:
            file_path = os.path.join(batch_files_dir, fn)  # 实际要上传的文件路径
            print('batch file original name:', file_path)
            return file_path, fn
    return '', ''


def upload_preview(base_url, resource_type, batch_files_dir):
    resources = get_resource_data(base_url, resource_type)
    if resources is None:
        return
    try:
        for res in resources:
            resource_id = res.get('resourceId')
            res_name = res.get('name')
            print("resource id:" + resource_id + " name:" + res_name)
            preview_path = res.get('path')
            if preview_path is None:
                print("resource " + res_name + " has no preview")
                continue
            preview_name = preview_path.split("/")[-1]
            print("preview name original:", preview_name)
            preview_name = preview_name.lower()
            print("preview name lower:", preview_name)
            upload_preview_func(base_url, resource_type, batch_files_dir, resource_id, preview_name)
        # end for
        print("<--- done")
    except Exception as e:
        print("something gets wrong:", e)
        traceback.print_exc()


def upload_bundle(base_url, resource_type, resource_file_type, batch_files_dir):
    resources = get_resource_data(base_url, resource_type)
    if resources is None:
        return
    try:
        for res in resources:
            resource_id = res.get('resourceId')
            res_name = str(res.get('name'))
            print("resource id:" + resource_id + " name:" + res_name)
            files = res.get('files')
            for file in files:
                if resource_file_type != '默认类型':
                    file_type = file.get("fileType")
                    if file_type != resource_file_type:
                        continue
                bundle_path = file.get('path')
                if bundle_path is None:
                    print("resource " + res_name + " has no bundle file")
                    break
                bundle_name = file.get('fileName')
                print("bundle name original:", bundle_name)
                bundle_name = bundle_name.lower()
                print("bundle name lower:", bundle_name)
                upload_file_func(base_url, resource_type, resource_file_type, batch_files_dir, resource_id, bundle_name)
        # end for
        print("<--- upload bundle file done")
    except Exception as e:
        print("something gets wrong:", e)
        traceback.print_exc()


def upload_art(base_url, resource_type, resource_file_type, batch_files_dir):
    resources = get_resource_data(base_url, resource_type)
    if resources is None:
        return
    try:
        for res in resources:
            resource_id = res.get('resourceId')
            res_name = str(res.get('name'))
            print("resource id:" + resource_id + " name:" + res_name)
            files = res.get('files')
            for file in files:
                file_type = file.get("fileType")
                if file_type != resource_file_type:
                    continue
                art_path = file.get('path')
                if art_path is None:
                    print("resource " + res_name + " has no art file")
                    break
                art_name = file.get('fileName')
                print("art name original:", art_name)
                art_name = art_name.lower()
                print("art name lower:", art_name)
                upload_file_func(base_url, resource_type, resource_file_type, batch_files_dir, resource_id, art_name)
        # end for
        print("<--- upload art file done")
    except Exception as e:
        print("something gets wrong:", e)
        traceback.print_exc()


def upload_scene_floor_plan(base_url, resource_type, resource_file_type, batch_files_dir):
    resources = get_resource_data(base_url, resource_type)
    if resources is None:
        return
    try:
        for res in resources:
            resource_id = res.get('resourceId')
            res_name = str(res.get('name'))
            print("resource id:" + resource_id + " name:" + res_name)
            files = res.get('files')
            for file in files:
                file_type = file.get("fileType")
                if file_type != resource_file_type:
                    continue
                floor_plan_path = file.get('path')
                if floor_plan_path is None:
                    print("resource " + res_name + " has no floor-plan file")
                    break
                floor_plan_name = file.get('fileName')
                print("floor-plan name original:", floor_plan_name)
                floor_plan_name = floor_plan_name.lower()
                print("floor-plan name lower:", floor_plan_name)
                upload_file_func(base_url, resource_type, resource_file_type, batch_files_dir, resource_id, floor_plan_name)
        # end for
        print("<--- upload scene floor-plan done")
    except Exception as e:
        print("something gets wrong:", e)
        traceback.print_exc()


def get_res_data_and_upload_file(base_url, resource_type, resource_file_type=None, batch_files_dir=None):
    if base_url is None:
        return -1
    if resource_type is None:
        return -1

    matched = False
    if resource_file_type == res_file_types[0]:
        # 上传缩略图
        matched = True
        upload_preview(base_url, resource_type, batch_files_dir)
    if resource_file_type == res_file_types[1] or resource_file_type == res_file_types[4]:
        # 上传bundle文件
        matched = True
        upload_bundle(base_url, resource_type, resource_file_type, batch_files_dir)
    if resource_file_type == res_file_types[2] and (resource_type == res_types[0] and resource_type == res_types[1] and resource_type == res_types[2] and resource_type == res_types[3]):
        # 上传美术文件，只允许scene\character\objects\cloth
        matched = True
        upload_art(base_url, resource_type, resource_file_type, batch_files_dir)
    if resource_file_type == res_file_types[3] and resource_type == res_types[0]:
        # 上传scene的floor-plan，只允许scene
        matched = True
        upload_scene_floor_plan(base_url, resource_type, resource_file_type, batch_files_dir)

    if matched is False:
        print("no cases matched, do nothing")

    print('==== 结束 =================================================================')
    return 0


if __name__ == '__main__':
    print("start --->")
    base_url = "http://3.91.94.157:8060/resource/"
    resource_type = "emotion"
    resource_file_type = "默认类型"
    batch_files_dir = "/Users/woke/Desktop/Action_Resource/Res_2022.11.03/emotion_bundle"
    get_res_data_and_upload_file(base_url, resource_type, resource_file_type, batch_files_dir)