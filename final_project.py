# final_project.py
# Aarsh Shah, Phoenix Bouma ENDG 233 F21
# A terminal-based application to process and compute data based on given user input and data csv files.

# imports numpy and matplotlib libraries.
import numpy as np
import matplotlib.pyplot as plt


class dataClass:
    """dataClass that sets class variables for the main variables used in the entire program.
    The instances' of this class are used to find, compute, and print data from csv data files depending on user inputs.
    Parameters: 
        input: Variable for the users input which stores the place selected.
        type: Variable that stores the type of input recieved (country or region/continent)."""
    def __init__(self, input, type):
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
        # Type variable that stores the type of input recieved (country or region/continent).
        self.type = type

    def return_data(self):
        """Method that allows the variables declared in the class to be accessed globally via indexing of the list.
        Parameters: None (other than 'self' for the instance of the class).
        Returns: list containing all the variables set in the constructor of the class"""
        return [
            self.input,
            self.population_data,
            self.species_data,
            self.country_data,
            self.type,
        ]

    def countries_in_region(self):
        """Finds positions of country in region or continent.
        Parameters: None (other than 'self' for the instance of the class).
        Returns: A list of all the countries in the chosen region."""
        # Finds position of the region.
        position = np.where(self.country_data == self.input)
        # Returns a list of the countries using the position and removes any invalid data.
        return [
            self.country_data[i][0] for i in position[0]
            if self.country_data[i][-1] != ""
        ]

    def sub_regions_in_cont(self):
        """Finds positions of sub-regions in region or continent.
        Parameters: None (other than 'self' for the instance of the class).
        Returns: A list of the sub regions in chosen continent."""
        # Finds postion of continents in the data set.
        position = np.where(self.country_data == self.input)
        # Makes a set of all the sub-regions in a given region, gets rid of duplicates and returns it as a list.
        return list(set([self.country_data[i][2] for i in position[0]]))

    def countries_in_sub_region(self):
        """Finds positions of countries in the sub-regions.
        Parameters: None (other than 'self' for the instance of the class).
        Returns: A list of all the countries in a sub-region."""
        # Finds postion of the sub regions in the region.
        position = np.where(self.country_data == self.input)
        # Makes a list of the sub regions with no duplicates.
        sub_regions = list(set([self.country_data[i][2] for i in position[0]]))
        pos = []
        # Finds all the countries in each sub-region and appends it to a list.
        for i in sub_regions:
            pos.append(np.where(self.country_data == i))

        return pos

    def compute_species_data(self):
        """Method that finds the positions of each species' data, sums the values at
        those positons and prints out the totals in a print statements and plots. 
        It also compares these totals to the amount of land the place takes up and plots based on that data.
        Parameters: None (other than 'self' for the instance of the class).
        Returns: None"""
        # Creates empty lists for each type of species.
        (plant_data, fish_data, bird_data, mammal_data) = ([], [], [], [])
        # For loop that takes every country in the chosen region.
        for i in self.countries_in_region():
            # Finds the position of the name of each country in species array.
            position = np.where(self.species_data == i)
            (x, y) = position[0][0], position[1][0]
            # Then uses the position of the country to find the position.
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
        # Prints out the average number of species across the types.
        print('Average endangered species across the types: {}'.format(
            np.mean(sums)))
        # Finds the endangered species/ to area ratio and prints it out
        print('Number of endangered species per sq km: {}'.format(
            sum(sums) / sum(self.region_area_total())))

        # Creating the bar plot for the species data, which plots the 4 different types of
        # species to the amount of total amount of endangered animals in the region.
        plt.bar('Plants', sums[0], color='red', width=0.5, label='Plants')
        plt.bar('Fish', sums[1], color='blue', width=0.5, label='Fish')
        plt.bar('Birds', sums[2], color='yellow', width=0.5, label='Birds')
        plt.bar('Mammals', sums[3], color='green', width=0.5, label='Mammals')
        # Formats the bar plot including title, x-y labels, legend and prints the plot.
        plt.xlabel('Types of Species')
        plt.ylabel('Number of Endangered Species')
        plt.title(f'Number of Endangered Species in {self.input} by Type')
        plt.legend(loc='upper right')
        plt.show()

        # Finds the threatend species density for each type and stores it in a list.
        density = []
        for i in range(0, 4):
            density.append(sums[i] / sum(self.region_area_total()))

        # Creating the bar plot for the species data, which plots the 4 different types of
        # species to the endangered animals density in the region.
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
            f'Number of Endangered Species per Km^2 of Land in {self.input} by Type'
        )
        plt.legend(loc='upper right')
        plt.show()

    def region_area_total(self):
        """Method that looks for the positions of all the countries in the chosen
        region and then finds the area of each country which is then stored in a list.
        Parameters: None (other than 'self' for the instance of the class).
        Returns: list of all the areas of all the counties in the given region."""
        area_data = []
        for i in self.countries_in_region():
            # Finds the position in the dataset of each country in the region.
            position = np.where(self.country_data == i)
            (x, y) = position[0][0], position[1][0]
            # Appends the area of each country to the list.
            area_data.append(self.country_data[x][y + 3])
        # Returns the list of area in integers and clears any discrepancies in the data.
        return [int(i) for i in area_data if i != ""]

    def subregion_area_total(self):
        """Method that looks for the positions of all the sub-regions in the chosen
        region and then finds the area of each sub-region which is then stored in a list.
        Parameters: None (other than 'self' for the instance of the class)
        Returns: list of all the areas of the sub-regions in the given region"""
        area_data = []
        for i in self.sub_regions_in_cont():
            # Finds position of each sub region.
            position = np.where(self.country_data == i)
            x = position[0][0]
            # Adds the areas each of the countries in the subregion to a list.
            area_data.append(self.country_data[x][3])
        # Returns a list of integers of the area of the countries.
        return [int(i) for i in area_data if i != ""]

    def size_of_region(self):
        """Method that finds the size of a region and the sub-regions within it 
        and prints data based on it, through print statements and plots.
        Parameters: None (other than 'self' for the instance of the class)
        Returns: None"""
        # Prints out the total amount of area a region takes up.
        print(
            f"\nThe total number of area {self.input} takes up: {sum(self.region_area_total())} km^2"
        )
        # Finds the largest country and prints it out.
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
        plt.title(f"Different Sizes for the Countries in {self.input}")
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
        plt.title(f"Different Sizes for the Sub-Regions in {self.input}")
        plt.legend(loc='upper right')
        plt.show()

    def population_data_country(self):
        """Method that finds the population data of a country, and uses it to calculate data 
        such as max's, min's and then creates plots on population and density.
        Parameters: None (other than 'self' for the instance of the class)
        Returns: None"""
        # Finds the position of the chosen country in the data set.
        pos = np.where(self.population_data == self.input)
        # List for years.
        years = [i for i in range(2000, 2021)]
        # Creates list using position.
        population = list(self.population_data[pos[0][0]])
        # Deletes name of country in data.
        del population[0]

        # Finds the smallest and largest values in the population lists
        max_pop = max(population)
        min_pop = min(population)
        # Finds max year
        max_year = np.where(
            self.population_data[pos[0][0]] == str(max_pop))[0][0]
        # Finds min year
        min_year = np.where(
            self.population_data[pos[0][0]] == str(min_pop))[0][0]

        for iteration, i in enumerate(population):
            # Divides population by thousand for simpler reading
            population[iteration] = int(i) / 1000

        # Serie of print statements that print out the data that is computed above.
        print(
            f"\nThe mean population from 2000-2020 is: {np.mean(population)} thousand"
        )
        # add 1999 because of index
        print("Max population during {} at {} people".format(
            1999 + max_year, max_pop))
        print("Min population during {} at {} people".format(
            1999 + min_year, min_pop))

        # Creates a plot for the population trend over 20 years.
        plt.plot(years, population, "r--", label='Population Trend')
        # Formats the plot including title, x-y labels, x-axis, legend and prints the plot.
        plt.ylabel("Population in thousands")
        plt.xlabel("Years")
        plt.title(f"Population Trend in {self.input}")
        plt.xticks(range(2000, 2022, 2))
        plt.legend(loc='upper right')
        plt.show()

        # Finds the area of the chosen country
        position = np.where(self.country_data == self.input)
        (x) = position[0][0]
        area = int(self.country_data[x][3])

        # Computes the population density for each year from 2000-2020 and stores it in a list
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
        country/region which then allows them to get data on the new input
        Parameters: None (other than 'self' for the instance of the class)
        Returns: None"""
        # Creates an object used for data
        test_case = dataClass(None, None)
        user_input = "not valid"
        # Checks if input is in country data
        while user_input not in test_case.return_data()[3]:
            # Gets user input for the new region/country they want.
            user_input = input(
                "Please enter a Country or a Continent: ").title()
            if user_input in test_case.return_data()[3]:
                # Sets user input as the new input
                self.input = user_input
                # Calls function type1 to find the type
                self.type = type1(user_input)
            else:
                # Case for an invalid input
                print("You must select a valid region or continent")


def menu(data):
    """The menu function prints out different options for printing data depending on if 
    the input was a region or country and takes another input for what the user wants data on.
    The function then uses a series of conditional statments to call a method from the dataClass that
    will print out the requested data.
    Parameters: An instance of the dataClass that has the user input and type stored in it.
    Returns: None"""

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
        user_choice1 = (input("Enter selection: "))
        user_choice = int(user_choice1)
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


def type1(user_input_place):
    """Function that determines the charcteristic of the users input (Whether its a region/continent or a country)
    Parameter: variable that stores the users input on the region/country they want.
    Returns: A string thats either 'Continent' or 'Country'
    """
    # Creates a test instance of the dataClass to check if users input is a country or a continent.
    test2 = dataClass(user_input_place, None)
    # Returns a string depending on the condition.
    return ("Continent" if test2.return_data()[0]
            in test2.return_data()[3][:, 1] else "Country")


def main():
    """Main function for the program that creates an instance of the dataClass that will 
    be accessed throughout the program. And also gets the user input for the country/region 
    and ensures they are valid inputs. Then calls the menu function to continue the program.
    Parameters: None
    Returns: None"""
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