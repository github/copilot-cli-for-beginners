![Capítulo 00: Inicio rápido](../../../00-quick-start/images/chapter-header.png)

¡Bienvenido! En este capítulo instalarás GitHub Copilot CLI (Command Line Interface), iniciarás sesión con tu cuenta de GitHub y verificarás que todo funciona. Es un capítulo corto de configuración. Una vez que esté funcionando, ¡las demos de verdad empiezan en el Capítulo 01!

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, habrás:

- Instalado GitHub Copilot CLI
- Iniciado sesión con tu cuenta de GitHub
- Verificado que funciona con una prueba sencilla

> ⏱️ **Tiempo estimado**: ~10 minutos (5 min de lectura + 5 min de práctica)

---

## ✅ Requisitos previos

- **Cuenta de GitHub** con acceso a Copilot. [Consulta las opciones de suscripción](https://github.com/features/copilot/plans). Estudiantes y profesores pueden acceder a Copilot Pro de [forma gratuita a través de GitHub Education](https://education.github.com/pack).
- **Conocimientos básicos de terminal**: te resulta cómodo usar comandos como `cd` y `ls`

### Qué significa "acceso a Copilot"

GitHub Copilot CLI requiere una suscripción activa a Copilot. Puedes consultar tu estado en [github.com/settings/copilot](https://github.com/settings/copilot). Deberías ver una de estas opciones:

- **Copilot Individual**: suscripción personal
- **Copilot Business**: a través de tu organización
- **Copilot Enterprise**: a través de tu empresa
- **GitHub Education**: gratis para estudiantes y profesores verificados

Si ves "You don't have access to GitHub Copilot", tendrás que usar la opción gratuita, suscribirte a un plan o unirte a una organización que te dé acceso.

---

## Instalación

> ⏱️ **Estimación de tiempo**: la instalación tarda entre 2 y 5 minutos. La autenticación añade otros 1 o 2 minutos.

### GitHub Codespaces (cero configuración)

Si no quieres instalar ninguno de los requisitos previos, puedes usar GitHub Codespaces, que ya trae GitHub Copilot CLI listo para usar (solo tendrás que iniciar sesión) y trae Python y pytest preinstalados.

1. [Haz un fork de este repositorio](https://github.com/github/copilot-cli-for-beginners/fork) en tu cuenta de GitHub
2. Selecciona **Code** > **Codespaces** > **Create codespace on main**
3. Espera unos minutos a que se construya el contenedor
4. ¡Ya está! La terminal se abrirá automáticamente en el entorno del Codespace.

> 💡 **Verifica en el Codespace**: ejecuta `cd samples/book-app-project && python book_app.py help` para confirmar que Python y la app de ejemplo funcionan.

### Instalación local

Sigue estos pasos si quieres ejecutar Copilot CLI en tu máquina local con los ejemplos del curso.

1. Clona el repo para tener los ejemplos del curso en tu máquina:

    ```bash
    git clone https://github.com/github/copilot-cli-for-beginners
    cd copilot-cli-for-beginners
    ```

2. Instala Copilot CLI usando una de las siguientes opciones.

    > 💡 **¿No sabes cuál elegir?** Usa `npm` si tienes Node.js instalado. En caso contrario, elige la opción que se ajuste a tu sistema.

    ### Todas las plataformas (npm)

    ```bash
    # Si tienes Node.js instalado, esta es una forma rápida de obtener el CLI
    npm install -g @github/copilot
    ```

    ### macOS/Linux (Homebrew)

    ```bash
    brew install copilot-cli
    ```

    ### Windows (WinGet)

    ```bash
    winget install GitHub.Copilot
    ```

    ### macOS/Linux (script de instalación)

    ```bash
    curl -fsSL https://gh.io/copilot-install | bash
    ```

<details>
<summary>Opcional: habilitar la autocompletado del shell con Tab</summary>

La autocompletado con Tab del shell te permite pulsar **Tab** para completar subcomandos de `copilot`, opciones de comando y algunos valores de opciones. Es opcional, pero puede resultar muy útil cuando ya te sientas cómodo usando el CLI.

Copilot CLI actualmente soporta scripts de autocompletado para Bash, Zsh y Fish:

```shell
# Bash, solo en la sesión actual
source <(copilot completion bash)

# Bash, persistente en Linux
copilot completion bash | sudo tee /etc/bash_completion.d/copilot

# Zsh
copilot completion zsh > "${fpath[1]}/_copilot"

# Fish
copilot completion fish > ~/.config/fish/completions/copilot.fish
```

Reinicia tu shell después de añadir la autocompletado persistente. PowerShell está soportado para ejecutar Copilot CLI en Windows, pero `copilot completion` actualmente solo soporta Bash, Zsh y Fish.

</details>

---

## Autenticación

Abre una ventana de terminal en la raíz del repositorio `copilot-cli-for-beginners`, inicia el CLI y permite el acceso a la carpeta.

```bash
copilot
```

Se te pedirá que confíes en la carpeta que contiene el repositorio (si aún no lo has hecho). Puedes confiar en ella por una vez o para todas las sesiones futuras.

<img src="../../../00-quick-start/images/copilot-trust.png" alt="Confiando en archivos de una carpeta con el Copilot CLI" width="800"/>

Después de confiar en la carpeta, puedes iniciar sesión con tu cuenta de GitHub.

```
> /login
```

**Lo que ocurre a continuación:**

1. Copilot CLI muestra un código de un solo uso (como `ABCD-1234`)
2. Tu navegador se abre en la página de autorización de dispositivos de GitHub. Inicia sesión en GitHub si aún no lo has hecho.
3. Introduce el código cuando se te pida
4. Selecciona "Authorize" para conceder acceso a GitHub Copilot CLI
5. Vuelve a tu terminal: ¡ya tienes la sesión iniciada!

<img src="../../../00-quick-start/images/auth-device-flow.png" alt="Flujo de autorización de dispositivo: muestra el proceso de 5 pasos desde el inicio de sesión en la terminal hasta la confirmación de sesión iniciada" width="800"/>

*El flujo de autorización de dispositivo: tu terminal genera un código, lo verificas en el navegador y Copilot CLI queda autenticado.*

**Tip**: el inicio de sesión persiste entre sesiones. Solo necesitas hacerlo una vez, salvo que tu token caduque o cierres sesión explícitamente.

---

## Verifica que funciona

### Paso 1: prueba Copilot CLI

Ahora que tienes la sesión iniciada, vamos a verificar que Copilot CLI te funciona. En la terminal, inicia el CLI si aún no lo has hecho:

```bash
> Say hello and tell me what you can help with
```

Después de recibir una respuesta, puedes salir del CLI:

```bash
> /exit
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demo de hola](../../../00-quick-start/images/hello-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas serán distintos a los que se muestran aquí.*

</details>

---

**Salida esperada**: una respuesta amistosa que enumera las capacidades de Copilot CLI.

### Paso 2: ejecuta la app de ejemplo de libros

El curso incluye una app de ejemplo que explorarás y mejorarás a lo largo del curso usando el CLI *(puedes ver el código en /samples/book-app-project)*. Comprueba que la *app de terminal de colección de libros en Python* funciona antes de empezar. Ejecuta `python` o `python3` según tu sistema.

> **Nota:** los ejemplos principales del curso usan Python (`samples/book-app-project`), así que necesitarás tener [Python 3.10+](https://www.python.org/downloads/) disponible en tu máquina local si elegiste esa opción (el Codespace ya lo trae instalado). También están disponibles las versiones en JavaScript (`samples/book-app-project-js`) y C# (`samples/book-app-project-cs`) por si prefieres trabajar con esos lenguajes. Cada ejemplo tiene un README con instrucciones para ejecutar la app en ese lenguaje.

```bash
cd samples/book-app-project
python book_app.py list
```

**Salida esperada**: una lista de 5 libros que incluye "The Hobbit", "1984" y "Dune".

### Paso 3: prueba Copilot CLI con la app de libros

Vuelve primero a la raíz del repositorio (si has ejecutado el Paso 2):

```bash
cd ../..   # Vuelve a la raíz del repositorio si es necesario
copilot 
> What does @samples/book-app-project/book_app.py do?
```

**Salida esperada**: un resumen de las funciones y comandos principales de la app de libros.

Si ves un error, consulta la [sección de solución de problemas](#troubleshooting) más abajo.

Cuando termines puedes salir de Copilot CLI:

```bash
> /exit
```

---

## ✅ ¡Estás listo!

Eso es todo en cuanto a la instalación. La diversión de verdad empieza en el Capítulo 01, donde:

- Verás cómo la IA revisa la app de libros y encuentra problemas de calidad de código al instante
- Aprenderás tres formas distintas de usar Copilot CLI
- Generarás código funcional a partir de inglés sencillo

**[Continuar al Capítulo 01: Primeros pasos →](../01-setup-and-first-steps/README.md)**

---

## Solución de problemas

### "copilot: command not found"

El CLI no está instalado. Prueba con otro método de instalación:

```bash
# Si brew falló, prueba npm:
npm install -g @github/copilot

# O el script de instalación:
curl -fsSL https://gh.io/copilot-install | bash
```

### "You don't have access to GitHub Copilot"

1. Verifica que tienes una suscripción a Copilot en [github.com/settings/copilot](https://github.com/settings/copilot)
2. Comprueba que tu organización permite el acceso al CLI si usas una cuenta de trabajo

### "Authentication failed"

Vuelve a autenticarte:

```bash
copilot
> /login
```

### El navegador no se abre automáticamente

Visita manualmente [github.com/login/device](https://github.com/login/device) e introduce el código que aparece en tu terminal.

### Token caducado

Simplemente vuelve a ejecutar `/login`:

```bash
copilot
> /login
```

### ¿Sigues atascado?

- Consulta la [documentación de GitHub Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- Busca en [GitHub Issues](https://github.com/github/copilot-cli/issues)

---

## 🔑 Conclusiones clave

1. **Un GitHub Codespace es una forma rápida de empezar**: Python, pytest y GitHub Copilot CLI vienen preinstalados, así que puedes saltar directamente a las demos
2. **Varios métodos de instalación**: elige el que funcione en tu sistema (Homebrew, WinGet, npm o script de instalación)
3. **Autenticación de una sola vez**: el inicio de sesión persiste hasta que el token caduca
4. **La app de libros funciona**: usarás `samples/book-app-project` durante todo el curso

> 📚 **Documentación oficial**: [Instalar Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started) para opciones de instalación y requisitos.

> 📋 **Referencia rápida**: consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para ver la lista completa de comandos y atajos.

---

**[Continuar al Capítulo 01: Primeros pasos →](../01-setup-and-first-steps/README.md)**
