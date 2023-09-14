import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Union
from pydantic import BaseModel

app = FastAPI()

# Crear una nueva API, la cuál contenga cuatro endpoints con
# las siguientes consideraciones:
#
# Un endpoint para crear un diccionario en donde las llaves
# de dicho diccionario sea un id de tipo entero como
# identificador único para una lista de usuarios. El valor
# de dicha llave será otro diccionario con la siguiente
# estructura:
#
#     {"user_name": "name",
#     "user_id": id,
#     "user_email": "email",
#     "age" (optional): age,
#     "recommendations": list[str],
#     "ZIP" (optional): ZIP
#     }


class User(BaseModel):
    user_name: str
    user_email: str
    age: Union[int, None] = None
    recommendations: list[str]
    ZIP: Union[int, None] = None


class UserPost(User):
    user_id: int

# Cada vez que se haga un request a este endpoint, se debe
# actualizar el diccionario. Hint: Definir un diccionario
# vacío fuera del endpoint. La respuesta de este endpoint
# debe enviar el id del usuario creado y una descripción de
# usuario creado exitosamente.
#
# Si se envía datos con un id ya repetido, se debe regresar
# un mensaje de error que mencione este hecho.


users = dict()


@app.post("/user")
async def create_user(user: UserPost):
    user = user.dict()
    user_id = user.get('user_id')

    if user_id in users:
        raise HTTPException(
            status_code=400,
            detail="The user with that user_id already exists."
        )

    users[user_id] = user

    return {
        "user_id": user_id,
        "detail": "User was created successfully."
    }


# Un endpoint para actualizar la información de un usuario
# específico buscándolo por id. Si el id no existe, debe
# regresar un mensaje de error que mencione este hecho.


@app.put("/user/{user_id}")
async def update_user(user_id: int, user: User):
    user = user.dict()

    if user_id not in users:
        raise HTTPException(
            status_code=400,
            detail="The user with that user_id does not exist."
        )
    user['user_id'] = user_id
    users[user_id] = user

    return {
        "user_id": user_id,
        "detail": "User was updated successfully."
    }


# Un endpoint para obtener la información de un usuario
# específico buscándolo por id. Si el id no existe, debe
# regresar un mensaje de error que mencione este hecho.


@app.get("/user/{user_id}")
async def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(
            status_code=400,
            detail="The user with that user_id does not exist."
        )

    return {
        "user": users[user_id]
    }


# Un endpoint para eliminar la información de un usuario
# específico buscándolo por id. Si el id no existe, debe
# regresar un mensaje de error que mencione este hecho.


@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(
            status_code=400,
            detail="The user with that user_id does not exist."
        )
    users.pop(user_id)
    return {
        "detail": f"User with user_id = {user_id} was deleted successfully."
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=False)

