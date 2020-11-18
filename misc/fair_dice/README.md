# Fair Dice :game_die:

### Description:

* Are you willing to throw dices and try your luck at DCTF?

### Challenge:

The interface of the program looks like this:

```sh
w3th4nds@void:~/github/ENISA_Hackfest_2020/misc/fair_dice$ nc 35.242.192.203 30769
Welcome to a fair dice game.
 - We are going to play some fair rounds. Let's say 101.
 - We both throw one dice. The biggest numbered showed on the dice, wins!
 - The person who wins more rounds from 101, wins that game.
 - If you win too many games in the same session, I am going to alter the game rules to make it fairer for me.
 - If you are going to win four games, I will give you a special code.
 - Note that I am getting bored very fast and I will close this game soon.
Should we start?y
Let me show you first 3 dices we are going to play:

Here is the blue dice:

       xxxxxxx
       x     x
       x  3  x
       x     x
       xxxxxxx
xxxxxxxxxxxxxxxxxxxxx
x     xx     xx     x
x  3  xx  6  xx  3  x
x     xx     xx     x
xxxxxxxxxxxxxxxxxxxxx
       xxxxxxx
       x     x
       x  3  x
       x     x
       xxxxxxx
       xxxxxxx
       x     x
       x  3  x
       x     x
       xxxxxxx
Ok?y

Here is the yellow dice:

       xxxxxxx
       x     x
       x  5  x
       x     x
       xxxxxxx
xxxxxxxxxxxxxxxxxxxxx
x     xx     xx     x
x  5  xx  5  xx  2  x
x     xx     xx     x
xxxxxxxxxxxxxxxxxxxxx
       xxxxxxx
       x     x
       x  2  x
       x     x
       xxxxxxx
       xxxxxxx
       x     x
       x  2  x
       x     x
       xxxxxxx
```

So, we have to win 4 games in row, each game has 101 rounds.

Pretty simple and straight-forward.

### Exploit:

```python
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
```

### PoC

![Imgur](https://i.imgur.com/jFiWStI.png)