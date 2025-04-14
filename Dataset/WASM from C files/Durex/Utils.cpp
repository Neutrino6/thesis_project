#include "Utils.hpp"

Utils::Utils ()
{
	return ;
}

Utils::Utils ( Utils const & src )
{
	*this = src;
}

Utils &				Utils::operator=( Utils const & rhs )
{
	return (*this);
}

Utils::~Utils ()
{
	return ;
}

std::ostream &				operator<<(std::ostream & o, Utils const & i)
{

	return (o);
}

template<typename Out>
void Utils::split(const std::string &s, char delim, Out result) {
	std::stringstream ss;
	ss.str(s);
	std::string item;
	while (std::getline(ss, item, delim)) {
		*(result++) = item;
	}
}

std::vector<std::string> Utils::split(const std::string &s, char delim) {
	std::vector<std::string> elems;
	Utils::split(s, delim, std::back_inserter(elems));
	return elems;
}

std::string Utils::getCurrentPath()
{
    char arg1[20];
    char exe_path[PATH_MAX + 1] = { 0 };

    sprintf(arg1, "/proc/%d/exe", getpid());
    readlink(arg1, exe_path, 1024);
    return std::string(exe_path);
}
