# final_project.py
# Aarsh Shah ENDG 233 F21
# A terminal-based application to process and plot data based on given user input and data csv files.


# imports numpy and matplotlib libraries.
import numpy as np
import matplotlib.pyplot as plt


def data():
    # Creates a numpy array from the population data and stores it in a variable.
    population_data = np.genfromtxt(
        'Population_Data.csv', delimiter=',', skip_header=True)

    # Creates a numpy array from the species data and stores it in a variable.
    species_data = np.genfromtxt(
        'Threatened_Species.csv', delimiter=',', skip_header=True)

    # Creates a numpy array from the country data and stores it in a variable.
    country_data = np.genfromtxt(
        'Country_Data.csv', delimiter=',', skip_header=True)

    # Creates empty list that will store all the chosen school's enrollment data.
    data = []
    # Creates a list that stores the arrays of all the school data.
    list_data = [population_data, species_data, country_data]
    # Creates a while loop that runs until the code runs 3 times (for each grade).
    iteration = 1
    while iteration <= 3:
        # Create a for loop that will run for all 3 years of data.
        for year in range(0, 3):
            # Finds the position of the chosen school code in the given years array.
            position = np.where(list_data[year] == int(None))
            # Reassigns the position from tuple format to individual x y coordinates.
            (x, y) = (position[0], position[1])
            # Stores the enrollment data for given school, year, and grade.
            enrollment = list_data[year][x, y + iteration]
            # Adds the enrollment data to the data list
            data.append(enrollment)
        # Tracks how many times the while loop has run.
        iteration += 1
