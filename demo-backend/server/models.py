# Imports for models
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

from config import db, bcrypt

# Models go here!
class User ( db.Model ) :
    __tablename__ = 'users'

    id = db.Column( db.Integer, primary_key = True )
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )

    email = db.Column( db.String, nullable = False, unique = True )
    _password_hash = db.Column( db.String, nullable = False )
    username = db.Column( db.String, unique = True )

    user_recipes = db.relationship( 'UserRecipe', backref = 'user' )
    recipes = association_proxy( 'user_recipes', 'recipe' )

    allergies = db.relationship( 'Allergy', backref = 'user' )
    allergic_to = association_proxy( 'allergies', 'ingredient' )

    def __repr__ ( self ) :
        return f"{{ User { self.id } }}"
    
    def to_dict ( self ) :
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username
        }

    validation_errors = []

    def get_validation_errors ( self ) :
        return list( set( self.validation_errors ) )
    
    @classmethod
    def clear_validation_errors ( cls ) :
        cls.validation_errors = []

    @validates( 'email' )
    def validate_email( self, key, email ) :
        if type( email ) is str and email and '@' in email and '.' in email :
            return email
        else : 
            self.validation_errors.append( "Email must be a string in valid email format with a '@' and a '.'" )

    @validates( 'username' )
    def validate_username( self, key, username ) :
        if username :
            if type( username ) is str and len( username ) in range( 3, 17 ) :
                return username
            else :
                self.validation_errors.append( "Username must be a string between 3 to 16 characters long." )

# Password stuff for user model!
    @hybrid_property
    def password_hash ( self ) :
        return self._password_hash
    
    @password_hash.setter
    def password_hash ( self, password ) :
        if type( password ) is str and len( password ) in range( 6, 17 ) :
            password_hash = bcrypt.generate_password_hash( password.encode( 'utf-8' ) )
            self._password_hash = password_hash.decode( 'utf-8' )
        else :
            self.validation_errors.append( "Password validation error goes here!" )

    def authenticate ( self, password ) :
        return bcrypt.check_password_hash( self._password_hash, password.encode( 'utf-8' ) )
    

class Recipe ( db.Model ) :
    __tablename__ = 'recipes'

    id = db.Column( db.Integer, primary_key = True )
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )

    name = db.Column( db.String, nullable = False )

    recipe_ingredients = db.relationship( 'RecipeIngredient', backref = 'recipe' )
    ingredients = association_proxy( 'recipe_ingredients', 'ingredient' )

    user_recipes = db.relationship( 'UserRecipe', backref = 'recipe' )
    users = association_proxy( 'user_recipes', 'user' )

    def to_dict( self ) :
        return {
            'id': self.id,
            'name': self.name
        }
    
    def to_dict_with_ingredients ( self ) :
        recipe = self.to_dict()
        recipe[ 'ingredients' ] = [ ingredient.to_dict() for ingredient in self.ingredients ]
        return recipe

    def __repr__ ( self ) :
        return f"{{ Recipe { self.id }, Name: { self.name } }}"

    validation_errors = []

    def get_validation_errors ( self ) :
        return list( set( self.validation_errors ) )
    
    @classmethod
    def clear_validation_errors ( cls ) :
        cls.validation_errors = []

    @validates( 'name' )
    def validate_name( self, key, name ) :
        if type( name ) is str and name :
            return name
        else :
            self.validation_errors.append( "Recipe must have a name with more than 0 characters." )


class Ingredient ( db.Model ) :
    __tablename__ = 'ingredients'

    id = db.Column( db.Integer, primary_key = True )
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )

    name = db.Column( db.String, nullable = False )
    calories = db.Column( db.Integer )

    recipe_ingredients = db.relationship( 'RecipeIngredient', backref = 'ingredient' )
    recipes = association_proxy( 'recipe_ingredients', 'recipe' )

    allergies = db.relationship( 'Allergy', backref = 'ingredient' )
    users = association_proxy( 'allergies', 'user' )

    def to_dict( self ) :
        return {
            'id': self.id,
            'name': self.name,
            'calories': self.calories
        }

    def __repr__ ( self ) :
        return f"{{ Ingredient { self.id }, Name: { self.name }, Calories: { self.calories if self.calories else 'Unknown' } }}"

    validation_errors = []

    def get_validation_errors ( self ) :
        return list( set( self.validation_errors ) )
    
    @classmethod
    def clear_validation_errors ( cls ) :
        cls.validation_errors = []

    @validates( 'name' )
    def validate_name( self, key, name ) :
        if type( name ) is str and name :
            return name
        else :
            self.validation_errors.append( "Ingredient must have a name with more than 0 characters." )

    @validates( 'calories' )
    def validate_calories( self, key, calories ) :
        if calories :
            if type( calories ) is int and calories >= 0 :
                return calories
            else :
                self.validation_errors.append( "Calories must be a number greater than or equal to 0." )


class RecipeIngredient ( db.Model ) :
    __tablename__ = 'recipe_ingredients'

    id = db.Column( db.Integer, primary_key = True )
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )

    amount = db.Column( db.String, nullable = False )

    recipe_id = db.Column( db.Integer, db.ForeignKey( 'recipes.id' ) )
    ingredient_id = db.Column( db.Integer, db.ForeignKey( 'ingredients.id' ) )

    def to_dict( self ) :
        return {
            'id': self.id,
            'amount': self.amount,
            'recipe': self.recipe.name,
            'ingredient': self.ingredient.name
        }

    def __repr__ ( self ) :
        return f"{{ RecipeIngredient { self.id }, Recipe: { self.recipe.name }, Ingredient: { self.ingredient.name }, Amount: { self.amount } }}"

    validation_errors = []

    def get_validation_errors ( self ) :
        return list( set( self.validation_errors ) )
    
    @classmethod
    def clear_validation_errors ( cls ) :
        cls.validation_errors = []

    @validates( 'amount' )
    def validate_amount( self, key, amount ) :
        if type( amount ) is str and amount :
            return amount
        else :
            self.validation_errors.append( "Amount must be a string greater than 0 characters." )

    @validates( 'recipe_id' )
    def validate_recipe( self, key, rid ) :
        if Recipe.query.filter_by( id = rid ).first() :
            return rid
        else :
            self.validation_errors.append( 'Recipe not found.' )
    
    @validates( 'ingredient_id' )
    def validate_ingredient( self, key, iid ) :
        if Ingredient.query.filter_by( id = iid ).first() :
            return iid
        else :
            self.validation_errors.append( 'Ingredient not found.' )


class Allergy ( db.Model ) :
    __tablename__ = 'allergies'

    id = db.Column( db.Integer, primary_key = True )
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )

    user_id = db.Column( db.Integer, db.ForeignKey( 'users.id' ) )
    ingredient_id = db.Column( db.Integer, db.ForeignKey( 'ingredients.id' ) )

    def __repr__ ( self ) :
        return f"{{ Allergic to { self.ingredient.name } }}"

    validation_errors = []

    def get_validation_errors ( self ) :
        return list( set( self.validation_errors ) )
    
    @classmethod
    def clear_validation_errors ( cls ) :
        cls.validation_errors = []

    @validates( 'user_id' )
    def validate_user( self, key, uid ) :
        if User.query.filter_by( id = uid ).first() :
            return uid
        else :
            self.validation_errors.append( 'User not found.' )
    
    @validates( 'ingredient_id' )
    def validate_ingredient( self, key, iid ) :
        if Ingredient.query.filter_by( id = iid ).first() :
            return iid
        else :
            self.validation_errors.append( 'Ingredient not found.' )


class UserRecipe ( db.Model ) :
    __tablename__ = 'user_recipes'

    id = db.Column( db.Integer, primary_key = True )
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )

    user_id = db.Column( db.Integer, db.ForeignKey( 'users.id' ) )
    recipe_id = db.Column( db.Integer, db.ForeignKey( 'recipes.id' ) )

    def __repr__ ( self ) :
        return f"{{ UserRecipe { self.id }, User: { self.user.username if self.user.username else self.user.id }, Recipe: { self.recipe.name } }}"

    validation_errors = []

    def get_validation_errors ( self ) :
        return list( set( self.validation_errors ) )
    
    @classmethod
    def clear_validation_errors ( cls ) :
        cls.validation_errors = []

    @validates( 'user_id' )
    def validate_user( self, key, uid ) :
        if User.query.filter_by( id = uid ).first() :
            return uid
        else :
            self.validation_errors.append( 'User not found.' )

    @validates( 'recipe_id' )
    def validate_recipe( self, key, rid ) :
        if Recipe.query.filter_by( id = rid ).first() :
            return rid
        else :
            self.validation_errors.append( 'Recipe not found.' )


# Model template!
# class NameOfClass ( db.Model ) :
#     __tablename__ = 'name of class plural'

#     id = db.Column( db.Integer, primary_key = True )
#     created_at = db.Column( db.DateTime, server_default = db.func.now() )
#     updated_at = db.Column( db.DateTime, onupdate = db.func.now() )

#     table_column_id = db.Column( db.Integer, db.ForeignKey( 'table.id' ) )

#     def __repr__ ( self ) :
#         return f"{{ ModelName { self.id } }}"

#     validation_errors = []

#     def get_validation_errors ( self ) :
#         return list( set( self.validation_errors ) )
    
#     @classmethod
#     def clear_validation_errors ( cls ) :
#         cls.validation_errors = []


