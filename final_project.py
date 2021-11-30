# final_project.py
# Aarsh Shah ENDG 233 F21
# A terminal-based application to process and compute data based on given user input and data csv files.

# imports numpy and matplotlib libraries.
import numpy as np
import matplotlib.pyplot as plt


class dataClass():
    def __init__(self, data, type, place, data_set_needed, data_set1, data_set2, data_set3):
        self.data = data
        self.type = type
        self.place = place
        self.data1 = data_set1
        self.data2 = data_set2
        self.data3 = data_set3
        self.list_data = [self.data1, self.data2, self.data3]
        self.set = data_set_needed

    # def position(self):
        # iteration = 1
        # while iteration <= 3:
        #     for set in range(0, 3):
        #         position = np.where(self.list_data[self.set] == self.place)
        #         (x, y) = (position[0], position[1])
        #         self.data = self.list_data[set][x, y + iteration]

        #     iteration += 1

    def country_computation(self):
        if self.type == 1:
            pass
        elif self.type == 2:
            pass

    def species_threathened_region(self):
        iteration = 1
        while iteration <= 3:
            for set in range(0, 3):
                position = np.where(self.list_data[self.set] == self.place)
                (x, y) = (position[0], position[1])
                self.data = self.list_data[set][x, y + iteration]

            iteration += 1


def user_input(data_set3):
    valid = True
    while valid:
        # Asks the user to input the place for which they want data on.
        requested_place = str(input(
            'Please enter a country name or region: ')).capitalize()
        if requested_place in data_set3:
            if requested_place in data_set3[:, 0]:
                print('You have chosen a country')
                type = 'country'
                valid = False
            if requested_place in data_set3[:, 1]:
                print('You have chosen a region')
                type = 'region'
                valid = False
        else:
            # If the user doesn't choose a valid place they are prompted to try again.
            print('You must enter a valid country or region.')

    valid2 = True
    while valid2 == True:
        if type == 'country':
            requested_data = int(input(
                f'''What data would you like on {requested_place}
Year with the highest population - Including population trend (Enter: 11)
Year with the lowest population - Including population trend (Enter: 12)
                '''))
            if requested_data in range(1, 3):
                valid2 = False

        if type == 'region':
            requested_data = input(
                f'''What data would you like on {requested_place}\n 
                Total number of Plants, Fish, Birds, and Mammals threatened in the region (Enter: 21)
                Total number of square km in the region (Enter: 21)
                ''')
            if requested_data in range(1, 3):
                valid2 = False
        else:
            print('Invalid data request please try again')

    return requested_data, requested_place, type


def data_plotting():
    # Pheonix implement
    pass


def main():
    # Creates a numpy array from the population, species, and country data and stores it in a its respective variable.
    population_data = np.genfromtxt(
        'Population_Data.csv', delimiter=',', skip_header=True, dtype=str)
    species_data = np.genfromtxt(
        'Threatened_Species.csv', delimiter=',', skip_header=True, dtype=str)
    country_data = np.genfromtxt(
        'Country_Data.csv', delimiter=',', skip_header=True, dtype=str)

    if user_input(country_data)[2] == 'country':
        pass
    elif user_input(country_data)[2] == 'region':
        pass


if __name__ == '__main__':
    main()

    # def data_computation(type, data_set1, data_set2, data_set3):
    # # Creates empty list that will store all the chosen school's enrollment data.
    # data = []
    # # Creates a list that stores the arrays of all the school data.
    # list_data = [data_set1, data_set2, data_set3]
    # # Creates a while loop that runs until the code runs 3 times (for each grade).
    # iteration = 1
    # while iteration <= 3:
    #     # Create a for loop that will run for all 3 data sets.
    #     for year in range(0, 3):
    #         # Finds the position of the chosen school code in the given years array.
    #         position = np.where(list_data[year] == int(None))
    #         # Reassigns the position from tuple format to individual x y coordinates.
    #         (x, y) = (position[0], position[1])
    #         # Stores the data for given school, year, and grade.
    #         enrollment = list_data[year][x, y + iteration]
    #         # Adds the data to the data list
    #         data.append(enrollment)
    #     # Tracks how many times the while loop has run.
    #     iteration += 1
    # return data
