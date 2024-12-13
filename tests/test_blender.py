from unittest.mock import patch
from lib.blender import Blender, FoodGeniusAPI, Smoothie
from datetime import datetime

def test_add_ingredients():
    blender = Blender()
    blender.add_ingredients([
        "oats",
        "protein powder",
        "banana"
    ])
    assert blender.ingredients == [
        "oats",
        "protein powder",
        "banana"
    ]
    
@patch.object(FoodGeniusAPI, 'suggest_complementary_ingredients')
def test_suggest_and_add_complementary_ingredients(mock_complementary_ingredients):
    mock_complementary_ingredients.return_value = [
        "honey",
        "peanut butter"
    ]
    
    blender = Blender()
    blender.add_ingredients([
        "oats",
        "protein powder",
        "banana"
    ])
    blender.suggest_and_add_complementary_ingredients()
    assert blender.ingredients == [
        "oats",
        "protein powder",
        "banana",
        "honey",
        "peanut butter"
    ]

@patch.object(FoodGeniusAPI, 'get_macros')
@patch('lib.blender.datetime')
def test_blend_ingredients(mock_datetime, mock_get_macros):
    mock_get_macros.return_value = {
        "protein": 35,
        "carbs": 50,
        "fat": 20,
    }
    mock_date = datetime(2022, 12, 25)
    mock_datetime.today.return_value = mock_date
    mock_datetime.strftime = datetime.strftime
    blender = Blender()
    blender.add_ingredients([
        "oats",
        "protein powder",
        "banana"
    ])
    smoothie = blender.blend_ingredients()
    
    assert isinstance(smoothie, Smoothie)
    assert smoothie.macros == {
        "protein": 35,
        "carbs": 50,
        "fat": 20,
    }
    assert smoothie.create_date == '25/12/2022'








# @patch.object(FoodGeniusAPI, 'suggest_complementary_ingredients') 
# def test_add_ingredients(mock_complementary_ingredients):
#     mock_complementary_ingredients.return_value = ["Oat Milk", "Vanilla Extract", "Apple"]
    
#     blender = Blender()
    
#     blender.add_ingredients(
#         [
#             "Oats",
#             "Protein powder",
#             "Seeds mix",
#         ]
#     )

#     blender.suggest_and_add_complementary_ingredients()
    
#     assert blender.ingredients == [
#         "Oats", 
#         "Protein powder",
#         "Seeds mix",
#         "Oat Milk", 
#         "Vanilla Extract",
#         "Apple"
#     ]

# @patch.object(FoodGeniusAPI, 'get_macros') 
# @patch('lib.blender.datetime')
# def test_blend_ingredients(mock_datetime, mock_get_macros):
#     mock_get_macros.return_value = {
#         "protein": 25,
#         "carbs": 60,
#         "fat": 10,
#     }
#     mock_date = datetime(2022, 12, 25)
#     mock_datetime.today.return_value = mock_date
#     mock_datetime.strftime = datetime.strftime

#     blender = Blender()
#     blender.add_ingredients(
#         [
#             "Oats",
#             "Protein powder",
#             "Seeds mix",
#         ]
#     )
#     smoothie = blender.blend_ingredients()
    
#     assert isinstance(smoothie, Smoothie)
#     assert smoothie.macros == {
#         "protein": 25,
#         "carbs": 60,
#         "fat": 10,
#     }
#     assert smoothie.create_date == '2022-12-25'