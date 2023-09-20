#!/usr/bin/env python3

from config import app, db, api, Resource, bcrypt, request, session
import json

# Import models here!!!
from models import db, User, Recipe, Ingredient, RecipeIngredient, Allergy, UserRecipe

# Routes!!!
class Recipes ( Resource ) :
    def get ( self ) :
        recipes = [ recipe.to_dict() for recipe in Recipe.query.all() ]
        return recipes, 200
    
api.add_resource( Recipes, '/recipes', endpoint = 'recipes' )

class RecipeById ( Resource ) :
    def get ( self, id ) :
        recipe = Recipe.query.filter_by( id = id ).first()
        if recipe :
            return recipe.to_dict_with_ingredients(), 200
        
api.add_resource( RecipeById, '/recipes/<int:id>', endpoint = 'recipe' )

class Ingredients ( Resource ) :
    def get ( self ) :
        ingredients = [ ingredient.to_dict() for ingredient in Ingredient.query.all() ]
        return ingredients, 200
    
api.add_resource( Ingredients, '/ingredients', endpoint = 'ingredients' )

class IngredientById ( Resource ) :
    def get ( self, id ) :
        ingredient = Ingredient.query.filter_by( id = id ).first()
        return ingredient.to_dict(), 200
    
api.add_resource( IngredientById, '/ingredients/<int:id>', endpoint = 'ingredient' )

class Login ( Resource ) :
    def post ( self ) :
        email = request.get_json()[ 'email' ]
        password = request.get_json()[ 'password' ]
        
        user = User.query.filter( User.email.like( f"%{ email }%" ) ).first()
        if user and user.authenticate( password ) :
                session[ 'user_id' ] = user.id
                print( session['user_id'] )
                return user.to_dict(), 200
        else :
            return { 'errors': ["Invalid email and/or password. Please try again."] }, 401

api.add_resource( Login, '/login', endpoint = 'login' )

class Logout ( Resource ) :
    def delete ( self ) :
        session[ 'user_id' ] = None
        return {}, 204
    
api.add_resource( Logout, '/logout', endpoint = 'logout' )

class AutoLogin ( Resource ) :
    def get ( self, id ) :
        user = User.query.filter_by( id = id ).first()
        if user :
            return user.to_dict(), 200
        else :
            return '', 204

api.add_resource( AutoLogin, '/autologin/<int:id>', endpoint = 'autologin' )


if __name__ == '__main__':
    app.run( port=3000, debug=True )
