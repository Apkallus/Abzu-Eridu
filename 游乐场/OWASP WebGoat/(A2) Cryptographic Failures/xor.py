key = 0x5f
ps_str = ';>+>=>,:/>,,(0-;'

ps_decode = ''.join([chr(ord(ch) ^ key) for ch in ps_str])
print(ps_decode)