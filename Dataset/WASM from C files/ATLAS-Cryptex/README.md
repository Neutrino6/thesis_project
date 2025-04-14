# ATLAS-Cryptex
Simple example of ransomware execution 
 
ATLAS XOR Cryptex es un ramsomware de tipo demostrativo el cual cifra archivos usando el sistema XOR convencional
en combinacion de una pasada XOR combinacional de segunda ronda de una key periodicamente preestablecida con 
claves de coma flotante.

El código como tal es para enseñar como funciona de manera muy simple un ransomware de manera muy controlada,
si deseas hacer uso practico de el en demos de seguridad o criptografia solo es necesario cambiar una porcion de código,
actualmente 14 de May 2017 no es detectado por ningun antivirus, aunque el cifrado no es tan complejo y puede ser resuelte por
metodos criptograficos en poco tiempo , esto en caso de accidentes (tambien porque es para explicar sencillamente su funcionamiento).

La funcion de autoreplicación esta deshabilitado
por propositos de solo enseñanza de como trabaja 
un mecanismo semicomplejo de ransomware.
	 
En esta version el escaneo de ficheros en determinados directorios esta activado y cifrara cualquier archivo
en su interior.
	 
------------------------------------------------------

ATLAS Laboratories | Mark Security Research Laboratory
