# final_project.py
# Aarsh Shah, Phoenix Bouma ENDG 233 F21
# A terminal-based application to process and compute data based on given user input and data csv files.

# imports numpy and matplotlib libraries.
import numpy as np
import matplotlib.pyplot as plt


class dataClass():
    def __init__(self, inp):
        self.inp = inp
        self.population_data = np.genfromtxt(
        'Population_Data.csv', delimiter=',', skip_header=True, dtype=str)
        self.species_data = np.genfromtxt(
        'Threatened_Species.csv', delimiter=',', skip_header=True, dtype=str)
        self.country_data = np.genfromtxt(
        'Country_Data.csv', delimiter=',', skip_header=True, dtype=str)

    def print_countries(self):

        position = np.where(self.country_data == self.inp)#finds positions of country in region or continent

        for i in position[0]:

            print('{}'.format(self.country_data[i][0]), end =', ')

        print()#empty line

        choice = -1
        user_input = input('Select a country for more data: ').title()

        while choice != 0:

            
            print('If you would like to see the population trend in the past 20 years select: 1')
            print('If you would like to see amount of threatened species select: 2')
            print('To change selected country select: 3')
            print('To quit select: 0')
            choice = int(input('Selection : '))

            if choice == 1:
                pos = np.where(self.population_data == user_input)
                years = [i for i in range(2000,2021)]#list for years
                population = list(self.population_data[pos[0][0]])#creates list using position
                del population[0] # deletes name of country in data
                iteration = 0
                for i in population:
                    population[iteration] = int(i)/1000
                    iteration += 1
                print(population)
                plt.plot(years,population, 'r--', label='Population Trend in {}'.format(user_input))
                plt.ylabel('Population in thousands')
                plt.xlabel('Years')
                plt.show()
                
                
                
            

    def print_countries_population(self):
        pass

    def change_selected(self,inp):
        self.inp = inp

    def menu(self):
        user_choice = -1
        while user_choice != 0:

            print('To see countries in selected region or continent select: 1')
            print('To see countries population in selected region or continent select: 2')
            print('To change selected region or continent select: 3')
            print('To quit select: 0')

            user_choice = int(input('Enter selection: '))

            if user_choice == 1:
                self.print_countries()

            if user_choice == 3:
                new_inp = input('Select a new region or continent: ').title()
                self.change_selected(new_inp)



def main():
    # Creates a numpy array from the population, species, and country data and stores it in a its respective variable.
    country_list = np.array(np.genfromtxt('Country_Data.csv',delimiter=',', skip_header=True, dtype=str))

    print('Eng 233 Multi Region Data')
    user_input = 'not valid'
    while user_input not in country_list:
        user_input = input('Please enter a Region or a Continent: ').title()
        if user_input in country_list:
            data = dataClass(user_input)
            data.menu()
        else:
            print('You must select a valid region or continent')

    
        

if __name__ == '__main__':
    main()