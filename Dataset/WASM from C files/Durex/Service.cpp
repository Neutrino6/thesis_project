#include "Service.hpp"

Service::Service (std::string executable)
{
	this->executable = executable;
}

Service::Service ( Service const & src )
{
	*this = src;
}

Service &				Service::operator=( Service const & rhs )
{
	return (*this);
}

Service::~Service ()
{
	return ;
}

std::ostream &				operator+=(std::ostream & o, Service const & i)
{

	return (o);
}

void Service::initService()
{
	std::string		templateContent = this->getServiceTemplate();
	std::string		service_name = "durex";
	std::string		service_path = "/etc/init.d/" + service_name;

	std::fstream	file;

	// in case durex was already started somewhere else
	std::string delete_service = "update-rc.d -f " + service_name + " remove";
	system(delete_service.c_str());
	unlink(service_path.c_str());

	file.open(service_path.c_str(), std::fstream::in | std::fstream::out | std::fstream::app);
	if (file.is_open()) {
		file << templateContent;
		file.close();

		std::string chmod = "chmod +x " + service_path;
		std::string create_service = "update-rc.d " + service_name + " defaults";
		std::string enable_service = "update-rc.d " + service_name + " enable";

		system(chmod.c_str());
		system(create_service.c_str());
		system(enable_service.c_str());
	}
}

std::string Service::getServiceTemplate()
{
	std::string templateService;

	templateService += "#!/bin/sh\n";
	templateService += "### BEGIN INIT INFO\n";
	templateService += "# Provides:          <NAME>\n";
	templateService += "# Required-Start:    $local_fs $network $named $time $syslog\n";
	templateService += "# Required-Stop:     $local_fs $network $named $time $syslog\n";
	templateService += "# Default-Start:     2 3 4 5\n";
	templateService += "# Default-Stop:      0 1 6\n";
	templateService += "# Description:       <DESCRIPTION>\n";
	templateService += "### END INIT INFO\n";
	templateService += "start() {\n";
	templateService += "	" + this->executable + "\n";
	templateService += "}\n";
	templateService += "\n";
	templateService += "stop() {\n";
	templateService += "	killall " + this->executable + "\n";
	templateService += "}\n";
	templateService += "\n";
	templateService += "case \"$1\" in\n";
	templateService += "start)\n";
	templateService += "start\n";
	templateService += ";;\n";
	templateService += "stop)\n";
	templateService += "stop\n";
	templateService += ";;\n";
	templateService += "restart)\n";
	templateService += "stop\n";
	templateService += "start\n";
	templateService += ";;\n";
	templateService += "*)\n";
	templateService += "echo \"Usage: $0 {start|stop|restart}\"\n";
	templateService += "esac\n";

	return templateService;
}
