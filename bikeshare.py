import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago' : 'chicago.csv',
              'new york city' : 'new_york_city.csv',
              'washington' : 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #get user input for city (chicago, new york city, washington).
    city = input('Please pick either Chicago, New York City, or Washington: ')
    city = city.lower()
    while city not in CITY_DATA:
        city = input('Sorry, invalid input, try again: ')

    #get user input for month (all, january, february, ... , june)
    month = input('Please pick a month or pick all: ')
    month = month.lower()
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while month not in months:
        month = input('Sorry, invalid input, try again: ')

    #get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please pick a day of the week or pick all: ')
    day = day.lower()
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
    'sunday', 'all']
    while day not in days:
        city = input('Sorry, invalid input, try again: ')


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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month']== month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    most_common_month = df['month'].mode()[0]

    #display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]

    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]

    print('Most Frequent Start Hour: ', popular_hour)
    print('Most common day is: ', most_common_day)
    print('Most common month is: ', most_common_month)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    df['trip'] = df['Start Station'].str.cat(df['End Station'], sep = ' - ')

    #display most commonly used start station
    popular_start_station = df['Start Station'].mode().to_string()

    #display most commonly used end station
    popular_end_station = df['End Station'].mode().to_string()

    #display most frequent combination of start station and end station trip
    most_common_trip = df['trip'].mode().to_string()

    print('Most common start station is:: ', popular_start_station)
    print('Most common end station is: ', popular_end_station)
    print('Most common trips are: ', most_common_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    trip_duration_sum = df['Trip Duration'].sum()


    #display mean travel time
    trip_duration_mean = df['Trip Duration'].mean()

    print('The total amount of trip time is: ', trip_duration_sum, ' seconds')
    print('The mean trip time is: ', trip_duration_mean, ' seconds')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts()

    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
    else:
        genders = ('No data available')

    #Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year_min = int(df['Birth Year'].min())
        birth_year_max = int(df['Birth Year'].max())
        birth_year_pop = int(df['Birth Year'].mode())
    else:
        birth_year_min = ('No data available')
        birth_year_max = ('No data available')
        birth_year_pop = ('No data available')

    print(user_types)
    print ('Gender: ', genders)
    print('Oldest user birth year: ', birth_year_min)
    print('Youngest user birth year: ', birth_year_max)
    print('Most popular user birth year: ', birth_year_pop)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    '''Displays a line of data when user after being asked if they want to see raw data
    asks the user if they would like to see more.'''

    def is_valid(rawdata):
        if rawdata.lower() in ['yes', 'no']:
            return True
        else:
            return False
    rdata = 0
    raw_input = False
    while raw_input == False:
        rawdata = input('\nWould you like to view individual trip data? ')
        raw_input = is_valid(rawdata)
        if raw_input == True:
            break
        else:
            print("Sorry, I do not understand your input. Please type 'yes' or"
                  " 'no'.")
    if rawdata.lower() == 'yes':
        #prints every column of raw data
        print(df[df.columns[0:-1]].iloc[rdata])
        more_data = ''
        while more_data.lower() != 'no':
            raw_input_in = False
            while raw_input_in == False:
                more_data = input('\nWould you like to view more raw trip data? ')
                raw_input_in = is_valid(more_data)
                if raw_input_in == True:
                    break
                else:
                    print('Sorry, I do not understand your input. Type "yes" or "no"')
            if more_data.lower() == 'yes':
                rdata += 1
                print(df[df.columns[0:-1]].iloc[rdata])
            elif more_data.lower() == 'no':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print(display_data(df))
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
