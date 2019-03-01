import hashlib
def FileMd5(fileName,block_size=64*1024):
    with open(fileName,'rb') as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()
