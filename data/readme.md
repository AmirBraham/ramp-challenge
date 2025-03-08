# Traffic Accident Severity Prediction

## Dataset Overview

This project aims to predict the severity of traffic accidents using the French BAAC (Bulletin d'Analyse des Accidents Corporels) dataset. The dataset is split into four main tables, each containing different aspects of traffic accidents.

## Database Schema
![alt text](image.png)


## Data Description

The dataset consists of four interconnected tables, linked through the accident identifier (`Num_Acc`):

### 1. CARACTERISTIQUES (General Accident Information)

| Variable     | Description                                                      |
|--------------|------------------------------------------------------------------|
| `Num_Acc`    | Unique accident identifier (primary key)                        |
| `jour`       | Day of the accident                                             |
| `mois`       | Month of the accident                                           |
| `an`         | Year of the accident                                            |
| `hrmn`       | Time of the accident (hour and minutes)                         |
| `lum`        | Lighting conditions (1=Daylight, 2=Dawn/Dusk, etc.)             |
| `dep`        | Department code (INSEE code)                                     |
| `com`        | Municipality code (INSEE code)                                  |
| `agg`        | Location (1=Outside urban area, 2=In urban area)               |
| `int`        | Intersection type (1=Not at intersection, 2-9=Various intersection types) |
| `atm`        | Weather conditions (1=Normal, 2=Light rain, etc.)               |
| `col`        | Collision type (1=Head-on collision, 2=Rear-end collision, etc.)  |
| `adr`        | Postal address (filled in for accidents in urban areas)         |
| `lat`        | Latitude coordinates                                            |
| `long`       | Longitude coordinates                                          |

### 2. LIEUX (Location Characteristics)

| Variable     | Description                                                      |
|--------------|------------------------------------------------------------------|
| `Num_Acc`    | Accident identifier (foreign key)                               |
| `catr`       | Road category (1=Highway, 2=National road, etc.)                  |
| `voie`       | Road number                                                      |
| `v1`, `v2`   | Additional road identifiers                                      |
| `circ`       | Traffic flow (1=One-way, 2=Two-way, etc.)                        |
| `nbv`        | Number of traffic lanes                                         |
| `vosp`       | Reserved lane indicator (1=Bike path, etc.)                      |
| `prof`       | Road profile (1=Flat, 2=Slope, etc.)                            |
| `pr`, `pr1`  | Reference points on the road                                     |
| `plan`       | Road layout (1=Straight section, etc.)                           |
| `lartpc`     | Width of the central reservation (median) in meters             |
| `larrout`    | Road width in meters                                            |
| `surf`       | Road surface condition (1=Normal, 2=Wet, etc.)                  |
| `infra`      | Infrastructure (1=Tunnel, 2=Bridge, etc.)                        |
| `situ`       | Accident location (1=On roadway, etc.)                          |
| `vma`        | Maximum authorized speed at the time and place of the accident  |

### 3. VEHICULES (Vehicle Information)

| Variable     | Description                                                      |
|--------------|------------------------------------------------------------------|
| `Num_Acc`    | Accident identifier (foreign key)                               |
| `id_vehicule`| Unique vehicle identifier (numeric code)                         |
| `num_veh`    | Vehicle identifier (alphanumeric code)                          |
| `senc`       | Direction of travel (1=Increasing address/reference, etc.)       |
| `catv`       | Vehicle category (00=Indeterminable, 01=Bicycle, etc.)          |
| `obs`        | Fixed obstacle hit (1=Parked vehicle, etc.)                     |
| `obsm`       | Mobile obstacle hit (1=Pedestrian, etc.)                        |
| `choc`       | Initial impact point (1=Front, etc.)                            |
| `manv`       | Main maneuver before the accident (1=No change in direction, etc.) |
| `motor`      | Vehicle engine type (1=Hydrocarbon, etc.)                       |
| `occutc`     | Number of occupants in public transport                         |

### 4. USAGERS (User/Victim Information)

| Variable     | Description                                                      |
|--------------|------------------------------------------------------------------|
| `Num_Acc`    | Accident identifier (foreign key)                               |
| `id_usager`  | Unique user identifier                                           |
| `id_vehicule`| Vehicle identifier                                                |
| `num_veh`    | Vehicle identifier (alphanumeric)                               |
| `place`      | Position in the vehicle                                          |
| `catu`       | User category (1=Driver, 2=Passenger, etc.)                      |
| `grav`       | Injury severity (1=Unharmed, 2=Killed, etc.) - TARGET VARIABLE  |
| `sexe`       | Gender (1=Male, 2=Female)                                        |
| `an_nais`    | Year of birth                                                   |
| `trajet`     | Purpose of trip (1=Home-work commute, etc.)                     |
| `secu1`, `secu2`, `secu3` | Safety equipment used (1=Seatbelt, etc.)                         |
| `locp`       | Pedestrian location (1=More than 50m from crosswalk, etc.)       |
| `actp`       | Pedestrian action (1=Moving in same direction as vehicle, etc.)   |
| `etatp`      | Pedestrian status (1=Alone, etc.)                               |

## Target Variable Definition

The target variable for this prediction task is `grav` (injury severity), which has four classes:

- 1 = Unharmed
- 2 = Killed
- 3 = Hospitalized injured
- 4 = Slight injury
