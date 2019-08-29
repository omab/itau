# Historial de Cuenta bancaria

Esta simple app permite obtener el historial de movimientos de una cuenta en `I`
`t` `a` `ú`.

## Instalar y correr

``` sh
$ pip install -r requirements.txt
$ FLASK_DEBUG=1 flask run
```

Abre http://localhost:5000

## Uso

Para poder obtener el historial es necesario:

1. Ir al reporte de la cuenta deseada en el portal del banco
2. Abrir el tab de `Network` el `Developer Tools` (Chrome), y filtrar por
   requests del tipo `XHR`
3. Ir a la sección de `Consulta Histórica`
4. Seleccionar una de las fechas disponibles
5. Copiar como `cURL` la request realizada al endpoint `consultaHistorica`

Con la copia del request en formato `cURL` ve a `http://localhost:5000` y pega
la misma en formulario.
