# final_project.py
# Aarsh Shah, Phoenix Bouma ENDG 233 F21
# A terminal-based application to process and compute data based on given user input and data csv files.

# imports numpy and matplotlib libraries.
import numpy as np
import matplotlib.pyplot as plt


class dataClass():
    def __init__(self, input, type):
        self.input = input
        self.population_data = np.genfromtxt(
            'Population_Data.csv', delimiter=',', skip_header=True, dtype=str)
        self.species_data = np.genfromtxt(
            'Threatened_Species.csv', delimiter=',', skip_header=True, dtype=str)
        self.country_data = np.genfromtxt(
            'Country_Data.csv', delimiter=',', skip_header=True, dtype=str)
        self.type = type

    def return_data(self):
        """Method that allows the variables declared in the class to be accessed globally via indexing of the list"""
        return [self.input, self.population_data, self.species_data, self.country_data, self.type]

    def countries_in_continent(self):
        # finds positions of country in region or continent
        position = np.where(self.country_data == self.input)
        return [self.country_data[i][0] for i in position[0]]

    def print_countries(self):
        print(", ".join(self.countries_in_continent()))

        choice = -1
        user_input = input('\nSelect a country for more data: ').title()

        while choice != 0:

            print(
                'If you would like to see the population trend in the past 20 years select: 1')
            print('If you would like to see amount of threatened species select: 2')
            print('To change selected country select: 3')
            print('To quit select: 0')
            choice = int(input('Selection : '))

            if choice == 1:
                pos = np.where(self.population_data == user_input)
                years = [i for i in range(2000, 2021)]  # list for years
                # creates list using position
                population = list(self.population_data[pos[0][0]])
                del population[0]  # deletes name of country in data
                for iteration, i in enumerate(population):
                    population[iteration] = int(i)/1000
                print(population)
                plt.plot(years, population, 'r--',
                         label='Population Trend in {}'.format(user_input))
                plt.ylabel('Population in thousands')
                plt.xlabel('Years')
                plt.show()

    def print_countries_population(self):
        pass

    def compute_species_data(self):
        # new_species_data = self.species_data.astype(int)

        if self.type == 'Continent':
            places = self.countries_in_continent()
        else:
            places = [self.input]

        plant_data = []
        fish_data = []
        bird_data = []
        mammal_data = []

        for i in places:
            position = np.where(self.species_data == i)
            (x, y) = position[0][0], position[1][0]
            plant_data.append(self.species_data[x][y+1])
            fish_data.append(self.species_data[x][y+2])
            bird_data.append(self.species_data[x][y+3])
            mammal_data.append(self.species_data[x][y+4])

        plant_data_int = list(map(int, plant_data))
        fish_data_int = list(map(int, fish_data))
        bird_data_int = list(map(int, bird_data))
        mammal_data_int = list(map(int, mammal_data))

        return [sum(plant_data_int), sum(fish_data_int), sum(bird_data_int), sum(mammal_data_int)]

    def size_of_region(self):
        pass

    def change_selected(self, input):
        self.input = input


def menu(data):
    user_choice = -1

    while user_choice != 0:
        print('To quit select: 0')
        print('To see countries population in selected country or continent select: 1')
        print('To change selected country or continent select: 2')
        print('To see total number of Plants, Fish, Birds, and Mammals in the chosen continent or country select: 3')

        if data.return_data()[4] == 'Continent':
            print('To see countries in selected region or continent select: 4')
        else:
            print()

        user_choice = int(input('Enter selection: '))

        if user_choice == 1:
            pass

        elif user_choice == 2:
            new_input = input('Select a new region or continent: ').title()
            data.change_selected(new_input)

        elif (user_choice == 3):
            print(data.compute_species_data())

        elif (user_choice == 4) and data.return_data()[4] == 'Continent':
            data.print_countries()

        else:
            print('Please Try again that is an invalid choice')


def type1(user_input):
    test2 = dataClass(user_input, None)
    return (
        'Continent'
        if test2.return_data()[0] in test2.return_data()[3][:, 1]
        else 'Country'
    )


def main():
    test1 = dataClass(None, None)
    print('Eng 233 Multi Region Data')
    user_input = 'not valid'
    while user_input not in test1.return_data()[3]:
        user_input = input('Please enter a Country or a Continent: ').title()
        if user_input in test1.return_data()[3]:
            data = dataClass(user_input, type1(user_input))
            menu(data)
        else:
            print('You must select a valid region or continent')


if __name__ == '__main__':
    main()
