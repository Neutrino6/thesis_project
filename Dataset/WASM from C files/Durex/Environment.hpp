#ifndef ENVIRONMENT_HPP
# define ENVIRONMENT_HPP
#include "all.hpp"
#include "Utils.hpp"
class Variable {
	public:
	Variable(std::string var, std::string value) {
		this->var = var;
		this->value = value;
	}
	std::string getVarName() { return this->var; }
	std::string getVarValue() { return this->value; }
private:
	std::string var;
	std::string value;
};

class Environment
{
	public:

		Environment(char **env);
		Environment( Environment const & src );
		virtual ~Environment( void );

		Environment &							operator=( Environment const & rhs );
		friend std::ostream &				operator<<(std::ostream & o, Environment const & i);
		Variable *getVariable(std::string var);

	private:
		std::vector<Variable*>			Variables;
};

#endif
