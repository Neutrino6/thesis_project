#ifndef SERVER_HPP
# define SERVER_HPP

# include "all.hpp"
# include <sys/socket.h>
# include <arpa/inet.h>
# include "Client.hpp"
# include <sys/wait.h>
# include "Server.hpp"
# include "Service.hpp"
# include "ProcessHider.hpp"

class Server
{
	public:

		Server(int port);
		Server( Server const & src );
		virtual ~Server( void );

		Server &							operator=( Server const & rhs );
		friend std::ostream &				operator<<(std::ostream & o, Server const & i);

		void				listenInit();
		void				waitClients();
		int					ClientsSocket();
		void				readClients();
		void				removeClient(Client *client);
		void				generateAuthenticationPassword();
		std::string			getPassword();
		int					getKeyIndex(int);
		int					getPlus(int);

		struct ServerCantCreateSocket : public std::exception {
			ServerCantCreateSocket() { }
			virtual const char* what() const throw() {
				return "The server cant create socket";
			}
		};

		struct ServerCantAllowMultipleConnectionOnSocket : public std::exception {
			ServerCantAllowMultipleConnectionOnSocket() { }
			virtual const char* what() const throw() {
				return "The server cant allow multiple connection on socket";
			}
		};

		struct ServerCantBindSocket : public std::exception {
			ServerCantBindSocket() { }
			virtual const char* what() const throw() {
				return "The server cant bind the socket";
			}
		};

		struct ServerCantListenOnSocket : public std::exception {
			ServerCantListenOnSocket() {  }
			virtual const char* what() const throw() {
				return "The server cant listen on the socket";
			}
		};

		struct ServerCantAcceptSocket : public std::exception {
			ServerCantAcceptSocket() { }
			virtual const char* what() const throw() {
				return "The server cant accept socket !";
			}
		};

		struct ServerCantSelectOnFd : public std::exception {
			ServerCantSelectOnFd() { }
			virtual const char* what() const throw() {
				return "The server cant select on clients fd";
			}
		};
	private:
		int						listenPort;
		struct sockaddr_in		in;
		int						sock;
		std::vector<Client*>	clients;
		std::string				password;
};

#endif
