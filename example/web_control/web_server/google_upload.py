from __future__ import print_function
import os
import io
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools
import signal
import time

# 权限必需
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']




def delete_drive_service_file(service, file_id):
    service.files().delete(fileId=file_id).execute()


def update_file(service, update_drive_service_name, local_file_path, update_drive_service_folder_id):
    """
    将本地端的文件上传到云端
    :param service: 认证用
    :param update_drive_service_name: 存到云端的文件名
    :param local_file_path: 本地文件位置加文件名
    """

    print("Uploading file...")
    # file_metadata = {'name': update_drive_service_name}
    if update_drive_service_folder_id is None:
        file_metadata = {'name': update_drive_service_name}
    else:
        # print(update_drive_service_folder_id)
        file_metadata = {'name': update_drive_service_name,
                         'parents': update_drive_service_folder_id}
    media = MediaFileUpload(local_file_path, )
    file_metadata_size = media.size()
    start = time.time()
    file_id = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    end = time.time()
    print('File name: ' + str(file_metadata['name']))
    print('Could file ID: ' + str(file_id['id']))
    print('File size: ' + str(file_metadata_size) + ' byte')
    print("Upload time: " + str(end-start))

    return file_metadata['name'], file_id['id']



def search_file(service, update_drive_service_name, is_delete_search_file=False):
    """
    寻找云端相同文件名称，取得file id，可进行删除
    :param service: 认证用
    :param update_drive_service_name: 存到云端的文件名
    :param is_delete_search_file: 判断是否删除找到的文件
    :return:
    """
    # Call the Drive v3 API
    results = service.files().list(fields="nextPageToken, files(id, name)", spaces='drive',
                                   q="name = '" + update_drive_service_name + "' and trashed = false",
                                   ).execute()
    items = results.get('files', [])
    if not items:
        print('There is no duplicate ' + update_drive_service_name + ' file in the cloud')
    else:
        print('Duplicate files found in the cloud: ')
        for item in items:
            times = 1
            print(u'{0} ({1})'.format(item['name'], item['id']))
            if is_delete_search_file is True:
                print("Delete the file with the same name as:" + u'{0} ({1})'.format(item['name'], item['id']))
                delete_drive_service_file(service, file_id=item['id'])

            if times == len(items):
                return item['id']
            else:
                times += 1

def search_folder(service, update_drive_folder_name=None):
    """
    如果云端文件夹名称相同，则只会选择一个文件夹上传，请勿取名相同
    :param service: 认证用
    :param update_drive_folder_name: 取得指定文件夹的id，沒有的话回传None，给错也会回传None
    :return:
    """
    get_folder_id_list = []
    # print(len(get_folder_id_list))
    if update_drive_folder_name is not None:
        response = service.files().list(fields="nextPageToken, files(id, name)", spaces='drive',
                                       q = "name = '" + update_drive_folder_name + "' and mimeType = 'application/vnd.google-apps.folder' and trashed = false").execute()
        for file in response.get('files', []):
            # Process change
            print('Found folder: %s (%s)' % (file.get('name'), file.get('id')))
            get_folder_id_list.append(file.get('id'))
        if len(get_folder_id_list) == 0:
            print("Cloud folder does not exist! , so the file is uploaded to the cloud root")
            return None
        else:
            return get_folder_id_list
    return None


def trashed_file(service, is_delete_trashed_file=False):
    """
    抓取到云端上垃圾桶內的全部文件，进行刪除
    :param service: 认证用
    :param is_delete_trashed_file: 是否要刪除垃圾桶文件
    :return:
    """
    results = service.files().list(fields="nextPageToken, files(id, name)", spaces='drive', q="trashed = true",
                                   ).execute()
    items = results.get('files', [])
    if not items:
        print('垃圾桶无任何文件.')
    else:
        print('垃圾桶文件: ')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            if is_delete_trashed_file is True:
                print("刪除文件为:" + u'{0} ({1})'.format(item['name'], item['id']))
                delete_drive_service_file(service, file_id=item['id'])


def set_timeout(num, callback):
    def wrap(func):
        def handle(signum, frame):  # 收到信号 SIGALRM 后的回调函数，第一个参数是信号的数字，第二个参数是the interrupted stack frame.
            raise RuntimeError
 
        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
                signal.alarm(num)  # 设置 num 秒的闹钟
                print('start alarm signal.')
                r = func(*args, **kwargs)
                print('close alarm signal.')
                signal.alarm(0)  # 关闭闹钟
                return r
            except RuntimeError as e:
                callback()
 
        return to_do
 
    return wrap
 
def after_timeout():  # 超时后的处理函数
    print("Upload picture time out!")

@set_timeout(60, after_timeout)
def upload(file_path=None, file_name=None, update_drive_service_folder_name=None):
    """
    :param is_update_file_function: 判断是否执行上传的功能
    :param update_drive_service_name: 要上传的文件名称
    :param update_drive_service_folder_name: 要上传到网盘的位置
    """

    # print("is_update_file_function")
    # print(type(is_update_file_function))
    # print(is_update_file_function)

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    # print('*' * 10)

    # print(update_file_path + update_drive_service_name)
    print("=====Execute upload file=====")
    # 清空 云端垃圾桶文件
    # trashed_file(service=service, is_delete_trashed_file=True)
    
    get_folder_id = search_folder(service = service, update_drive_folder_name = update_drive_service_folder_name)

    # 查找要上传的文件名称在云端上是否已经存在，存在就删除
    search_file(service=service, update_drive_service_name=file_name,
                is_delete_search_file=True)
    # 文件上传到云端
    name, _ = update_file(service=service, update_drive_service_name=file_name,
                local_file_path=file_path + '/' +file_name, update_drive_service_folder_id=get_folder_id)
   
    print("=====Upload file succeeded=====")
    return name


if __name__ == '__main__':

    name = upload(file_path='/home/pi/picture_file', file_name='20200611-040043.jpg')
    print(name)
