#ifndef REMOTESHELL_HPP
# define REMOTESHELL_HPP

#include "all.hpp"
#include "pstream.h"
#include "Utils.hpp"
class Client;
class RemoteShell
{
	public:

		RemoteShell(Client *client);
		RemoteShell( RemoteShell const & src );
		virtual			~RemoteShell();
		void			handleShell();
		void			printPrompt();
		void			initShell();
		bool			handleChdir(std::string buf);
		std::string		getAbovePath();
		bool			pathExist(std::string path);

		RemoteShell &							operator=( RemoteShell const & rhs );
		friend std::ostream &				operator<<(std::ostream & o, RemoteShell const & i);
	private:
		Client		*client;
		std::string	path;
};

#endif
