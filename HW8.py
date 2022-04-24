import matplotlib.pyplot as plt
import os
import numpy as np
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute("SELECT r.name,c.category,b.building, r.rating FROM restaurants r, categories c, buildings b WHERE r.category_id = c.id AND r.building_id = b.id")
    conn.commit()
    lst = [] 
    for t in cur.fetchall():
        dict = {}
        dict['name']=t[0]
        dict['category']=t[1]
        dict['building']=t[2]
        dict['rating']=t[3]
        lst.append(dict)
    
    return lst

def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories along the y-axis and the counts of each category along the
    x-axis.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute("SELECT c.category,COUNT(*) FROM restaurants r, categories c WHERE r.category_id = c.id GROUP BY c.category")
    conn.commit()
    temp = []
    values = []
    dict = {}
    for t in cur.fetchall():
        temp.append(t[0])
        values.append(t[1])
        dict[t[0]] = t[1]

    objects = tuple(temp)
    y_pos = np.arange(len(objects))

    plt.barh(y_pos,values,align='center',alpha=1)
    plt.yticks(y_pos,objects)
    plt.xlabel('Number of Restaurants')
    plt.title('Types of Restaurant on South University Ave')

    plt.show()
    return dict

#EXTRA CREDIT
def highest_rated_building(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each building and returns a tuple containing the
    building number with the highest rated restaurants and the average rating of the restaurants
    in that building. This function should also create a bar chart that displays the buildings along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute("SELECT b.building, AVG(r.rating) AS avg FROM restaurants r, buildings b WHERE r.building_id = b.id GROUP BY b.building ORDER BY avg ")
    conn.commit()
    
    temp = []
    values = []
    for t in cur.fetchall():
        temp.append(t[0])
        values.append(t[1])
    objects = tuple(temp)
    y_pos = np.arange(len(objects))
    aws = (objects[-1],values[-1])
    plt.barh(y_pos,values,align='center',alpha=1)
    plt.yticks(y_pos,objects)
    plt.xlabel('Ratings')
    plt.title('Average Restaurant Ratings by Building')

    plt.show()
    return(aws)

#Try calling your functions here
def main():
    get_restaurant_data('South_U_Restaurants.db')
    barchart_restaurant_categories('South_U_Restaurants.db')
    highest_rated_building('South_U_Restaurants.db')

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_building = ((1335, 4.8), ('1335', 4.8))

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_building(self):
        best_building = highest_rated_building('South_U_Restaurants.db')
        self.assertIsInstance(best_building, tuple)
        self.assertIn(best_building, self.best_building)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)