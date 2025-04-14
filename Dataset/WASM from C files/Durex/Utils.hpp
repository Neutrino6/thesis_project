#ifndef UTILS_HPP
# define UTILS_HPP

#include "all.hpp"
class Utils
{
	public:

		Utils();
		Utils( Utils const & src );
		virtual ~Utils();

		Utils &								operator=( Utils const & rhs );
		friend std::ostream &				operator<<(std::ostream & o, Utils const & i);
		static std::vector<std::string>		split(const std::string &s, char delim);
		static std::string					getCurrentPath();

		template<typename Out>
		static void split(const std::string &s, char delim, Out result);
};

#endif
