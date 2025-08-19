import select
from flask import Flask, request,jsonify,Blueprint
from models import db, User, Personaje, Planeta

api=Blueprint("api",__name__)

# Rutas Personajes

@api.route("/personajes", methods=["GET"])
def get_personajes():
    personajes = Personaje.query.all()
    return jsonify([personaje.serialize() for personaje in personajes]), 200

@api.route("/personaje/<int:personaje_id>", methods=["GET"])
def get_personajes(personaje_id):
    personaje = Personaje.query.get(personaje_id)
    if  not personaje:
        return jsonify({"msg": "Character not found"}), 404
    return jsonify(personaje.serialize()), 200



# Rutas  Planetas

@api.route("/planetas", methods=["GET"])
def get_planetas():
    planetas = Planeta.query.all()
    return jsonify  ([planeta.serialize() for planeta in planetas]), 200

@api.route("/planetas/<int:planeta_id>", methods=["GET"])
def get_planetas(planeta_id):
    planetas = Planeta.query.get(planeta_id)
    if not planetas:
        return jsonify({"msg":"Planet not found"}), 404
    return jsonify(planetas.serialize()), 200  



# rutas de usuario

@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200



@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user= User.query.get(user_id)
    if not user:
        return jsonify({"msg":"User not found"}), 404
    return jsonify(user.serialize()), 200  


@api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("email") or not data.get("password") or not data.get("user_name"):
        return jsonify({"msg":"Email and Password are required"}), 400
    

    existing_user = db.session.execute(select(User).where(User.email == data.get("email"))).scalar_one_or_none()

    if not existing_user is None:
        return jsonify ({"msg": " this user is alredy axisting"}), 400
    new_user = User(             # creando un objeto
        email =data.get("email"),
        password =data.get("password"),
        user_name =data.get("user_name")

    ) 
    #guardo lo que cree en un modelo
    db.session.add(new_user)
    db.session.commit()
    return jsonify ({ new_user.serialize()}), 201


#favoritos

@api.route("<int:user_id>/favorite/<int:personaje_id>", methods=["POST"])
def create_fav_personaje(user_id, personaje_id):
    personaje = db.session.get(Personaje,personaje_id)
    user = db.session.get(User,user_id) # solo cuando vamos a hacer cambios

    if not personaje or not user:
        return jsonify ({"msg": "User or Character not found"}), 400
    
    if personaje in user.fav_personajes:
        return jsonify({ "msg": "Character alredy in favorites"}), 400
    
    user.fav_personajes.append(personaje)

    # para guardar los cambios de sesión
    db.session.commit()
    return jsonify(user.serialize()), 200


@api.route("/favorites/<int:user_id>/planets/<int:planet_id>", methods=["POST"])
def create_fav_planets(user_id, planet_id):
    planet = db.session.get(Planeta, planet_id)
    user = db.session.get(User,user_id) 

    if not planet or not user:
        return jsonify ({"msg": "User or planet not found"}), 400
    
    if planet in user.fav_planetas:
        return jsonify({ "msg": "Planet alredy in favorites"}), 400
    
    user.fav_planetas.append(planet)

    
    db.session.commit()
    return jsonify(user.serialize()), 200


# para eliminar favoritos

@api.route("<int:user_id>/favorite/<int:personaje_id>", methods=["DELETE"])
def delete_fav_personajes(user_id, personaje_id):
    personaje = db.session.get(Personaje, personaje_id)
    user = db.session.get(User,user_id) # solo cuando vamos a hacer cambios

    if not personaje or not user:
        return jsonify ({"msg": "User or character not found"}), 400
    
    if  personaje in user.fav_planetas:
       user.fav_planetas.remove(personaje)

    
    db.session.commit()
    return jsonify(user.serialize()), 200

@api.route("/favorites/<int:user_id>/planets/<int:planet_id>", methods=["DELETE"])
def delete_fav_planets(user_id, planet_id):
    planet = db.session.get(Planeta,planet_id)
    user = db.session.get(User,user_id) 

    if not planet or not user:
        return jsonify ({"msg": "User or planet not found"}), 400
    
    if  planet in user.fav_planetas:
        user.fav_planetas.remove(planet)

    
    db.session.commit()
    return jsonify(user.serialize()), 200

# solo favoritos de un usuario
@api.route("/favorites/<int:user_id>/", methods=["GET"])
def get_favorites (user_id):
    user = db.session.get(User,user_id) 
    if not user:
        return jsonify ({"msg":"user not found"})
    
    favorites = [Personaje.serialize() for Personaje in user.favorites]
    return jsonify(favorites), 200

    
