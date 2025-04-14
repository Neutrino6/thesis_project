# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: frmarinh <frmarinh@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/05/20 17:57:50 by frmarinh          #+#    #+#              #
#    Updated: 2017/09/18 04:57:47 by frmarinh         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME_DUREX	=	Durex

NAME		=   Durex
NAMEBASE    =   $(shell basename $(NAME))
LENGTHNAME	=	`printf "%s" $(NAMEBASE) | wc -c`
MAX_COLS	=	$$(echo "$$(tput cols)-24-$(LENGTHNAME)"|bc)

CC			=	g++ -L /usr/lib/ -std=c++11 -lpthread
FLAGS_O		=

SRCDIR_DUREX		=	srcs/
OBJDIR_DUREX		=	objs/

INCDIR				=	includes/

SRCBASE_DUREX	=	\
					main.cpp			\
					Durex.cpp			\
					Environment.cpp		\
					Service.cpp			\
					Utils.cpp			\
					Server.cpp			\
					Client.cpp			\
					RemoteShell.cpp		\
					ProcessHider.cpp

INCS			=	$(addprefix $(INCDIR), $(INCBASE))

SRCS_DUREX			=	$(addprefix $(SRCDIR_DUREX), $(SRCBASE_DUREX))
OBJS_DUREX			=	$(addprefix $(OBJDIR_DUREX), $(SRCBASE_DUREX:.cpp=.o))

.SILENT:

all:		$(NAME)

$(NAME):
	if test -f $(NAME_DUREX) ; then											\
		echo "make: Nothing to be done for \`all\`.";				        		\
	else																			\
		make DUREX && 														\
		echo "\r\033[38;5;184m👥  AUTHOR(s): \033[0m\033[K" && 						\
		echo "\r\033[38;5;15m`cat auteur | sed s/^/\ \ \ \ -/g`\033[0m\033[K" &&	\
		echo "\033[38;5;44m☑️  ALL    $(NAMEBASE) is done\033[0m\033[K";			\
	fi

$(OBJDIR_DUREX):
	mkdir -p $(OBJDIR_DUREX)
	mkdir -p $(dir $(OBJS_DUREX))

$(OBJDIR_DUREX)%.o : $(SRCDIR_DUREX)%.cpp | $(OBJDIR_DUREX)
	$(CC) $(FLAGS) -MMD -c $< -o $@											\
		-I $(INCDIR)														\
		-I $(INCDIR)

fcleanlib:	fclean

re:			fclean all

relib:		fclean fcleanlib all

.PHONY:		fclean fcleanlib clean re relib

DUREX: $(OBJDIR_DUREX) $(OBJS_DUREX)
	$(CC) $(FLAGS) $(FLAGS_O) -o $(NAME_DUREX) $(OBJS_DUREX)
	echo "\r\033[38;5;22m📗  MAKE $(NAME_DUREX)"

clean:
	@rm -rf $(OBJDIR_DUREX)
	echo "\r\033[38;5;124m📕  CLEAN $(OBJDIR_DUREX)\033[0m\033[K";

fclean:		clean
	@rm -rf $(NAME_DUREX)
	echo "\r\033[38;5;124m📕  FCLEAN $(NAME_DUREX)\033[0m\033[K";

-include $(OBJS:.o=.d)
