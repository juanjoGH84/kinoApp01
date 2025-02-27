from pymongo import MongoClient, errors
###RECUERDA QUE PYTHON ES UN LENGUAJE INTERPRETADO####
# Conectar a la base de datos de origen y destino
#cliente_origen = MongoClient("mongodb://52.15.210.68:27017/")
#cliente_destino = MongoClient("mongodb://localhost:27017/")  #
# Conectar a la base de datos de origen y destino con autenticación
usr= "adminK"
pwd = "KinoA01"
usr_origin = "kinoDev"
pwd_origin = "kinokea01"

try: 
    trgt_db = MongoClient(f"mongodb://{usr}:{pwd}@localhost:27017/KinoDev?authSource=admin")  #
    trgt_db.server_info()
    print("Conexión exitosa a la base de datos de destino.")
except errors.ServerSelectionTimeoutError:
    print("Error: No se pudo conectar a la base de datos de destino.")
    exit()
except errors.OperationFailure as e:
    print(f"Error de autenticación con la base de datos de destino: {e}")
    exit()
try:
    trgt_origin = MongoClient(f"mongodb://{usr_origin}:{pwd_origin}@52.15.210.68:27017/users?authSource=admin")
    trgt_origin.server_info()
    print("Conexión exitosa a la base de datos de origen.")
except errors.ServerSelectionTimeoutError:
    print("Error: No se pudo conectar a la base de datos de origen.")
    exit()
except errors.OperationFailure as e:
    print(f"Error de autenticación con la base de datos de origen: {e}")
    exit()

# Nombres de la base de datos de origen y destino
db_origin = "users"
db_dev = "KinoDev"

# Obtener la base de datos de origen y destino
db_source = trgt_origin[db_origin]
db_finaldev = trgt_db[db_dev]

# Obtener todas las colecciones de la base de datos de origen
collections = db_source.list_collection_names()

# Copiar la estructura y los datos de cada colección
for collection in collections:
    # Obtener todos los documentos de la colección
    documents =  list(db_source[collection].find())

    # Insertar todos los registros (documentos) en la colección de destino
    if len(documents) > 0:
        db_finaldev[collection].insert_many(documents)
    #   Esta línea se elimina para poder copiar la BD a la parte local
    #    db_dev[collection].delete_many({})
    #    db_dev[collection].drop()
print(f"Estructura y datos de la base de datos '{db_origin}' copiados a '{db_dev}'.")
