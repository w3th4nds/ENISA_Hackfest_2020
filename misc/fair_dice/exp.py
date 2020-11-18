#!/usr/bin/python3
from pwn import *

ip = '35.242.192.203' # change this
port = 30769 # change this
flag = b''

def game1(red, bl, rc, rl, ru, sla):
	sla('Should we start?', 'y')
	for i in range(3):
		sla('Ok?', 'y')
	counter = 0
	for i in range (101):
		counter += 1
		sla('red:', red)
		same_dice = rl()
		if b'Hey' in same_dice:
			sla('red:', bl)
		if counter % 20 == 0:
			print('Round A: {}'.format(counter))
	ru('win!\n')
	rl()
	win = rl()
	if b'I won' in win:
		print('ROUND LOST!')
		return False
	print('ROUND WON!')
	return True 

def game2(red, bl, rc, rl, ru, sla):
	counter = 0
	for i in range (101):
		counter += 1
		sla('red:', red)
		same_dice = rl()
		if b'Hey' in same_dice:
			sla('red:', bl)
		if counter % 20 == 0: 
			print('Round B: {}'.format(counter))
	ru('win!\n')
	rl()
	win = rl()
	if b'I won' in win:
		print('ROUND LOST!')
		return False
	print('ROUND WON!')
	return True

def game3(red, bl, rc, rl, ru, sla):
	for i in range(4):
		sla('Ok?', 'y')
	counter = 0
	for i in range (101):
		counter += 1
		sla('green:', red)
		same_dice = rl()
		if b'Hey' in same_dice:
			sla('green:', bl)
		if counter % 20 == 0: 
			print('Round C: {}'.format(counter))
	ru('win!\n')
	rl()
	win = rl()
	if b'I won' in win:
		print('ROUND LOST!')
		return False
	print('ROUND WON!')
	return True

def game4(red, bl, rc, rl, ru, sla):
	counter = 0
	for i in range (101):
		counter += 1
		sla('green:', red)
		same_dice = rl()
		if b'Hey' in same_dice:
			sla('green:', bl)
		if counter % 20 == 0:
			print('Round D: {}'.format(counter))
	ru('win!\n')
	rl()
	win = rl()
	if b'You won' in win:
		ru('DCTF')
		flag = rl()
		print('Flag: DCTF{}'.format(flag))
		return True
	return False

def pwn():
	red = 'red'
	bl = 'blue'
	fl = True
	tries = 1
	while fl:
		print('Try No: {}'.format(tries))
		r = remote(ip, port)
		rc = lambda : r.recv()
		cl = lambda : r.close()
		rl = lambda : r.recvline()
		ru = lambda x : r.recvuntil(x)
		sla = lambda x,y : r.sendlineafter(x,y)
		if game1(red, bl, rc, rl, ru, sla):
			if game2(red, bl, rc, rl, ru, sla):
				if game3(red, bl, rc, rl, ru, sla):
					if game4(red, bl, rc, rl, ru, sla):
						print('Success!')
						fl = False
		cl()
		tries += 1
	

if __name__ == '__main__':
	pwn()
