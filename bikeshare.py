import time
import calendar
import datetime
import pandas as pd

# create dictionary to get filename based on user input
CITY_DATA = {'chicago': 'chicago.csv', 'new york': 'new_york_city.csv', 'washington': 'washington.csv'}
# list of available months used to validate user input and convert month number to name
months = ["january", "february", "march", "april", "may", "june"]
# used to validate user input
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def get_filters():
    """Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    """

    valid_inputs_city = list(CITY_DATA.keys())
    valid_inputs_usr_choice = ["month", "day", "all"]

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user inputs and compare with lists of valid inputs
    # prompt user to enter a new value until it matches one of the valid inputs

    # first: get input for city
    while True:
        city = input("Please choose a city.\n"
                     "You can choose Chicago, New York or Washington.\n"
                     "No gender and birth info available for Washington").lower()

        # if user input is valid then break loop
        if city in valid_inputs_city:
            break

        # user input is not valid: prompt error message and continue with loop to get new user input
        else:
            print("Oops! That ist not a valid input. Please, try again")

    # second: Ask user which filter he want's to apply and store selection in 'usr_choice'
    while True:
        usr_choice = input("Would you like to filter the data by month or day or not at all?\n"
                           "Type \"all\" if you wan\'t to apply no filter\n").lower()

        # if user input is valid then break loop
        if usr_choice in valid_inputs_usr_choice:
            break

        # user input is not valid: prompt error message and continue with loop to get new user input
        else:
            print("Oops! That ist not a valid input. Please, try again")

    # if user choice is "month" then ask user which month and store selection in 'month'
    if usr_choice == "month":
        while True:
            month = input("Please choose a month.\n"
                          "You can choose: January, February, March, April, May and June.\n").lower()

            # if user input is valid then break loop
            if month in months:
                # user choose month so no day filter is applied => set 'day' to "all"
                day = "all"
                break

            # user input is not valid: prompt error message and continue with loop to get new user input
            else:
                print("Oops! That ist not a valid input. Please, try again")

    # if user choice is "day" then ask user which day and store selection in 'day'
    elif usr_choice == "day":
        while True:
            day = input("Please choose a day of week.\n"
                        "Please type in Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday\n").lower()

            # if user input is valid then break loop
            if day in days:
                # user choose day so no month filter is applied => set 'month' to "all"
                month = "all"
                break

            # user input is not valid: prompt error message and continue with loop to get new user input
            else:
                print("Oops! That ist not a valid input. Please, try again")

    # only other valid user input = "all". Set 'month' and 'day' to "all" to apply no filter at all
    else:
        month = "all"
        day = "all"

    print('-' * 40)

    return city, month, day


def load_data(city, month, day):
    """Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        df - pandas DataFrame containing city data filtered by month and day

    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df["Start Time"].dt.month
    df['day_of_week'] = df["Start Time"].dt.weekday_name
    df['hour'] = df["Start Time"].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use index of the months list to get the corresponding int.
        month = months.index(month) + 1  # +1 to get right month

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Calculates and displays statistics on the most frequent times of travel.

    Args:
        (pandas.DataFrame) df - pandas DataFrame containing city data filtered by month and day

    Returns:
        None

    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # calculate the most common month as number
    most_common_month_num = int((df['month'].mode()[0]))
    # get the month name from month number
    most_common_month_name = calendar.month_name[most_common_month_num]
    # display the most common month
    print("The most common month is: {}".format(most_common_month_name))

    # calculate and display the most common day of week
    most_common_dayofweek = df['day_of_week'].mode()[0]
    print("The most common day of the week is: {}".format(most_common_dayofweek))

    # calculate and display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print("The most common start hour is: {}".format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Calculates and displays statistics on the most popular stations and trip.

    Args:
        (pandas.DataFrame) df - pandas DataFrame containing city data filtered by month and day

    Returns:
        None

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # calculate and display most commonly used start station
    start_station_most_commonly = df['Start Station'].mode()[0]
    print("The most commonly used start station is: {}".format(start_station_most_commonly))

    # calculate and display most commonly used end station
    end_station_most_commonly = df['End Station'].mode()[0]
    print("The most commonly used end station is: {}".format(end_station_most_commonly))

    # calculate and display most frequent combination of start station and end station trip
    start_and_end_station_most_commonly = (df['End Station'] + " - " + df['Start Station']).mode()[0]
    print("The most frequent combination"
          "of start station and end station is: {}".format(start_and_end_station_most_commonly))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Calculates and displays statistics on bikeshare users.

    If the necessary columns are not present in the dataframe, the user will be notified about it.

    Args:
        (pandas.DataFrame) df - pandas DataFrame containing city data filtered by month and day

    Returns:
        None

    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate total travel time
    total_travel_time_in_sec = int(df['Trip Duration'].sum())
    # convert the total travel time in days, hours, minutes and seconds and display value
    total_travel_time = datetime.timedelta(seconds=total_travel_time_in_sec)
    print("The total travel time is: {} seconds or {} [hh:mm:ss]".format(total_travel_time_in_sec, total_travel_time))

    # calculate mean travel time
    mean_travel_time_in_sec = int(df['Trip Duration'].mean())
    # convert the mean travel time in hours, minutes and seconds and display value
    mean_travel_time = datetime.timedelta(seconds=mean_travel_time_in_sec)
    print("The mean travel time is: {} seconds or {} [hh:mm:ss]".format(mean_travel_time_in_sec, mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        (pandas.DataFrame) df - pandas DataFrame containing city data filtered by month and day

    Returns:
        None

    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Calculate and display counts of user types
    user_types_count = df['User Type'].value_counts()
    print("There are the following users:\n{}.".format(user_types_count))

    # Display counts of gender only if necessary data is available
    # If column "Gender" exists in 'df' calculate counts of gender and display.
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print("There are these genders:\n{}".format(gender_count))

    # Column not present in 'df': Display message
    else:
        print("There is no gender information for this city.")

    # Display earliest, most recent, and most common year of birth only if necessary data is available
    # If column "Birth Year" exists in 'df' calculate counts of gender and display.
    if 'Birth Year' in df.columns:
        year_of_birth_earliest = int(df['Birth Year'].min())
        print("The earliest year of birth is: {}".format(year_of_birth_earliest))

        year_of_birth_most_recent = int(df['Birth Year'].max())
        print("The most recent year of birth is: {}".format(year_of_birth_most_recent))

        year_of_birth_average = int(round(df['Birth Year'].mean(), 0))
        print("The average year of birth is: {}".format(year_of_birth_average))

    # Column not present in 'df': Display message
    else:
        print("There is no birth information for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """Prompts the user if they want to see 5 lines of raw data and iterates until answer is "no"

    Args:
        (pandas.DataFrame) df - pandas DataFrame containing city data filtered by month and day

    Returns:
        None

    """

    # row_counter = 0 to start with row number 1
    row_counter = 0
    # display the total count of rows
    print("\nThe filtered data set has a total of {} rows.\n".format(df.shape[0]))
    # expand the output display to see more columns
    pd.set_option("display.max_columns", 20)

    # prompt user if the want's to see the raw data
    while True:
        raw_data_prompt = input('Would you like to see the raw data?\n'
                                'Enter yes or no: ').lower()

        # if user input is valid then break loop
        if raw_data_prompt in ["yes", "no", "y", "n"]:
            break

        # user input is not valid: prompt error message and continue with loop to get new user input
        else:
            print("Oops! That ist not a valid input. Please, try again")

    # if user choose "yes" or "y" create a new variable and assign it to "yes"
    if raw_data_prompt in ["yes", "y"]:
        # new variable to display second prompt
        more_data_prompt = "yes"

        # start loop and display the first 5 lines
        while more_data_prompt in ["yes", "y"]:
            print(df.iloc[row_counter: row_counter + 5])
            # increment row_counter by 5 to get start row for next iteration
            row_counter += 5
            # check if end of dataset is reached
            if row_counter >= df.shape[0]:
                print("\nYou have reached the end of the data set\n")
                break

            # ask user if they want to see 5 more rows and validate input
            while True:
                more_data_prompt = input('Want to see 5 more rows?\n'
                                         'Enter yes or no: ').lower()
                if more_data_prompt in ["yes", "no", "y", "n"]:
                    break
                else:
                    print("Oops! That ist not a valid input. Please, try again")

    print('-' * 40)


def main():
    """Get user choice, filter data, display statistics and raw data, ask user if he wants to restart"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart?\nEnter yes or no.\n')
        if restart.lower() not in ['yes', 'y']:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
