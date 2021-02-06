import time
import pandas as pd
import numpy as np
import calendar

# print the version
print(pd.__version__)
CITY_DATA = { 'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv' }
MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
DAY_DATA = {'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'all': 7}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    name = input('Please enter your name: ')
    
    print('Hello {}! Let\'s explore some US bikeshare data!'.format(name.title()))
    
    # get user input for city (Chicago, New York City, Washington). HINT: Use a while loop to handle invalid inputs
    city =''
    print('\nPlease choose ONE of these cities: Chicago, New York City or Washington.')
    print('\nAccepted input: Full name of city in title or lower case e.g. "New York City" or "new york city".')
    
    while city not in CITY_DATA.keys():
        city = str(input('Enter a city: ')).lower()
        
        if city not in CITY_DATA.keys():
           print('That\'s not a valid input. Please try again!')  
        
    print('You have chosen {}.'.format(city))
    
    # get user input for month (All, January, February, ... , June)
    
    month = ''
    print('\nPlease choose ONE month from January to June or "all".')
    print('\nAccepted input: Full name of month or all in title case or lower case e.g. "March" or "march".')
    
    while month not in MONTH_DATA:
        month = str(input('Enter a month or all: ')).lower()
            
        if month not in MONTH_DATA:
           print('That\'s not a valid input. Please try again!')
    
    print('You have chosen {}.'.format(month))

    # get user input for day of week (All, Monday, Tuesday, ... Saturday)
    
    day = ''
    print('\nPlease choose ONE day of the week from Monday to Saturday or "all".')
    print('\nAccepted input: Full name of month or all in title or lower case e.g. "Tuesday" or "tuesday".')
    
    while day not in DAY_DATA:
        day = str(input('Enter a day or all: ')).lower()
            
        if day not in DAY_DATA:
           print('That\'s not a valid input. Please try again!')
    
    print('You have chosen {}.'.format(day))
    print('You have chosen {} as the selected DAY, {} as the selected month and {} as the selected day of the week.'.format(city, month, day))
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
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]


    # filter by day of week if applicable
    if day != 'all':
        # Use the index of the days list to get the corresponding int
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        day = days.index(day) + 1
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


# 1.Most common time
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # 1.1. Most common month: find the most common month 
    popular_month = df['month'].mode()[0]

    print('Most Common Month (1 = January, 2 = February, 3 = March, 4 = April, 5 = May ,6 = June):', popular_month)
    
    # 1.2. Most common day of week: find the most common day of the week 
    common_day = df['day_of_week'].mode()[0]

    print('Most Common Day (1 = Monday, 2 = Tuesday, 3 = Wednesday, 4 = Thursday, 5 = Friday, 6 = Saturday):', common_day )

    # 1.3. Most common hour of day: find the most common hour (from 0 to 23)
    
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    common_hour = df['hour'].mode()[0]
    
    print('Most Common Start Hour:', common_hour)

    # print the calculation performance time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# 2. Most common stations and trip
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # 2.1. Most common start station

    # find the most common start station
    common_start_station = df['Start Station'].mode()[0]

    print('Most Common Start Station:', common_start_station)

    # 2.2. Most common end station

    # find the most common end station
    common_end_station = df['End Station'].mode()[0]

    print('Most Common End Station:', common_end_station)

    # 2.3. Most common trip from start to end

    # find the most common combination
    common_combination = df.groupby(['Start Station','End Station']).size().idxmax()

    print('Most Common Stations Combination:', common_combination)

    # print the calculation performance time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# 3. Trip duration
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # 3.1. Total travel time

    # calculate the total travel time of all trips
    total_travel_time = df['Trip Duration'].sum()

    print('Total travel time:', total_travel_time, 'secs.')

    # 3.2. Average travel time

    # calculate the average travel time of all trips
    average_travel_time = df['Trip Duration'].mean()

    print('Average travel time:', average_travel_time, 'secs.')

    # print the calculation performance time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# 4. User info
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # 4.1. Count of each user type

    # calculate value counts for each user type
    user_types = df['User Type'].value_counts()

    print('Counts of each user type:', user_types)

    # 4.2. Count of each gender

    # calculate value counts for each gender (only available for NYC and Chicago)
    try:
        genders = df['Gender'].value_counts()

        print('Counts of each user gender:', genders)
    except:
        print('No gender data available in this file.')
    # 4.3. Earliest, most recent, most common year of birth (only available for NYC and Chicago)

    # calculate the earliest year of birth, most recent year of birth, most common year of birth
    try:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])

        print('Earliest year of birth:', earliest_year)
        print('\nMost recent year of birth:', most_recent_year)
        print('\nMost common year of birth:', most_common_year)
    except:
        print('No birth year data available in this file.')

    # print the calculation performance time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# 5.
def display_data(df):
    """
    Load the first 10 rows of data for the specified city if asked by users.
    """
    
    print('\nWould you like to view 10 rows of individual trip data?')
    print('\nAccepted input: "Yes" or "No" in title or lower case.')
    view_data = input('Enter "Yes" or "No".\n').title()
    start_loc = 0
    while view_data == 'Yes':
        print(df.iloc[start_loc:start_loc + 10])
        start_loc += 10
        continue_view = input('Do you wish to continue?').title()
        if continue_view != 'Yes':
            break
    print('-'*40)        


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter "yes" or "no".\n')
        if restart.lower() != 'yes':
            break


if __name__ == '__main__':
	main()

#REFERENCE: I HAVE APPLIED PRACTICE SOLUTION 1,2,3 TO MY ASSIGNMENT
#def display_data code is based on (StackOverFlow, 2020) 
#at https://stackoverflow.com/questions/65480967/how-can-i-display-five-rows-of-data-based-on-user-in-python