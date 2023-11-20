import paramiko


def upload_files(host, user, passwd, local_path, remote_path, port=22):
    print(f"Загружаем фаил {local_path} в каталог {remote_path}")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def download_files(host, user, passwd, local_path, remote_path, port=22):
    print(f"Скачиваем фаил {local_path} в каталог {remote_path}")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()