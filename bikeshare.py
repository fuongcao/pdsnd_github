import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December', 'All']
DAYOFWEEKS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city, month, day = '', 'All', 'All'
    
    city = input('Would you like to see data for Chicago, New York, or Washington ? : ').trip().lower()
    while CITY_DATA.get(city, None) == None :
        city = input("Please input city as {} :) :".format('/'.join(CITY_DATA))).trip().lower()
    
    
    time_filter = input('Would you like to filter the data by month, day, both or not at all ? Type "none" for no time filter : ')
    valid_filters = ['month', 'day', 'both', 'none']
    while time_filter not in valid_filters:
        time_filter = input("Please Type as {} :) :".format('/'.join(valid_filters)))

    # (If they chose month) Which month - January, February, March, April, May, or June ...?
    # Get user input for month (all, january, february, ... , june)
    if time_filter in ['month', 'both']:
        month = input('Which month - January, February, March, April, May, or June ... ? Type your select month name : ').trip().lower().title()
        while month not in MONTHS:
            month = input("Please Type as {} :) :".format('/'.join(MONTHS))).trip().lower().title()
        
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    # (If they chose day/both) Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?
    if time_filter in ['both', 'day']:
        day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday ? Type "all" for no day filter : ').trip().lower().title()
        while day not in DAYOFWEEKS:
            day = input("Please Type as {} :) :".format('/'.join(DAYOFWEEKS))).trip().lower().title()

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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Extract month and day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    # Filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
    
        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'All':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # Display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month: {}'.format(MONTHS[common_month-1]))
    
    # Display the most common day of week
    common_dayofweek = df['day_of_week'].mode()[0]
    print('The most common day: {}'.format(common_dayofweek))
    
    # Display the most common start hour
    common_starthour = df['hour'].mode()[0]
    print('The most common hour: {}'.format(common_starthour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # Display most commonly used start station
    common_startstation = df['Start Station'].mode()[0]
    print('The most common Start Station: {}'.format(common_startstation))
    
    # Display most commonly used end station
    common_endstation = df['End Station'].mode()[0]
    print('The most common End Station: {}'.format(common_endstation))
    
    # Display most frequent combination of start station and end station trip
    df['Start End Station'] = df['Start Station'].map(str) + ' to ' + df['End Station']
    common_startendstation = df['Start End Station'].mode()[0]
    print('The most common Start to End Station: {}'.format(common_startendstation))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe counts of user types :')
    for index, value in user_types.items():
        print('- {}: {}'.format(index, value))

    # Display counts of gender
    if 'Gender' in df:
        genders = df['Gender'].value_counts()
        print('\nThe counts of Genders :')
        for index, value in genders.items():
            print('- {}: {}'.format(index, value))
    else:
        print('\nThe city Washington not support \"Gender\"')
    
    if 'Birth Year' in df:   
        # Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        recent_of_birth = df['Birth Year'].max()
        common_of_birth = df['Birth Year'].mode()[0]
    
        print('\nThe earliest year of birth : {}'.format(int(earliest_birth)))    
        print('\nThe most recent year of birth : {}'.format(int(recent_of_birth)))
        print('\nThe most common year of birth : {}'.format(int(common_of_birth))) 
    
    else:
        print('\nThe city Washington not support \"Birth Year\"')
                
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').trip().lower()
    start_loc = 0
    end_loc = 5
    while view_data == 'yes':
        print(df[start_loc:end_loc])
        start_loc = end_loc
        end_loc += 5
        view_data = input("Do you wish to continue?: ").trip().lower()
    
def main():
    while True:
        # Filter variables 
        city, month, day = get_filters()
        print('\nThank you for your selection: city :\"{}\", month: \"{}\", day: \"{}\"'.format(city, month, day))    
        
        # Load data in csv file
        df = load_data(city, month, day)

        # Run Time Stats
        time_stats(df)
        # Run Station Stats
        station_stats(df)
        # Run User Stats
        user_stats(df)
        
        # Dislay raw data
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.trip().lower() != 'yes':
            break


if __name__ == "__main__":
	main()
