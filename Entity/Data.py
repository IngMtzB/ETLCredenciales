import pickle
import datetime

#Clase para definir 
class Data():
    def __init__(self,numeroEmpleado, credenciales,fecha):
        self.numeroEmpleado = numeroEmpleado
        self.credenciales = credenciales
        self.fecha = fecha
 
def save_object(obj,numeroEmpleado):
    try:
        with open(f"{numeroEmpleado}.pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)

def load_object(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)

userCredentialsExpireData = {} 
userCredentialsExpireData.update({"tiendavirtual":
                                            {"usename":"90311467","valuntil":"2024-01-01","daysleft":"30"}
                                            }) 
userCredentialsExpireData.update({"tienda800":
                                            {"usename":"90311467","valuntil":"2024-01-01","daysleft":"5"}
                                            })      
today = datetime.date.today()
numeroEmpleado = "90311467"
obj = Data(numeroEmpleado,userCredentialsExpireData,today)
save_object(obj,numeroEmpleado)

obj = load_object(f"{numeroEmpleado}.pickle")
print(isinstance(obj, Data))
print(obj.numeroEmpleado)
print(obj.credenciales)
print(obj.fecha)


