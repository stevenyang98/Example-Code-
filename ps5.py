# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Steven Yang
# Collaborators (discussion): Adam Katz
# Time: 6 hours
# Late days used: 3

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE', 
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2011)
TESTING_INTERVAL = range(2011, 2017)

"""
Begin helper code
"""
class Dataset(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Dataset instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d numpy array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return np.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year {} is not available".format(year)
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by a linear
            regression model
        model: a numpy array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = np.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        degs: a list of integers that correspond to the degree of each polynomial 
            model that will be fit to the data

    Returns:
        a list of numpy arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    np_array = []
    for power in degs: #pretty straightfoward
        np_array.append(np.polyfit(x,y,power))
    return np_array


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models: #separate plot for each model
        model_points = np.polyval(model,x)#evaluates polynomial at each x value
        plt.figure()
        plt.plot(x,y,'bo',label='Measured Points')
        plt.plot(x,model_points,'r',label='Fit') #plotting with label conventions
        plt.xlabel("Year")
        plt.ylabel("Temperature in Celsius")
        degree=str(len(model)-1)#degree one is ax+b, thus len model -1
        R_2 =str(round(r2_score(y,model_points),5)) #using imported function
        ratio = str(round(se_over_slope(x,y,model_points,model),5)) #helper function to get ratio
        if len(model) == 2: #degree one polynomial
            plt.title('Degree of Fit: ' + degree + '\n' + 'R^2: ' + R_2 + '\n' + 'Ratio of Standard Error: '
                        + ratio) #\n to keep clean
        else:
            plt.title('Degree of Fit: ' + degree + '\n' + 'R^2: ' + R_2)
        plt.show()
        
    


def gen_cities_avg(temp, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        temp: instance of Dataset
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a numpy 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    annual_temps=[]
    for year in years:#iterate through number of years
        if year%4==0:
            divisor=366
        else:
            divisor=365
        avg_city = []
        for city in multi_cities:
            temperature = temp.get_yearly_temp(city,year)#get daily temp for the entire year
            avg = sum(temperature)/divisor #temperature is a numpy array
            avg_city.append(avg)
        annual_temps.append(sum(avg_city)/len(avg_city))#for each city average
    return np.array(annual_temps)
    
    

#temp = Dataset("data.csv")
#test_years = np.array(range(1961, 2016))
#yearly_temps = gen_cities_avg(temp, ['PORTLAND'], test_years)
        

#x = np.array(range(50))
#y = np.array(range(0,100,2))       


def find_interval(x, y, length, has_positive_slope):
    """
    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        length: the length of the interval
        has_positive_slope: a boolean whose value specifies whether to look for
            an interval with the most extreme positive slope (True) or the most
            extreme negative slope (False)

    Returns:
        a tuple of the form (i, j) such that the application of linear (deg=1)
        regression to the data in x[i:j], y[i:j] produces the most extreme
        slope and j-i = length.

        In the case of a tie, it returns the most recent interval. For example,
        if the intervals (2,5) and (8,11) both have the same slope, (8,11) should
        be returned.

        If such an interval does not exist, returns None
    """
    best_x = None #two place holders
    most = 0
    for number in range(len(x)-length+1): #x and y have the same length, +1 for one off error
        current = 0
        model = generate_models(x[number:length+number],y[number:length+number],[1]) #arrays that are length length
        if has_positive_slope: #true
            if model[0][0] > 0:
                current = model[0][0]
                if abs(current-most) <= 1e-8 or current > most: #if equal or one is greater
                    most = current
                    best_x = (number, number+length) #update
        else: #false
            if model[0][0] < 0:
                current = model[0][0]
                if abs(current -most) <= 1e-8 or current < most: #if equal or one is less
                    most = current
                    best_x = (number, number+length) #update   
    print("hi,", most)
    return best_x
            

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    total = 0
    for i in range(len(y)): #get every element in each list
        total+=(y[i]-estimated[i])**2#predicted - observed
    RMSE=(total/len(y))**0.5 #formula for RMSE
    return RMSE


def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model's estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models: #separate plot for each model
        model_points = np.polyval(model,x)#evaluates polynomial at each x value
        plt.figure()
        plt.plot(x,y,'bo',label='Measured Points')
        plt.plot(x,model_points,'r',label='Fit') #plotting with label conventions
        plt.xlabel("Year")
        plt.ylabel("Temperature in Celsius")
        degree=str(len(model)-1)#degree one is ax+b, thus len model -1
        RMSE=str(rmse(y,model_points))
        plt.title('Degree of Fit: ' + degree + '\n' + 'RMSE: ' + RMSE)
        plt.show()
        



if __name__ == '__main__':
    pass
    
    data = Dataset("data.csv")#create datset instance

    # Problem 3A
#    x = np.array([i for i in range(1961,2017)])
#    y = []
#    for year in x:
#        y.append(data.get_daily_temp("BOSTON",2,12,year))
#    actual = np.array(y)#make y value in array 
#    model = generate_models(x,actual,[1])
#    evaluate_models_on_training(x,actual,model)
       

    # Problem 3B
#    x = np.array([i for i in range(1961,2017)])
#    y = gen_cities_avg(data,["BOSTON"],x)
#    model = generate_models(x,y,[1])
#    evaluate_models_on_training(x,y,model)

    # Problem 4B
    #increasing
#    x = np.array([i for i in range(1961,2017)])    
#    y = gen_cities_avg(data,["LOS ANGELES"],x)    
#    window = find_interval(x,y,30,True)#find the interval over 30 years  
#    viable_years = window[0]
#    viable_end = window[1]+1
#    actual_x = np.array([i for i in range(viable_years+1961,viable_end+1961)]) #account for scaling the x
#    actual_y = y[viable_years:viable_end]
#    model = generate_models(actual_x,actual_y,[1])
#    evaluate_models_on_training(actual_x,actual_y,model)
    
    #decreasing
#    x = np.array([i for i in range(1961,2017)])
#    y = gen_cities_avg(data,["LOS ANGELES"],x)
#    window = find_interval(x,y,30,False)#find the interval
#    viable_years = window[0]
#    viable_end = window[1]+1 #do plus one so that it is included in the range
#    actual_x = np.array([i for i in range(viable_years+1961,viable_end+1961)])
#    actual_y = y[viable_years:viable_end]
#    model = generate_models(actual_x,actual_y,[1])
#    evaluate_models_on_training(actual_x,actual_y,model)
    
    #national average decreasing
#    x = np.array([i for i in range(1961,2017)])
#    y = gen_cities_avg(data,CITIES,x)
#    longest = (0,0)
#    for i in range(1,56): #upper limit of the interval is 2016-1961+1
#        test = find_interval(x,y,i,False)
#        if test is not None:
#                longest=test  
#    start = longest[0]
#    end = longest[1]+1
#    actual_x = np.array([i for i in range(start+1961,end+1961)])#x starts at 0 for some reason
#    actual_y = y[start:end]
#    model = generate_models(actual_x,actual_y,[1])
#    evaluate_models_on_training(actual_x,actual_y,model)
   
    #overall national
#    x = np.array([i for i in range(1961,2017)])
#    y = gen_cities_avg(data,CITIES,x)    
#    model = generate_models(x,y,[1])
#    evaluate_models_on_training(x,y,model)
            
        
    # Problem 5B
#    x = np.array(TRAINING_INTERVAL)
#    national_average = np.array(gen_cities_avg(data,CITIES,TRAINING_INTERVAL))
#    
#    model = generate_models(x,national_average,[1,2,15])
#    evaluate_models_on_training(x,national_average,model) #straight foward implementation 
#   
    #next part of 5B uncomment separately
    
#    x=np.array(TRAINING_INTERVAL)
#    national_average = np.array(gen_cities_avg(data,CITIES,TRAINING_INTERVAL)) #y based of training data
#    model = generate_models(x,national_average,[1,2,15])
#
#    test_x=np.array(TESTING_INTERVAL)#test
#    test_national_average = np.array(gen_cities_avg(data,CITIES,TESTING_INTERVAL))#testing data
#    evaluate_models_on_testing(test_x,test_national_average,model)#evaluate test on training 
#    
