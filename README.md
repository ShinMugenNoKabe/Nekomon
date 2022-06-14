<h1>Nekomon</h1>

<p>Nekomon es una red social completamente gratuita y sencilla de utilizar,
creada desde cero utilizando Python.</p>
<p>Puedes encontrar la web en <a href="https://www.nekomon.es">https://www.nekomon.es</a>.</p>

<h3>Tecnologías a usar:</h3>
<ul>
    <li>Framework para backend: <b>Django</b></li>
    <li>Framework JS para frontend: <b>jQuery</b></li>
    <li>IDE: <b>PyCharm/Visual Studio Code</b></li>
    <li>VPS desplagado en: <b>Contabo</b></li>
    <li>Servidor web: <b>NGINX</b></li>
    <li>Servidor proxy para los WebSockets: <b>Daphne</b></li>
    <li>Servidor de bases de datos: <b>MySQL</b></li>
    <li>Servidor de correo: <b>Postfix</b></li>
    <li>Dominio registrado en: <b>GoDaddy</b></li>
    <li>Autoridad de Certificación: <b>Let’s Encrypt</b></li>
</ul>

<p>Nekomon.es además viene incorporado con un Bot de Discord completamente funcional, el cual recibe datos de entidades desde una API REST y los muestra al usuario.</p>

El Bot puede mostrar los datos de un usuario o de un post. Para cada uno de ellos, se debe de escribir en un canal de texto el enlace del usuario o post. Ejemplo:<br>
<code>https://www.nekomon.es/Godofredo</code><br>
<code>https://www.nekomon.es/posts/1</code><br>

Puedes añadir el Bot a tu servidor haciendo click en <a href="https://discord.com/api/oauth2/authorize?client_id=981836167622299668&permissions=3147776&scope=bot">este enlace</a>.

La memoria del proyecto está disponible en <a href="https://github.com/ShinMugenNoKabe/Nekomon/raw/master/%C3%8Dndice%20memoria%20Proyecto%20final%20DAW.pdf">este enlace</a>.

<h3>Pasos para despliegue</h3>
<ol>
    <li>Clonar el repositorio con <code>git clone https://github.com/ShinMugenNoKabe/Nekomon.git</code></li>
    <li>Instalar Python y el <a href="https://phoenixnap.com/kb/install-pip-windows">gestor de paquetes PIP</a></li>
    <li>Crear un entorno virtual con <code>virtualenv nekomon</code></a></li>
    <li>Instalar todos los paquetes necesarios con <code>pip install -r requirements.txt</code></a></li>
    <li>Modificar las credenciales de MySQL en la carpeta de config.</li>
    <li>Crear un fichero .env con las variables:
        <ul>
            <li>SECRET_KEY - Clave secreta única de Django.</li>
            <li>EMAIL_HOST_USER - E-mail usado para enviar correos.</li>
            <li>EMAIL_HOST_PASSWORD - Contraseña de aplicación del e-mail.</li>
            <li>DEFAULT_FROM_EMAIL - Nombre que aparece en los correos.</li>
            <li>IMGUR_CLIENT_ID - ID de cliente de Imgur.</li>
            <li>IMGUR_API_KEY - Clave de API de Imgur.</li>
            <li>DISCORD_TOKEN - Token del Bot de Discord.</li>
        </ul>
    </li>
    <li>Crear una nueva base de datos con el nombre elegido, por defecto <code>nekomon</code></li>
    <li>Aplicar las migraciones con <code>python manage.py migrate</code></a></li>
    <li>Ejecutar el servidor con <code>python manage.py runserver</code></a></li>
<ol>