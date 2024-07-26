import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITY_INPUT = ['chicago', 'new york city', 'washington']

MONTH_INPUT = ["january", "february", "march", "april", "may", "june"]

DAY_INPUT = ["0", "1", "2", "3", "4", "5", "6"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n')
        city = city.lower()
        if(city in CITY_INPUT):
            break
        print('Invalid, please enter ' + ', '.join(CITY_INPUT))
    
    while True:
        type = input('Would you like to filter the data by month, day, or not at all?\n')
        type = type.lower()
        if (type in ["month", "day", "not at all"]):
            break
        print('Invalid, please enter "month", "day" or "not at all"')
        
    # get user input for month (all, january, february, ... , june)
    if (type == "month"):
        day = "all"
        while True:
            month = input('Which month - January, February, March, April, May, or June?\n')
            month = month.lower()
            if (month in MONTH_INPUT):
                break
            print('Invalid, please enter ' + ', '.join(MONTH_INPUT))
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if (type == "day"):
        month = "all"
        while True:
            day = input('Which day - 0.Monday, 1.Tuesday, 2.Wednesday, 3.Thursday, 4.Friday, 5.Saturday, or 6.Sunday?\n')
            if (day in DAY_INPUT):
                break
            print('Invalid, please enter ' + ', '.join(DAY_INPUT))

    # get month and day when type = not at all
    if (type == "not at all"):
        day = "all"
        month = "all"
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week
    df['hour'] = df['Start Time'].dt.hour
    df['StationSE'] = df['Start Station'] + " to " + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = MONTH_INPUT
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == int(day)]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month: {}".format(df['month'].mode()[0]))

    # display the most common day of week
    print("The most common day of week: {}".format(df['day_of_week'].mode()[0]))


    # display the most common start hour
    print("The most common hour: {}".format(df['hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common Start Station: {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("The most common End Station: {}".format(df['End Station'].mode()[0]))


    # display most frequent combination of start station and end station trip
    print("The most common start station and end station trip: {}".format(df['StationSE'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total Travel Time: {}s".format(np.sum(df['Trip Duration'])))

    # display mean travel time
    print("Mean Travel Time: {}s".format(np.mean(df['Trip Duration'])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Number of User Type: {}'.format(df["User Type"].value_counts()))

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Number of Gender: {}'.format(df["Gender"].value_counts()))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        
        print('\nBirth Year Stats:')
        print(f'Earliest year of birth: {earliest_year}')
        print(f'Most recent year of birth: {most_recent_year}')
        print(f'Most common year of birth: {most_common_year}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df, recordQuantity):
    """Displays raw data upon request by the user."""
    row_index = 0
    display_more = "yes"
    while display_more == 'yes':
        print(df.iloc[row_index:row_index + recordQuantity])
        row_index += recordQuantity
        display_more = input(f'Would you like to see {recordQuantity} more lines of raw data? Enter yes or no.\n').lower()



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df, 5)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
