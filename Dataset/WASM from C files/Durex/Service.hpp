#ifndef SERVICE_HPP
# define SERVICE_HPP
#include "all.hpp"

class Service
{
	public:

		Service(std::string);
		Service( Service const & src );
		virtual ~Service();

		Service &							operator=( Service const & rhs );
		friend std::ostream &				operator<<(std::ostream & o, Service const & i);

		std::string		getServiceTemplate();
		void			initService();
	private:
		std::string executable;
};

#endif
