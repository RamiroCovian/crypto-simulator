# crypto-simulator
Proyecto Final Flask | KeepCoding Bootcamp | Aprende a Programar desde Cero (Full Stack Jr. ) | Edición XVII


## Requisitos de instalacion

* **Crear entorno virtual**
  ```
  Windows
  python -m venv env
  --------------------
  Mac/Linux
  python3 -m venv env
  ``````
* **Activar entorno virtual**
  ```
  Windows
  env\Scripts\activate
  --------------------
  Mac/Linux
  source env/bin/activate
  ``````

* **Instalar Requirements**
  ```
  pip install -r requirements.txt
  ```

* **Crear variables de entorno**
  ```
  - Crear un archivo en la carpeta simulador ".env", en el se deben copiar las variables de entorno que se encuentran en el archivo ".env.template"
  ```

* **Crear una base de datos con la siguiente estructura en DB Browser (SQLite)**
  ```
  CREATE TABLE movements (
    id            INTEGER UNIQUE,
    date          TEXT    NOT NULL,
    time          TEXT    NOT NULL,
    from_currency TEXT    NOT NULL,
    from_quantity REAL    NOT NULL,
    to_currency   TEXT    NOT NULL,
    to_quantity   REAL    NOT NULL,
    PRIMARY KEY (
        id AUTOINCREMENT
    )
  );

  ```

* **Crear variables de configuracion**
 ```
  - Crear un archivo en la carpeta simulador "config.py", en el copiar las variables de configuracion que se encuentra dentro del archivo "config.template.py"
  - Modificar las variables "PATH", "SECRET_KEY" y "API_KEY", para esta ultima obtener un Apikey en https://www.coinapi.io/
  ```

* **Abre la terminal**
  ```
  Escribe "flask run"
  ```

* **Funcionamiento App**
  ```
  - La pagina cuenta con tres secciones(Inicio/Compra/Estado)
  En la pag principal te aparecera un listado vacio de movimientos, para poder comenzar a ver movimientos , deberas ingresar en la pag "Compra".
  En ella podras comprar inicialmente con Euros una de las cryptos que se encuentran dentro de la lista a seleccionar,
  deberas ingresar un monto de euros que deseas gastar, luego tendras que presionar en el boton "Calcular" para poder saber cuantas cryptos equivalen, 
  en el momento de la consulta, la cantidad de euros que ingresaste. Si no se calcula la equivalencia, no podras realizar la compra.
  En caso de que se quiera cancelar, podras presionar en el boton "x", que borraria todo el calculo y asi podras ingresar o consultar por otras cryptos o montos.
  Una vez que calculada la equivalencia, podras presionar el boton de aceptar para realizar la compra y asi automaticamente veras el movimiento generado en el listado principal,
  si deseas volver a realizar otra compra tendras a disposicion la cantidad de cryptos que posees en tu wallet(Monedero virtual).
  Y por ultimo, en la pagina de Estado, podras observar la inversion total generada en Euros, podras observar el Valor actual de las cryptos que hayas comprado y finalmente tendras
  la diferencia de inversion (Positivo o Negativo).
  ```
