# <div align="center">Red social de imágenes</div>

## Página principal
<img src="Inicio.png">

## Registro de cuenta (ruta: /registrarse)
Para crear la cuenta es necesario rellenar todos los campos del formulario. Si el usuario o el correo ya han sido registrados, se muestra otra vez la página de registro con un mensaje indicando que el usuario no está disponible o el correo ha sido registrado. Si es un usuario completamente nuevo, se verifica el formato del email. Para la contraseña es necesario tener *al menos una mayúscula y un número*.

<img src="Registro.png">

## Activación de cuenta (ruta: /confirmar_correo/<activación>)

El usuario tiene 600 segundos para acceder a este link y, una vez ingrese, se indica un mensaje con la activación exitosa y la actualización de la variable activo a 1 en la base de datos. Si no accede en este tiempo, el enlace deja de ser funcional enviando un mensaje de que ha expirado.

<img src="confirmarcorreo.png">

## Inicio de sesión (ruta: /Iniciosesion)

<img src="iniciosesion.png">
