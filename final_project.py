# final_project.py
# Aarsh Shah, Phoenix Bouma ENDG 233 F21
# A terminal-based application to process and compute data based on given user input and data csv files.

# imports numpy and matplotlib libraries.
import numpy as np
import matplotlib.pyplot as plt


class dataClass:
    def __init__(self, input, type):
        """Constructor for the dataClass that sets class variables for the main variables used in the entire program.
        Parameters: 
            input: Variable for the users input which stores the place selected
            type: Variable that stores the type of input recieved (country or region/continent).
        """
        # Input variable that stores the chosen region/ country by the user.
        self.input = input
        # Variables include: 3 Numpy arrays for the population, threatened species, and country data.
        self.population_data = np.genfromtxt("Population_Data.csv",
                                             delimiter=",",
                                             skip_header=True,
                                             dtype=str)
        self.species_data = np.genfromtxt("Threatened_Species.csv",
                                          delimiter=",",
                                          skip_header=True,
                                          dtype=str)
        self.country_data = np.genfromtxt("Country_Data.csv",
                                          delimiter=",",
                                          skip_header=True,
                                          dtype=str)
        # Type variable that stores the type of input recieved (country or region/continent)
        self.type = type

    def return_data(self):
        """Method that allows the variables declared in the class to be accessed globally via indexing of the list
        Returns: list contained all the variables set in the constructor of the class"""
        return [
            self.input,
            self.population_data,
            self.species_data,
            self.country_data,
            self.type,
        ]

    def countries_in_region(self):
        """Finds positions of country in region or continent
        Returns: A list of all the countries in the chosen region"""
        position = np.where(self.country_data == self.input)#finds position of the region
        return [
            self.country_data[i][0] for i in position[0]
            if self.country_data[i][-1] != ""
        ]#returns a list of the countries using the position and removes any invalida data

    def sub_regions_in_cont(self):
        """Finds positions of sub-regions in region or continent
        Returns: A list of the sub regions in chosen continent"""
        position = np.where(self.country_data == self.input)#finds postion of continents
        return list(set([self.country_data[i][2] for i in position[0]]))#makes a set to get rid of duplicates

    def countries_in_sub_region(self):
        """Finds positions of countries in the sub-regions
        Returns: A list of all the countries in the chosen region"""
        position = np.where(self.country_data == self.input)#finds postion of the sub regions or continent
        sub_regions = list(set([self.country_data[i][2] for i in position[0]]))#makes a list of the sub regions
        pos = []
        for i in sub_regions:
            pos.append(np.where(self.country_data == i))#appends the country to a list

        return pos

    def compute_species_data(self):
        """Method that finds the postions of each species' data, sums the values at
        those positons and prints out the totals in a print statements and plots"""

        # Creates empty lists for each type of species.
        (plant_data, fish_data, bird_data, mammal_data) = ([], [], [], [])
        # For loop that takes every country in the chosen region.
        for i in self.countries_in_region():
            # Finds the position of the name of each country in species array.
            position = np.where(self.species_data == i)
            (x, y) = position[0][0], position[1][0]
            # Then uses the position of the country to find the position
            # of the species data and add the value there to each respective list.
            plant_data.append(self.species_data[x][y + 1])
            fish_data.append(self.species_data[x][y + 2])
            bird_data.append(self.species_data[x][y + 3])
            mammal_data.append(self.species_data[x][y + 4])

        # Takes the sums of each of the 4 species' lists.
        sums = [
            sum(list(map(int, plant_data))),
            sum(list(map(int, fish_data))),
            sum(list(map(int, bird_data))),
            sum(list(map(int, mammal_data))),
        ]
        # Series of print statements that prints out all the species data that was located and computated above.
        print(f'\nNumber of endangered species by type in {self.input}:')
        print(f'Plants: {sums[0]}')
        print(f'Fish: {sums[1]}')
        print(f'Birds: {sums[2]}')
        print(f'Mammals: {sums[3]}')
        print('Total number of endangered species: {}'.format(sum(sums)))
        print('Average endangered species: {}'.format(np.mean(sums)))
        print('Number of endangered species per sq km: {}'.format(
            sum(sums) / sum(self.region_area_total())))

        # Creating the bar plot for the species data, which plots the 4 different types of
        # species to the amount of total amount of endangered animals in the region
        plt.bar('Plants', sums[0], color='red', width=0.5, label='Plants')
        plt.bar('Fish', sums[1], color='blue', width=0.5, label='Fish')
        plt.bar('Birds', sums[2], color='yellow', width=0.5, label='Birds')
        plt.bar('Mammals', sums[3], color='green', width=0.5, label='Mammals')
        # Formats the bar plot including title, x-y labels, legend and prints the plot.
        plt.xlabel('Types of Species')
        plt.ylabel('Number of Endangered Species')
        plt.title(f'Number of Endangered Species in {self.input} by type')
        plt.legend(loc='upper right')
        plt.show()

        # Finds the threatend species density for each type and stores it in a list.
        density = []
        for i in range(0, 4):
            density.append(sums[i] / sum(self.region_area_total()))

        # Creating the bar plot for the species data, which plots the 4 different types of
        # species to the endangered animals density in the region
        plt.bar('Plants', density[0], color='red', width=0.5, label='Plants')
        plt.bar('Fish', density[1], color='blue', width=0.5, label='Fish')
        plt.bar('Birds', density[2], color='yellow', width=0.5, label='Birds')
        plt.bar('Mammals',
                density[3],
                color='green',
                width=0.5,
                label='Mammals')
        # Formats the bar plot including title, x-y labels, legend and prints the plot.
        plt.xlabel('Types of Species')
        plt.ylabel('Number of Endangered Species per Km^2 of land')
        plt.title(
            f'Number of Endangered Species per Km^2 of land in {self.input} by type'
        )
        plt.legend(loc='upper right')
        plt.show()

    def region_area_total(self):
        """Method that looks for the postions of all the countries in the chosen
        region and then finds the area of each country which is then stored in a list
        Returns list of all the areas of all the counties in the given region"""
        area_data = []
        for i in self.countries_in_region():
            position = np.where(self.country_data == i)
            (x, y) = position[0][0], position[1][0]
            area_data.append(self.country_data[x][y + 3])

        return [int(i) for i in area_data if i != ""]

    def subregion_area_total(self):
        """Method that looks for the postions of all the sub-regions in the chosen
        region and then finds the area of each sub-region which is then stored in a list
        Returns list of all the areas of the sub-regions in the given region"""
        area_data = []
        for i in self.sub_regions_in_cont():
            position = np.where(self.country_data == i)
            x = position[0][0]
            area_data.append(self.country_data[x][3])

        return [int(i) for i in area_data if i != ""]

    def size_of_region(self):
        print(
            f"\nThe total number of area {self.input} takes up: {sum(self.region_area_total())} km^2"
        )

        region_max = np.max(self.region_area_total())
        pos = np.where(self.country_data == str(region_max))[0]
        biggest_country = self.country_data[pos][0]
        print(
            f"The largest country in the region is {biggest_country[0]} with an area of {region_max} km^2"
        )

        # Creating the bar plot for the area for each country in the chosen region
        i = 0
        while i < len(self.countries_in_region()):
            plt.bar(self.countries_in_region()[i],
                    self.region_area_total()[i],
                    label=self.countries_in_region()[i])
            i += 1
        # All formatting including title, x-y labels, legend and printing the plot
        plt.xlabel("Countries")
        plt.ylabel("Size in Square Km")
        plt.title(f"Different size for the countries in {self.input}")
        plt.xticks(rotation=90)
        plt.legend(loc='upper right')
        plt.show()

        # Creating the bar plot for the area for each sub-region in the chosen region
        i = 0
        while i < len(self.sub_regions_in_cont()):
            plt.bar(self.sub_regions_in_cont()[i],
                    self.subregion_area_total()[i],
                    label=self.sub_regions_in_cont()[i])
            i += 1
        # All formatting including title, x-y labels, legend and printing the plot
        plt.xlabel("Countries")
        plt.ylabel("Size in Square Km")
        plt.title(f"Different size for the sub-regions in {self.input}")
        plt.legend(loc='upper right')
        plt.show()

    def population_data_country(self):
        pos = np.where(self.population_data == self.input)
        # List for years.
        years = [i for i in range(2000, 2021)]
        # Creates list using position.
        population = list(self.population_data[pos[0][0]])
        del population[0]  # deletes name of country in data

        max_pop = max(population)
        min_pop = min(population)
        # Finds max year
        max_year = np.where(
            self.population_data[pos[0][0]] == str(max_pop))[0][0]
        # Finds min year
        min_year = np.where(
            self.population_data[pos[0][0]] == str(min_pop))[0][0]

        for iteration, i in enumerate(population):
            population[iteration] = int(i) / 1000

        print(
            f"\nThe mean population from 2000-2020 is: {np.mean(population)} thousand"
        )
        print("Max population during {} at {} people".format(
            1999 + max_year, max_pop))  # add 1999 because of index
        print("Min population during {} at {} people".format(
            1999 + min_year, min_pop))

        plt.plot(years, population, "r--", label='Population Trend')
        # Formats the plot including title, x-y labels, x-axis, legend and prints the plot.
        plt.ylabel("Population in thousands")
        plt.xlabel("Years")
        plt.title(f"Population Trend in {self.input}")
        plt.xticks(range(2000, 2022, 2))
        plt.legend(loc='upper right')
        plt.show()

        position = np.where(self.country_data == self.input)
        (x) = position[0][0]
        area = int(self.country_data[x][3])

        # Computes the population for each year from 2000-2020 and stores it in a list
        actual_population = [i * 1000 for i in population]
        density = [i / area for i in actual_population]

        # Ploting population density over 20 years (x-axis: each year, y-axis: density for each year)
        plt.plot(years, density, "r--", label='Population to Area Trend')
        # Formats the plot including title, x-y labels, x-axis, legend and prints the plot.
        plt.ylabel("Population density")
        plt.xlabel("Years")
        plt.title(f"Population Density Trend in {self.input}")
        plt.xticks(range(2000, 2022, 2))
        plt.legend(loc='upper right')
        plt.show()

    def change_selected(self):
        """Method that allows the user to change their selected 
        country/region which then allows them to get data on the new input"""
        test_case = dataClass(None, None)#creates an empty class used for data
        user_input = "not valid"
        while user_input not in test_case.return_data()[3]:#checks if input is in country data
            user_input = input(
                "Please enter a Country or a Continent: ").title()
            if user_input in test_case.return_data()[3]:
                self.input = user_input #sets user input as the new input
                self.type = type1(user_input)#finds the type
            else:
                print("You must select a valid region or continent")


def menu(data):
    """The menu function prints out different options for printing data depending on if 
    the input was a region or country and takes another input for what the user wants data on.
    The function then uses a series of conditional statments to call a method from the dataClass that
    will print out the requested data."""

    # While loop that runs until the user chooses to quit.
    user_choice = -1
    while user_choice != 0:
        # Prints out a series of statements for the different options.
        print("\nTo quit select: 0")
        print("To change selected country or continent select: 1")
        print(
            "To see total number of Plants, Fish, Birds, and Mammals in the chosen region and sub-region select: 2"
        )
        # If the place the user chose was a region then these print statements are also printed.
        if data.return_data()[4] == "Continent":
            print(
                "To see the amount of land area the region takes up select: 3")
        # If the place the user chose was a country then these print statements are also printed.
        else:
            print(
                "To see population data over the past 20 years on the chosen country select: 3"
            )
        # Gets user input in integer form.
        user_choice = int(input("Enter selection: "))
        # Series of conditional statements that call a method from the dataClass depending on the input.
        if user_choice == 2:
            data.compute_species_data()
        elif (user_choice == 3) and data.return_data()[4] == "Country":
            data.population_data_country()
        elif (user_choice == 3) and (data.return_data()[4] == "Continent"):
            data.size_of_region()
        elif user_choice == 1:
            data.change_selected()
        # If the user choses 'zero' it ends the program.
        elif user_choice == 0:
            quit()
        # If the user inputs an invalid integer they are prompted to try again.
        else:
            print("Please Try again that is an invalid choice")


def type1(user_input):
    """Function that determines the charcteristic of the users input (Whether its a region/continent or a country)
    Returns: A string thats either 'Continent' or 'Country'
    """
    # Creates a test instance of the dataClass to check if users input is a country or a continent.
    test2 = dataClass(user_input, None)
    # Returns a string depending on the condition.
    return ("Continent" if test2.return_data()[0]
            in test2.return_data()[3][:, 1] else "Country")


def main():
    """Main function for the program that creates an instance of the dataClass that will 
    be accessed throughout the program. And also gets the user input for the country/region 
    and ensures they are valid inputs. Then calls the menu function to continue the program."""
    # Creates an instance of the dataClass for conditional arguments.
    test1 = dataClass(None, None)
    # Prints program title.
    print("Eng 233 Multi Region Data")
    # while loop that ends once the user inputs a valid country.
    user_input = "not valid"
    while user_input not in test1.return_data()[3]:
        # Gets the users input.
        user_input = input("Please enter a Country or a Continent: ").title()
        # Checks to see if the input exists within the data files.
        if user_input in test1.return_data()[3]:
            # Creates the main instance of the data class and calls the menu function.
            data = dataClass(user_input, type1(user_input))
            menu(data)
        # If the input is not valid the user is prompted to try again.
        else:
            print("You must select a valid region or continent")


# Runs the program by calling the main function.
if __name__ == "__main__":
    main()