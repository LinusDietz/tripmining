Filters:

Checkin Density - 

    <img src="https://render.githubusercontent.com/render/math?math=e^{i \pi} = -1">

##### Test Data
 
    Test data is consisted of two units
    1. trips - contains the information of a trip
    2. traveler - created within a test combining a set of timely ordered trips 
    
###### Adding new trip
    Test data consists of a set of single trips. Each trip should be included within a yaml file named as 
    <unique_name>.yml. The <unique_name> of the trip should also be incoded in the file as the name. Please
    refer the existing trip files for reference.
    
###### Adding new traveler
    A new travler is created combining a timely ordered set of trips. These trips must be happnded in a sequence with 
    the minumus interval of 10 days between the trips. The traverl is created within a test by providing the set of
    trip as a list
    
    From: test_filters.py test script
    ex: selected_trips = ["trip1", "trip2", "trip3", "trip4"]



##### Running a single test set

Execute following shell command in the `qualitymeasurements` folder

   `$ pytest <test_case_name>.py`

##### Running all tests

Execute following shell command in the `qualitymeasurements` folder

   `$ pytest`