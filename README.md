# Tripmining — A Python Module for Mining Trips from Check-in Based Data


## Installation

Requires `Python3` with `pip`.

```
pip install git+https://github.com/LinusDietz/tripmining.git@master
```

## Usage

```python
def mine_trips(person):
    checkins = list()
    for raw_checkin in person.checkins:
        checkin_location = Location(raw_checkin['place_id'], Coordinate(raw_checkin['latitude'], raw_checkin['longitude']), raw_checkin['country_code'])
        checkins.append(Checkin(raw_checkin['user_id'], checkin_location, raw_checkin['local_created_at']))

    traveler = Traveler.from_checkins(checkins, 'dataset_identifier', min_duration=5, min_density=0.2)

    print(traveler)
    for trip in traveler.trips:
        print(trip.to_json())
```


## Authors

[Linus Dietz](https://www.cm.in.tum.de/en/research-group/linus-dietz/)
Avradip Sen
Lukas Vorwerk
Leonardo Tonetto
