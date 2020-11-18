# What to do :question:

### Description:

* We have received an anonymous call with the following message: “There was a critical information leakage, an attacker managed to read our emails without internet connection...all we have is this file”

### Challenge:

We got a binary file from the challenge.

We are going to use `Volatility` in order to continue.

First of all, we start with `imageinfo`:

```sh
w3th4nds@void:~/ctfs/ENISA_hackfest_2020/forensics/what_to_do$ volatility -f ./whatodobun.bin imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_23418
                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/w3th4nds/ctfs/ENISA_hackfest_2020/forensics/what_to_do/whatodobun.bin)
                      PAE type : No PAE
                           DTB : 0x187000L
                          KDBG : 0xf800028480a0L
          Number of Processors : 1
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0xfffff80002849d00L
             KUSER_SHARED_DATA : 0xfffff78000000000L
           Image date and time : 2020-11-16 03:55:19 UTC+0000
     Image local date and time : 2020-11-15 19:55:19 -0800
```

Now that we got the profile: `Win7SP1x64`

We are going to use `cmdscan` or `consoles` in order to check some of the actions:

```sh
w3th4nds@void:~/ctfs/ENISA_hackfest_2020/forensics/what_to_do$ volatility -f ./whatodobun.bin --profile Win7SP1x64 consoles
Volatility Foundation Volatility Framework 2.6
**************************************************
ConsoleProcess: conhost.exe Pid: 3972
Console: 0xffc16200 CommandHistorySize: 50
HistoryBufferCount: 1 HistoryBufferMax: 4
OriginalTitle: Windows PowerShell
Title: Windows PowerShell
AttachedProcess: powershell.exe Pid: 3020 Handle: 0x60
----
CommandHistory: 0x3dd940 Application: powershell.exe Flags: Allocated, Reset
CommandCount: 2 LastAdded: 1 LastDisplayed: 1
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x60
Cmd #0 at 0x3ddbb0: cd .\Downloads
Cmd #1 at 0x3dcc70: dir
----
Screen 0x301760 X:120 Y:3000
Dump:
Windows PowerShell                                                                                                      
Copyright (C) 2009 Microsoft Corporation. All rights reserved.                             
PS C:\Users\volf> cd .\Downloads                                                                                        
PS C:\Users\volf\Downloads> dir                                                                                     
    Directory: C:\Users\volf\Downloads                                                                  
Mode                LastWriteTime     Length Name                                                                       
----                -------------     ------ ----                                                                       
-a---        11/15/2020   7:49 PM       1726 flag.eml                                                                   
                                     
PS C:\Users\volf\Downloads> 
```

So, we see there is a `flag.eml` file.

We are now gonna use `filescan` to search for this file in the system.

```sh
w3th4nds@void:~/ctfs/ENISA_hackfest_2020/forensics/what_to_do$ volatility -f ./whatodobun.bin --profile Win7SP1x64 filescan | grep flag
Volatility Foundation Volatility Framework 2.6
0x000000007e1f3330     16      0 RW---d \Device\HarddiskVolume2\Users\volf\Downloads\flag.eml
0x000000007e3e5dc0     16      0 R--r-d \Device\HarddiskVolume2\Users\volf\Downloads\flag.eml
0x000000007fac6070     16      0 RW-rwd \Device\HarddiskVolume2\Users\volf\Downloads\flag.eml
```

Nice! Now we need to find which of these one contains the correct flag file.

We are using `dumpfiles` to dump.

```sh
w3th4nds@void:~/ctfs/ENISA_hackfest_2020/forensics/what_to_do$ volatility -f ./whatodobun.bin --profile Win7SP1x64 dumpfiles -Q 0x000000007e3e5dc0 --dump-dir=./
Volatility Foundation Volatility Framework 2.6
DataSectionObject 0x7e3e5dc0   None   \Device\HarddiskVolume2\Users\volf\Downloads\flag.eml
```

Last step, open the file:

```
w3th4nds@void:~/ctfs/ENISA_hackfest_2020/forensics/what_to_do$ cat file.None.0xfffffa8003a7be10.dat 
MIME-Version: 1.0
Date: Thu, 12 Nov 2020 15:39:11 +0200
References: <CADyiE+fb+ATkQBHod3Ouzo4cqYUndYVqVDYTatSX5m6gH3YhKg@mail.gmail.com>
In-Reply-To: <CADyiE+fb+ATkQBHod3Ouzo4cqYUndYVqVDYTatSX5m6gH3YhKg@mail.gmail.com>
Message-ID: <CAP4-SA33OXHwt8nQsGv=_p3z9D6HCevyeLiSS7dJvocGP=39_Q@mail.gmail.com>
Subject: Fwd: flag
From: Iulia Galea <iuliana.galea@gmail.com>
To: volf.hacking@gmail.com
Content-Type: multipart/alternative; boundary="0000000000007e93c205b3e909d6"

--0000000000007e93c205b3e909d6
Content-Type: text/plain; charset="UTF-8"

---------- Forwarded message ---------
De la: volf hacking <volf.hacking@gmail.com>
Date: mie., 16 sept. 2020 la 17:03
Subject: flag
To: <iuliana.galea@gmail.com>


if you want to meet the secret contact from the agency, you will need this
code
{6b858a61b8074e6a8b0f5ee45bb63c88210922a5ca4c9176d4b7ea2d884ba149}
```

