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