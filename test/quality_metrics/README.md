This folder contains tests for trip checkin quality metrics. These quality metrics can be used to exclude trips with 
low quality checkin information.

There are 2 test sets in the folder

   1.  **test_quality_metrics** - Consists of tests to check the correctness of the metric implementations
   2.  **test_filters** - Consists of tests to check the functionality of the filters mentioned below.

### Filters:

  Trips can be filtered using following filters. 

 1.  ##### Checkin Density -

     **<img src="https://render.githubusercontent.com/render/math?math=Checkin-density = \frac{days\: with\: check-in}{days}">**
     
     Range : 0(low quality) - 1(high quality). The default value of this metric is 0.2. 
     Refer : https://mediatum.ub.tum.de/doc/1428242/1428242.pdf
     
 2.  ##### Inter Streak Days -
   
     **<img src="https://render.githubusercontent.com/render/math?math=Inter\:Streak\:Days = \frac{\sum_{i=1}^{number \, of\, streaks -1} Last\,Date_{streak_i} - First \, Date_{streak_{i+1}}}{maximum\: possible\: unchecked\: days}">**
     
     Range : 0(high quality) - 1(low quality)

 3. ##### Checkin Discontinuity -

     **<img src="https://render.githubusercontent.com/render/math?math=Check-in\:discontinuity\:= \frac{number \:of\: streaks -1 }{maximum\: possible\: number\: of\: streaks - 1}">**
     
     Range : 0(high quality) - 1(low quality)
     
 4. ##### Maximum Speed of transitions -
 
     **<img src="https://render.githubusercontent.com/render/math?math=Max\: speed = Max\{speed\: of\: transitions\}">**
     
     Range : 0 - infinity
     
     This metric can be used to check the plausibility of a trip. Trips with maximum transition speed > max air speed 
     (1500 km/h - Reference: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0148913) are considered 
     as implausible trips.
     
 5. ##### Duration of the trip

      **<img src="https://render.githubusercontent.com/render/math?math=Duration = {last chekin\: date - first\: checkin\: date}">**
      
     Range : 2 - infinity

#### How to apply filters to exclude trips

Apply the appropriate threshold values for aforementioned filters while mining trips from a given checkin streak. 

**Example**:

        Traveler.from_checkins(traveler_checkins,
                               'twitter',
                               min_duration=7,
                               min_density=0.2,
                               max_inter_streak_days=0.4,
                               max_speed=1500,
                               max_checkin_discontinuity=0.3)
                               
**Explanation**: This threshold setting will filter out trips which has
              `duration is less than 7 days` and
              `checking density is less than 0.2` and
              `inter streak days value is greater than 0.4` and
              `maximum transition speed is greater than 1500 km/h` and 
              `checking discontinuity value is greater than 0.3`
              
              
##### Test Data
 
   Test data is constructed based on two concepts
   
   1. trip - contains the information of a trip 
   2. traveler - created within a test combining a set of timely ordered trips 
    

###### Adding new trip
   Test data consists of a set of single trips. Each trip should be included within a yaml file named as 
   <unique_name>.yml. The <unique_name> of the trip should also be included in the file as the name. Please
   refer the existing trip files for reference. 
    
###### Adding new traveler
   A new traveler is created combining a timely ordered set of trips. These trips must take place in a sequence with 
   the minimum interval of 10 days between the trips. The traveler is created within a test by providing the set of trip 
   as a list
    
   (Reference : test_filters.py test script)
   
   ex: 
   
       selected_trips = ["trip1", "trip2", "trip3", "trip4"]
       trips = [load_trip(trip) for trip in selected_individual_trips]
       traveler_checkins = prepare_traveler_from_raw_data(trips)


### Running Tests

Execute the following shell command in the `root` folder

   `$ pytest`