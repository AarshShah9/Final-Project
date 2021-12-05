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

    def countries_in_region(self):
        '''Finds positions of country in region or continent
        Returns: A list of all the countries in the chosen region'''
        position = np.where(self.country_data == self.input)
        return [self.country_data[i][0] for i in position[0]]

    def countries_in_sub_region(self):
        '''THIS DOESNT WORK Finds positions of sub-regions in region or continent
        Returns: A list of all the countries in the chosen region'''
        position = np.where(self.country_data == self.input)
        sub_regions = list(set(
            [self.country_data[i][2] for i in position[0]]))
        pos = []
        for i in sub_regions:
            pos.append(np.where(self.country_data == i))

        return pos

    def compute_species_data(self):
        (plant_data, fish_data, bird_data, mammal_data) = ([], [], [], [])

        for i in self.countries_in_region():
            position = np.where(self.species_data == i)
            (x, y) = position[0][0], position[1][0]
            plant_data.append(self.species_data[x][y+1])
            fish_data.append(self.species_data[x][y+2])
            bird_data.append(self.species_data[x][y+3])
            mammal_data.append(self.species_data[x][y+4])

        sums = [sum(list(map(int, plant_data))), sum(list(map(int, fish_data))), sum(
            list(map(int, bird_data))), sum(list(map(int, mammal_data)))]

        print(f'''Number of endangered species by type in {self.input}:
        Plants: {sums[0]}
        Fish: {sums[1]}
        Birds: {sums[2]}
        Mammals: {sums[3]}
        ''')

        # Creating the bar plot
        plt.bar(['Plants', 'Fish', 'Birds', 'Mammals'], sums, color=['red', 'blue', 'yellow', 'green'],
                width=0.5)
        plt.xlabel('Types of Species')
        plt.ylabel('Number of Species')
        plt.title(f'Number of Endangered Species in {self.input}')
        plt.show()

    def size_of_region(self):

        area_data = []
        for i in self.countries_in_region():
            position = np.where(self.country_data == i)
            (x, y) = position[0][0], position[1][0]
            area_data.append(self.country_data[x][y+3])

        for i in area_data:
            if i == '':
                area_data.remove(i)

        area_total = (list(map(int, area_data)))
        print(
            f'\nThe total number of area {self.input} takes up: {sum(area_total)} km^2')

        region_max = np.max(area_total)
        pos = np.where(self.country_data == str(region_max))[0]
        biggest_country = self.country_data[pos][0]
        print(
            f'The largest country in the region is {biggest_country[0]} with an area of {region_max} km^2')

        # Creating the bar plot
        plt.bar(self.countries_in_region(), area_total, color='red')
        plt.xlabel('Countries')
        plt.ylabel('Size in Square Km')
        plt.title(f'Different populations for the countries in {self.input}')
        plt.xticks(rotation=90)
        plt.show()

    def population_data_country(self):
        pos = np.where(self.population_data == self.input)
        # list for years
        years = [i for i in range(2000, 2021)]
        # creates list using position
        population = list(self.population_data[pos[0][0]])
        del population[0]  # deletes name of country in data
        for iteration, i in enumerate(population):
            population[iteration] = int(i)/1000

        print(f'The mean population from 2000-2020 is: {np.mean(population)}')
        plt.plot(years, population, 'r--')
        plt.ylabel('Population in thousands')
        plt.xlabel('Years')
        plt.title(f'Population Trend in {self.input}')
        plt.xticks(range(2000, 2022, 2))
        plt.show()

    def change_selected(self):
        test_case = dataClass(None,None)
        user_input = 'not valid'
        while user_input not in test_case.return_data()[3]:
            user_input = input('Please enter a Country or a Continent: ').title()
            if user_input in test_case.return_data()[3]:
               self.input = user_input
               self.type = type1(user_input)
            else:
                print('You must select a valid region or continent')


def menu(data):
    user_choice = -1

    while user_choice != 0:
        print('\nTo quit select: 0')
        print('To change selected country or continent select: 1')

        if data.return_data()[4] == 'Continent':
            print('To see total number of Plants, Fish, Birds, and Mammals in the chosen region and sub-region select: 2')
            print('To see the amount of land area the region takes up select: 3')
        else:
            print('To see population data on chosen country select: 2')

        user_choice = int(input('Enter selection: '))

        if (user_choice == 2) and data.return_data()[4] == 'Continent':
            data.compute_species_data()
        elif (user_choice == 2) and data.return_data()[4] == 'Country':
            data.population_data_country()
        elif (user_choice == 3) and (data.return_data()[4] == 'Continent'):
            data.size_of_region()
        elif user_choice == 1:
            data.change_selected()
        elif user_choice == 0:
            quit()
        elif user_choice == 5:
            print(data.countries_in_sub_region())
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