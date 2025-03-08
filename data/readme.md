# Traffic Accident Severity Prediction

## Database Schema
![alt text](image.png)

## Dataset Overview

This project aims to predict the severity of traffic accidents using the French BAAC (Bulletin d'Analyse des Accidents Corporels) dataset. The dataset is split into four main tables, each containing different aspects of traffic accidents.

## Data Description

The dataset consists of four interconnected tables, linked through the accident identifier (`Num_Acc`):

### 1. CARACTERISTIQUES (General Accident Information)

| Variable | Description | Possible Values |
|----------|-------------|-----------------|
| Num_Acc | Unique accident identifier (primary key) | Numeric ID |
| jour | Day of the accident | 1-31 |
| mois | Month of the accident | 1-12 |
| an | Year of the accident | Four-digit year |
| hrmn | Time of the accident (hour and minutes) | HHMM format |
| lum | Lighting conditions | 1 = Daylight<br>2 = Dawn/Dusk<br>3 = Night without street lights<br>4 = Night with street lights off<br>5 = Night with street lights on |
| dep | Department code (INSEE code) | Two-digit codes (including 2A/2B for Corsica) |
| com | Municipality code (INSEE code) | Department code + 3 digits |
| agg | Location | 1 = Outside urban area<br>2 = In urban area |
| int | Intersection type | 1 = Not at intersection<br>2 = X intersection<br>3 = T intersection<br>4 = Y intersection<br>5 = Intersection with more than 4 branches<br>6 = Roundabout<br>7 = Plaza<br>8 = Railroad crossing<br>9 = Other |
| atm | Weather conditions | -1 = Not specified<br>1 = Normal<br>2 = Light rain<br>3 = Heavy rain<br>4 = Snow/Hail<br>5 = Fog/Smoke<br>6 = Strong wind/Storm<br>7 = Dazzling weather<br>8 = Overcast<br>9 = Other |
| col | Collision type | -1 = Not specified<br>1 = Two vehicles - head-on<br>2 = Two vehicles - rear-end<br>3 = Two vehicles - side impact<br>4 = Three or more vehicles - chain collision<br>5 = Three or more vehicles - multiple collisions<br>6 = Other collision<br>7 = No collision |
| adr | Postal address | Text (for accidents in urban areas) |
| lat | Latitude coordinates | Decimal degrees |
| long | Longitude coordinates | Decimal degrees |

### 2. LIEUX (Location Characteristics)

| Variable | Description | Possible Values |
|----------|-------------|-----------------|
| Num_Acc | Accident identifier (foreign key) | Numeric ID |
| catr | Road category | 1 = Highway<br>2 = National road<br>3 = Departmental road<br>4 = Municipal road<br>5 = Off public network<br>6 = Parking lot open to public traffic<br>7 = Urban metropolitan roads<br>9 = Other |
| voie | Road number | Text |
| v1 | Numerical index of the road number | Numeric |
| v2 | Letter index of the road | Text |
| circ | Traffic flow | -1 = Not specified<br>1 = One-way<br>2 = Two-way<br>3 = Separated lanes<br>4 = Variable lanes |
| nbv | Number of traffic lanes | Numeric |
| vosp | Reserved lane | -1 = Not specified<br>0 = Not applicable<br>1 = Bike path<br>2 = Bike lane<br>3 = Reserved lane |
| prof | Road profile | -1 = Not specified<br>1 = Flat<br>2 = Slope<br>3 = Top of hill<br>4 = Bottom of hill |
| pr | Reference point number | Numeric (-1 if not specified) |
| pr1 | Distance in meters to reference point | Numeric (-1 if not specified) |
| plan | Road layout | -1 = Not specified<br>1 = Straight section<br>2 = Left curve<br>3 = Right curve<br>4 = "S" curve |
| lartpc | Width of the central reservation (median) in meters | Numeric |
| larrout | Road width in meters | Numeric |
| surf | Road surface condition | -1 = Not specified<br>1 = Normal<br>2 = Wet<br>3 = Puddles<br>4 = Flooded<br>5 = Snow-covered<br>6 = Mud<br>7 = Ice<br>8 = Oily<br>9 = Other |
| infra | Infrastructure | -1 = Not specified<br>0 = None<br>1 = Underground/Tunnel<br>2 = Bridge/Overpass<br>3 = Interchange ramp<br>4 = Railroad<br>5 = Developed intersection<br>6 = Pedestrian zone<br>7 = Toll zone<br>8 = Construction site<br>9 = Other |
| situ | Accident location | -1 = Not specified<br>0 = None<br>1 = On roadway<br>2 = On emergency lane<br>3 = On shoulder<br>4 = On sidewalk<br>5 = On bike path<br>6 = On other special lane<br>8 = Other |
| vma | Maximum authorized speed | Numeric (km/h) |

### 3. VEHICULES (Vehicle Information)

| Variable | Description | Possible Values |
|----------|-------------|-----------------|
| Num_Acc | Accident identifier (foreign key) | Numeric ID |
| id_vehicule | Unique vehicle identifier | Numeric code |
| num_veh | Vehicle identifier | Alphanumeric code |
| senc | Direction of travel | -1 = Not specified<br>0 = Unknown<br>1 = Increasing address/reference<br>2 = Decreasing address/reference<br>3 = No reference |
| catv | Vehicle category | 00 = Indeterminable<br>01 = Bicycle<br>02 = Moped < 50cc<br>03 = Quadricycle with motor (light car)<br>07 = Passenger car<br>10 = Light utility vehicle<br>13 = Heavy goods vehicle (3.5T-7.5T)<br>14 = Heavy goods vehicle (>7.5T)<br>15 = Heavy goods vehicle with trailer<br>16 = Road tractor alone<br>17 = Road tractor with semi-trailer<br>20 = Special equipment vehicle<br>21 = Agricultural tractor<br>30 = Scooter < 50cc<br>31 = Motorcycle > 50cc and ≤ 125cc<br>32 = Scooter > 50cc and ≤ 125cc<br>33 = Motorcycle > 125cc<br>34 = Scooter > 125cc<br>35 = Light quad ≤ 50cc<br>36 = Heavy quad > 50cc<br>37 = Bus<br>38 = Coach<br>39 = Train<br>40 = Tram<br>41 = 3-wheeled vehicle ≤ 50cc<br>42 = 3-wheeled vehicle > 50cc and ≤ 125cc<br>43 = 3-wheeled vehicle > 125cc<br>50 = Powered personal mobility device<br>60 = Non-powered personal mobility device<br>80 = Electric bicycle<br>99 = Other |
| obs | Fixed obstacle hit | -1 = Not specified<br>0 = Not applicable<br>1 = Parked vehicle<br>2 = Tree<br>3 = Metal guardrail<br>5 = Other guardrail<br>6 = Building/Wall/Bridge pier<br>7 = Vertical signage support or emergency call box<br>8 = Post<br>9 = Urban furniture<br>10 = Parapet<br>11 = Island/Refuge/Raised marker<br>12 = Curb<br>13 = Ditch/Embankment/Rock face<br>14 = Other fixed obstacle on roadway<br>15 = Other fixed obstacle on sidewalk or shoulder<br>16 = Road departure without obstacle<br>17 = Pipe - culvert head |
| obsm | Mobile obstacle hit | -1 = Not specified<br>0 = None<br>1 = Pedestrian<br>2 = Vehicle<br>4 = Rail vehicle<br>5 = Domestic animal<br>6 = Wild animal<br>9 = Other |
| choc | Initial impact point | -1 = Not specified<br>0 = None<br>1 = Front<br>2 = Front right<br>3 = Front left<br>4 = Rear<br>5 = Rear right<br>6 = Rear left<br>7 = Right side<br>8 = Left side<br>9 = Multiple impacts (rollover) |
| manv | Main maneuver before the accident | -1 = Not specified<br>0 = Unknown<br>1 = No change in direction<br>2 = Same direction, same lane<br>3 = Between two lanes<br>4 = Reversing<br>5 = Wrong way<br>6 = Crossing the median<br>7 = In bus lane, same direction<br>8 = In bus lane, opposite direction<br>9 = Entering traffic<br>10 = Making a U-turn<br>11 = Changing lanes to the left<br>13 = Veering to the left<br>14 = Veering to the right<br>15 = Turning left<br>16 = Turning right<br>17 = Overtaking on the left<br>18 = Overtaking on the right<br>19 = Crossing the roadway<br>20 = Parking maneuver<br>21 = Avoidance maneuver<br>22 = Door opening<br>23 = Stopped (not parking)<br>24 = Parked (with occupants)<br>25 = Driving on sidewalk<br>26 = Other maneuvers |
| motor | Vehicle engine type | -1 = Not specified<br>0 = Unknown<br>1 = Hydrocarbon<br>2 = Hybrid electric<br>3 = Electric<br>4 = Hydrogen<br>5 = Human-powered<br>6 = Other |
| occutc | Number of occupants in public transport | Numeric |

### 4. USAGERS (User/Victim Information)

| Variable | Description | Possible Values |
|----------|-------------|-----------------|
| Num_Acc | Accident identifier (foreign key) | Numeric ID |
| id_usager | Unique user identifier | Numeric code |
| id_vehicule | Vehicle identifier | Numeric code |
| num_veh | Vehicle identifier | Alphanumeric code |
| place | Position in the vehicle | 1-9 = Specific seat positions<br>10 = Pedestrian |
| catu | User category | 1 = Driver<br>2 = Passenger<br>3 = Pedestrian |
| **grav** | **Injury severity - TARGET VARIABLE** | **1 = Unharmed<br>2 = Killed<br>3 = Hospitalized injured<br>4 = Slight injury** |
| sexe | Gender | 1 = Male<br>2 = Female |
| an_nais | Year of birth | Four-digit year |
| trajet | Purpose of trip | -1 = Not specified<br>0 = Not specified<br>1 = Home-work commute<br>2 = Home-school commute<br>3 = Shopping<br>4 = Professional<br>5 = Leisure/Entertainment<br>9 = Other |
| secu1, secu2, secu3 | Safety equipment used | -1 = Not specified<br>0 = No equipment<br>1 = Seatbelt<br>2 = Helmet<br>3 = Children's device<br>4 = Reflective vest<br>5 = Airbag (2/3-wheeled motors)<br>6 = Gloves (2/3-wheeled motors)<br>7 = Gloves + Airbag (2/3-wheeled motors)<br>8 = Not determinable<br>9 = Other |
| locp | Pedestrian location | -1 = Not specified<br>0 = Not applicable<br>1 = More than 50m from crosswalk<br>2 = Less than 50m from crosswalk<br>3 = On crosswalk without traffic signals<br>4 = On crosswalk with traffic signals<br>5 = On sidewalk<br>6 = On shoulder<br>7 = On refuge or emergency lane<br>8 = On service road<br>9 = Unknown |
| actp | Pedestrian action | -1 = Not specified<br>0 = Not specified or not applicable<br>1 = Moving in same direction as vehicle<br>2 = Moving in opposite direction of vehicle<br>3 = Crossing<br>4 = Hidden<br>5 = Playing/Running<br>6 = With animal<br>9 = Other<br>A = Entering/exiting vehicle<br>B = Unknown |
| etatp | Pedestrian status | -1 = Not specified<br>1 = Alone<br>2 = Accompanied<br>3 = In group |

## Target Variable Definition

The target variable for this prediction task is `grav` (injury severity), which has four classes:
- 1 = Unharmed
- 2 = Killed
- 3 = Hospitalized injured
- 4 = Slight injury

