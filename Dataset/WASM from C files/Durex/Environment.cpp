#include "Environment.hpp"

Environment::Environment (char **env)
{
	for (int i = 0; env[i] != NULL; i++) {
		std::vector<std::string> content = Utils::split(std::string(env[i]), '=');
		if (content.size() == 2) {
			this->Variables.push_back(new Variable(content[0], content[1]));
		} else if (content.size() == 1) {
			this->Variables.push_back(new Variable(content[0], ""));
		}
	}
}

Environment::Environment ( Environment const & src )
{
	*this = src;
	return ;
}

Environment &				Environment::operator=( Environment const & rhs )
{
	return (*this);
}

Environment::~Environment ()
{
	for (int i = 0; i < this->Variables.size(); i++) {
		delete this->Variables[i];
	}
}

std::ostream &				operator<<(std::ostream & o, Environment const & i)
{
	return (o);
}


Variable	*Environment::getVariable(std::string var)
{
	for (int i = 0; i < this->Variables.size(); i++)
	{
		if (this->Variables[i]->getVarName() == var) {
			return this->Variables[i];
		}
	}
	return NULL;
}
