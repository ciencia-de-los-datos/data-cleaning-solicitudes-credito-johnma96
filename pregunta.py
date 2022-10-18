"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""
import pandas as pd

from typing   import Union
from datetime import datetime


def clean_data():
    data = pd.read_csv('solicitudes_credito.csv', sep=';', 
                        index_col='Unnamed: 0', encoding='utf8')
    data_clean = data.copy()
    data_clean.dropna(axis=0, how='any', inplace=True)

    def edit_idea_negocio(val:str) -> Union[str, float]:
        """
        Clean string value.

        Input:
            - val: String. String to clean

        Return:
            - val: Clean string
        """

        val = val.replace('-', ' ')
        val = val.replace('_', ' ')
        val = val.strip()  

        return val

    # Remove special characters from numbers
    data_clean.monto_del_credito = (data_clean.monto_del_credito
                                    .str.replace('[^\d.]+', '', regex=True))
    
    # Convert dates to single format
    data_clean.fecha_de_beneficio = (
                                pd.to_datetime(data_clean.fecha_de_beneficio, 
                                            format='%d/%m/%Y', errors='coerce')
                                .fillna(pd.to_datetime(
                                    data_clean.fecha_de_beneficio, 
                                    format='%Y/%m/%d', errors='coerce')))

    # Verify that columns can be converted to appropriate types
    types = {
        'sexo': 'category',
        'tipo_de_emprendimiento': 'category',
        'idea_negocio': str,
        'barrio': str,
        'estrato': int,
        'comuna_ciudadano': int,
        'fecha_de_beneficio': str,
        'monto_del_credito': float,
        'línea_credito': str
    }

    data_clean = data_clean.astype(types)
    data_clean.fecha_de_beneficio = pd.to_datetime(data_clean.fecha_de_beneficio)

    # All categorical columns or str in lowercase
    data_clean.sexo = data_clean.sexo.str.lower()
    data_clean.tipo_de_emprendimiento = data_clean.tipo_de_emprendimiento.str.lower()
    data_clean.idea_negocio = data_clean.idea_negocio.str.lower()
    data_clean.barrio = data_clean.barrio.str.lower()
    data_clean.línea_credito = data_clean.línea_credito.str.lower()

    # Cleaning categorical columns-str. special case with 'barrio'
    data_clean.idea_negocio = data_clean.idea_negocio.transform(
                                                lambda x: edit_idea_negocio(x))
    data_clean.tipo_de_emprendimiento = (data_clean.tipo_de_emprendimiento
                                    .transform(lambda x: edit_idea_negocio(x)))
    data_clean.línea_credito = data_clean.línea_credito.transform(
                                                lambda x: edit_idea_negocio(x))
    
    data_clean.barrio = data_clean.barrio.str.replace('-',' ')
    data_clean.barrio = data_clean.barrio.str.replace(' ','_')
    data_clean.barrio = data_clean.barrio.str.lower()

    # Removing duplicates
    data_clean.drop_duplicates(inplace=True, keep='last')

    return data_clean