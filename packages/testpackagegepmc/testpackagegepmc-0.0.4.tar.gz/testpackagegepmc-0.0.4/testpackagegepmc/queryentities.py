import logging
import json
from azure.data.tables import TableServiceClient

def query_entities(table_name, bodega, nud, redsocial, connection_string):
    logging.info(f'query_entity: {table_name} {nud} {bodega}')
    table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
    tables = [table.name for table in table_service_client.list_tables()]

    if table_name not in tables:
        raise Exception("No se encontro la tabla de datos")

    parameters = {}
    query_filter = ""
    productos_response = []
    descripciones_response = []

    try:
        # Obtener cliente de la tabla
        table_client = table_service_client.get_table_client(table_name)
        query_filter = "PartitionKey eq @pk and RowKey eq @rk"
        
        # Los parámetros de la consulta
        parameters["pk"] = str(bodega)  # PartitionKey es la bodega
        parameters["rk"] = str(nud)  # RowKey es el nud 
        
        logging.info(f'query_filter: {query_filter}')
        logging.info(f'parameters: {parameters}')
        
        # Ejecutar la consulta
        rows = list(table_client.query_entities(query_filter=query_filter, parameters=parameters))
        
        # Verificar si hay registros
        if not rows:
            logging.info("No se encontraron registros para la consulta.")
            return None  # Devolvemos None para cacharlo en la funcion que invocamos
        
        for row in rows:
            # Prefijos para descripciones y productos
            prefijos = [
                ['DescripcionesAlcohol', 'DescripcionesSinAlcohol'],
                ['ProductosAlcohol', 'ProductosSinAlcohol']
            ]

            # Arreglos para almacenar los resultados
            descripciones_sin_alcohol = []
            descripciones_con_alcohol = []
            productos_sin_alcohol = []
            productos_con_alcohol = []

            # Iterar sobre los prefijos
            for grupo in prefijos:
                for prefijo in grupo:
                    json_fragment = ""  # Para concatenar los fragmentos de JSON
                    
                    # Buscar la columna base (sin número)
                    key = prefijo  # Ejemplo: "productosSinAlcohol"
                    if key in row and row[key] and row[key].strip():
                        json_fragment += row[key].strip()
                    
                    # Buscar columnas con números (1, 2, 3, etc.)
                    i = 1
                    while True:
                        key = f"{prefijo}{i}"  # Ejemplo: "productosSinAlcohol1"
                        if key not in row or not row[key] or not row[key].strip():
                            break  # Salir del bucle si la columna no existe o está vacía
                        
                        # Concatenar el fragmento de JSON
                        json_fragment += row[key].strip()
                        i += 1  # Pasar a la siguiente columna (ej: productosSinAlcohol2)

                    # Convertir la cadena concatenada en un objeto JSON válido
                    if json_fragment:
                        try:
                            valores = json.loads(json_fragment)
                            if grupo == prefijos[0]:  # Descripciones
                                if prefijo == "DescripcionesSinAlcohol":
                                    descripciones_sin_alcohol.extend(valores)
                                elif prefijo == "DescripcionesAlcohol":
                                    descripciones_con_alcohol.extend(valores)
                            else:  # Productos
                                if prefijo == "ProductosSinAlcohol":
                                    productos_sin_alcohol.extend(valores)
                                elif prefijo == "ProductosAlcohol":
                                    productos_con_alcohol.extend(valores)
                        except json.JSONDecodeError as ex:
                            logging.error(f'Error al decodificar JSON para {prefijo}: {ex}')
                            raise Exception(f"Formato JSON inválido para {prefijo}")

            # Aplicar las reglas de redsocial
            if redsocial == "1":
                # Si redsocial es "1", agregar productos y descripciones con alcohol
                productos_final = productos_sin_alcohol + productos_con_alcohol
                descripciones_final = descripciones_sin_alcohol + descripciones_con_alcohol
            elif redsocial == "2":
                productos_final = productos_sin_alcohol
                descripciones_final = descripciones_sin_alcohol
            else:
                raise Exception("Dato de red social invalido")

            # Construir la respuesta
            response = [productos_final, descripciones_final]

    except Exception as ex:
        logging.error(f'Error al consultar entidades: {ex}')
        raise Exception("No se encontraron datos para la bodega o el nud y/o redsocial o hubo un error en la consulta")

    return response