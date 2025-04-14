#ifndef CLIENT_HPP
# define CLIENT_HPP

#include "all.hpp"
# include <sys/socket.h>
# include <arpa/inet.h>
# include "RemoteShell.hpp"

# define CLIENT_BUFFER 4096
# define CLIENT_READ 4095
class Server;
class Client
{
	public:

		Client( int fd, struct sockaddr_in	&in, Server *server);
		Client( Client const & src );
		virtual ~Client( void );
		static void clientThread(Client *client);

		Client &							operator=( Client const & rhs );
		friend std::ostream &				operator<<(std::ostream & o, Client const & i);
		std::string				getAddress();
		bool					authenticateClient();
		void					printPrompt(bool new_line);
		Server					*server;
		int 					fd;
		std::string				address;
		struct sockaddr_in		in;
};

#endif
