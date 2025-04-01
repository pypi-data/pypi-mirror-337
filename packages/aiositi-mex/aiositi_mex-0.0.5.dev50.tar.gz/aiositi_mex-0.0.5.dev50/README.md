# siti-python
[![release](https://github.com/cuenca-mx/siti-python/actions/workflows/release.yml/badge.svg)](https://github.com/cuenca-mx/siti-python/actions/workflows/release.yml)
[![test](https://github.com/cuenca-mx/siti-python/actions/workflows/test.yml/badge.svg)](https://github.com/cuenca-mx/siti-python/actions/workflows/test.yml)

Cliente para enviar reportes a la CNBV por medio de la plataforma SITI
Documentación: https://sitiapiqa.cnbv.gob.mx/devportal/apis/

La manera sugerida para llenar reportes es por medio de diccionarios con el formato del modelo:

## Desde diccionarios

```python
from siti.resources.ifpe import Reporte111

dict_111 = {
    'identificador_reporte': {
        'inicio_periodo': dt.date(2019, 1, 1),
        'fin_periodo': dt.date(2019, 1, 31),
        'clave_institucion': '065000',
        'reporte': '111',
    },
    'informacion_financiera': [
        {
            'concepto': '100000000000',
            'moneda': '2',
            'dato': 334422.0434,
        },
    ]
}

r111 = Reporte111(**dict_111)

In [1]: r111
Out[1]: 
    Reporte111(
        folio=None,
        identificador_reporte=IdentificadorReporte(
            inicio_periodo=datetime.date(2019, 1, 1),
            fin_periodo=datetime.date(2019, 1, 31),
            clave_institucion='065000',
            reporte='111'
        ),
        informacion_financiera=[
            InformacionFinanciera(
                concepto='100000000000',
                moneda='2',
                dato=334422.0434
            )
        ]
    )
```

Donde r111 será el reporte construido con el modelo, y se realizarán las validaciones propias de ese reporte.


## Desde dataframe
De igual manera se puede construir el objto con la utilización de un dataframe de Pandas con un formato que siga las columnas del modelo que se quiere construir.
Para obtener las columnas del modelo se puede mandar a llamar el método `.columns()`

```python
In [13]: Reporte111.columns()
Out[13]: 
{
    'inicio_periodo': str,
    'fin_periodo': str,
    'clave_institucion': str,
    'reporte': str,
    'concepto': str,
    'moneda': str,
    'dato': float
}
```

Se puede construir un dataframe con esta información y posteriormente mandar a llamar el método .from_dataframe(name, df), dónde name es el nombre del archivo que tiene que cumplir con el formato `CLAVEINSTITUCION_REPORTE_FECHAINICIO_FECHAFINAL` ejemplo: `065014_2610_20210831_20210831` para obtener los datos del campo `identificador_reporte`.

```python
import pandas as pd

name = '065014_2610_20210831_20210831.csv'
columns = Reporte111.columns()
df = pd.read_csv(name, dtype=columns)
r111 = Reporte111.from_dataframe(name, df)

In [1]: r111
Out[1]: 
    Reporte111(
        folio=None,
        identificador_reporte=IdentificadorReporte(
            inicio_periodo=datetime.date(2019, 1, 1),
            fin_periodo=datetime.date(2019, 1, 31),
            clave_institucion='065000',
            reporte='111'
        ),
        informacion_financiera=[
            InformacionFinanciera(
                concepto='100000000000',
                moneda='2',
                dato=334422.0434
            )
        ]
    )
```


## Enviar

Al mandar a llamar cualquiera de los métodos de enviar (`send`, `resend`, `update`), el cliente automáticamente convertirá el objeto al formato solicitado por la CNBV. Este formato se puede obtener llamando el método .dict(to_camel_case=True).


> **Estos métodos regresarán un folio, el cual es importante almacenar para poder realizar el seguimiento del envío**

```python
In [1]: r111.dict(to_camel_case=True)
Out[1]: 
{
    'identificadorReporte': {
        'inicioPeriodo': '20190101',
        'finPeriodo': '20190131',
        'claveInstitucion': '065000',
        'reporte': '111'
    },
    'informacionFinanciera': [
        {
            'concepto': '100000000000',
            'moneda': '2',
            'dato': 334422.0434
        }
    ]
}
```