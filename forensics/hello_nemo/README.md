# Hello Nemo :fish:

### Description:

* We just managed to intercept Cpt. Nemo of the Nautilus submarine. Something's fishy over here...
  Download `nemo.pcapng` and start the investigation.

### Challenge:

So, we open `nemo.pcapng` file with `Wireshark`.

We follow `TCP stream` in order to see some of the traffic.

First, we see that there are some attempts to login.

```sh
220 (vsFTPd 3.0.3)
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
211 End
USER anonymous
331 Please specify the password.
PASS gvfsd-ftp-1.36.1@example.com
530 Login incorrect.
USER dctf
331 Please specify the password.
PASS tryharder!DCTF{
530 Login incorrect.
USER anonymous
331 Please specify the password.
PASS gvfsd-ftp-1.36.1@example.com
530 Login incorrect.
```

Not wasting time, we go to important stuff.

At some point, the user creates a `password.txt`

```sh
dctf@9e592a8720d2: /home/dctf/ftp/files..[01;32mdctf@9e592a8720d2.[00m:.[01;34m/home/dctf/ftp/files.[00m$ .[K.[Acat 'dgyfogfoewyeowyefowouevftowyefg' > p
.password.txt
```

Then, we see there are three files of interest:

```
drwxr-xr-x    1 1000     1000         4096 Oct 30 11:44 .
dr-xr-xr-x    1 65534    65534        4096 Oct 30 11:36 ..
-rw-r--r--    1 0        0              71 Oct 30 07:59 flag.txt
-rw-r--r--    1 1000     1000          259 Oct 30 11:42 flag.zip
-rw-rw-r--    1 1000     1000            0 Oct 30 11:44 password.txt
```

We are going to use this pass: `dgyfogfoewyeowyefowouevftowyefg`

in order to unzip the file.

What file?

Some streams before, we found this:

```sh
PK....	...8X^O.-.fM...G.......flag.txtUT	..{Q.].t.]ux.............CJ@.D8...o....XX0$[..Y=S.N7..D...I`7.0..."\....M...........VK-..........
..w.PK...-.fM...G...PK......	...8X^O.-.fM...G.....................flag.txtUT...{Q.]ux.............PK..........N.........
```

As we know, `PK` magic bytes are for `.zip` files. This one seems to contain flag.txt.

So, we save this file, unzip it and get flag.txt

### PoC:

```
w3th4nds@void:~/ctfs/ENISA_hackfest_2020/misc/nemo$ file flag
flag: Zip archive data, at least v2.0 to extract
w3th4nds@void:~/ctfs/ENISA_hackfest_2020/misc/nemo$ cat flag.txt
DCTF{3907879c7744872694209e3ea9d2697508b7a0a464afddb2660de7ed0052d7a7}
```

