from random import shuffle
chars = list('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
shuffle(chars)
print(''.join(chars[0:50]))