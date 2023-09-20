#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker
from app import app

# Don't forget to import models here too!!!
from models import db, User, Recipe, Ingredient, RecipeIngredient, Allergy, UserRecipe

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding... 🌱")

        print( 'Wiping tables...' )
        # Clear all the tables!
        User.query.delete()
        Recipe.query.delete()
        Ingredient.query.delete()
        RecipeIngredient.query.delete()
        Allergy.query.delete()
        UserRecipe.query.delete()
        print( 'Database wiped!' )


        # print( 'Creating ______ ...' )

        # print( '_________ created!' )

        print( 'Creating users... 🕴️' )
        u1 = User(
            username = 'Princeton',
            email = 'princeton@gmail.com',
            password_hash = 'password'
        )
        u2 = User(
            username = 'Thomas',
            email = 'thomas@gmail.com',
            password_hash = 'password'
        )
        users = [ u1, u2 ]
        db.session.add_all( users )
        db.session.commit()
        print( 'Users created! 🥂' )

        print( 'Creating ingredients to cook with... 🌽' )
        i1 = Ingredient(
            name = 'Corn'
        )
        i2 = Ingredient(
            name = 'Bread'
        )
        i3 = Ingredient(
            name = 'Rice'
        )
        i4 = Ingredient(
            name = 'Chicken'
        )
        i5 = Ingredient(
            name = 'Salt'
        )
        i6 = Ingredient(
            name = 'Pepper'
        )
        i7 = Ingredient(
            name = 'Beans'
        )
        i8 = Ingredient(
            name = 'Potatoes'
        )
        i9 = Ingredient(
            name = 'Eggs'
        )
        i10 = Ingredient(
            name = 'Peanuts'
        )
        i11 = Ingredient(
            name = 'Noodles'
        )
        i12 = Ingredient(
            name = 'Cheese'
        )
        i13 = Ingredient(
            name = 'Butter'
        )
        ingredients = [ i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13 ]
        db.session.add_all( ingredients )
        db.session.commit()
        print( 'Ingredients added to the pantry. 🧑‍🍳' )

        print( 'Creating recipes to cook... 🔪' )
        r1 = Recipe(
            name = 'Chicken Soup'
        )
        r2 = Recipe(
            name = 'Jerk Chicken'
        )
        r3 = Recipe(
            name = 'Cornbread'
        )
        r4 = Recipe(
            name = 'Mashed Potatoes'
        )
        recipes = [ r1, r2, r3, r4 ]
        db.session.add_all( recipes )
        db.session.commit()
        print( 'Recipes created! 🍽️' )

        print( 'Tying ingredients to recipes... 🪢' )
        ri1 = RecipeIngredient(
            recipe_id = r1.id,
            ingredient_id = i4.id,
            amount = '1/2 lb.',
        )
        ri2 = RecipeIngredient(
            recipe_id = r1.id,
            ingredient_id = i11.id,
            amount = '1 pack',
        )
        ri3 = RecipeIngredient(
            recipe_id = r2.id,
            ingredient_id = r4.id,
            amount = '1 lb.',
        )
        ri4 = RecipeIngredient(
            recipe_id = r2.id,
            ingredient_id = i6.id,
            amount = '1/4 teaspoon',
        )
        ri5 = RecipeIngredient(
            recipe_id = r2.id,
            ingredient_id = i3.id,
            amount = '1/4 lb.',
        )
        ri6 = RecipeIngredient(
            recipe_id = r3.id,
            ingredient_id = i1.id,
            amount = '3/4 lb.',
        )
        ri7 = RecipeIngredient(
            recipe_id = r3.id,
            ingredient_id = i2.id,
            amount = '5 slices',
        )
        ri8 = RecipeIngredient(
            recipe_id = r4.id,
            ingredient_id = i13.id,
            amount = '1/4 stick',
        )
        ri9 = RecipeIngredient(
            recipe_id = r4.id,
            ingredient_id = i8.id,
            amount = '1 1/2 lbs.',
        )
        ri10 = RecipeIngredient(
            recipe_id = r4.id,
            ingredient_id = i5.id,
            amount = 'A pinch',
        )
        recipe_ingredients = [ ri1, ri2, ri3, ri4, ri5, ri6, ri7, ri8, ri9, ri10 ]
        db.session.add_all( recipe_ingredients )
        db.session.commit()
        print( 'Time to start cooking! 👩‍🍳' )

        print( "Users are getting ready to cook... 🍳" )
        ur1 = UserRecipe(
            user_id = u1.id,
            recipe_id = r2.id
        )
        ur2 = UserRecipe(
            user_id = u1.id,
            recipe_id = r3.id
        )
        ur3 = UserRecipe(
            user_id = u2.id,
            recipe_id = r1.id
        )
        ur4 = UserRecipe(
            user_id = u2.id,
            recipe_id = r4.id
        )
        user_recipes = [ ur1, ur2, ur3, ur4 ]
        db.session.add_all( user_recipes )
        db.session.commit()
        print( "Users have finished their main courses! 🍽️" )

        print( "Checking for allergies... 🤧" )
        a1 = Allergy(
            user_id = u2.id,
            ingredient_id = i10.id
        )
        a2 = Allergy(
            user_id = u2.id,
            ingredient_id = i1.id
        )
        allergies = [ a1, a2 ]
        db.session.add_all( allergies )
        db.session.commit()
        print( "Allergies found. Watch what you eat! 🤤" )

        print( "Seeding all done!!! 🌴" )
