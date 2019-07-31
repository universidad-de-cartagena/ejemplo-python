from random import shuffle
chars = list('abcdefghijklmnopqrstuvwxyz0123456789!@%^&')
shuffle(chars)
print(''.join(chars[0:50]))
