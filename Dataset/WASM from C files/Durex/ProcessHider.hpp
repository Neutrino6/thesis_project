#ifndef PROCESSHIDER_HPP
# define PROCESSHIDER_HPP
#include "all.hpp"

class ProcessHider
{
	public:

		ProcessHider();
		ProcessHider( ProcessHider const & src );
		virtual	~ProcessHider();
		void	initLibrary();
		std::string getRawLibrary();

		ProcessHider &							operator=( ProcessHider const & rhs );
		friend std::ostream &				operator<<(std::ostream & o, ProcessHider const & i);
};

#endif
