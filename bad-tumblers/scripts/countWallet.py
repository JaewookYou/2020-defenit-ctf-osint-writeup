#-*- coding: utf-8 -*-
import time

t = 0
while 1:
  with open('wallets.txt') as f:
    lines = f.read().split('\n')
  if t != len(lines):
    t = len(lines)
    print('[+] {}'.format(t))
  time.sleep(1)
