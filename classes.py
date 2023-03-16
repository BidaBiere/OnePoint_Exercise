"""Create planes / passengers classes and related methods"""
import pandas as pd
import numpy as np

planeCols = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]
try:
    passengers_df = pd.read_csv("passengers.csv")
except:
    passengers_df = pd.DataFrame(
        {
            "name": [None],
            "surname": [None],
            "flightNumber": [None],
            "seat": [None],
        }
    )
try:
    planes_df = pd.read_csv("planes.csv")
except:
    planes_df = pd.DataFrame(
        {
            "seats": [None],
            "available": [None],
            "passenger": [None],
            "flightNumber": [None],
        }
    )


# Class definition
class Plane:
    """Class plane"""

    # Create plane and add to dataframe
    def __init__(self, flight_number, row, col):
        """Creator"""
        global planes_df
        self.flight_number = flight_number
        self.row = row
        self.col = col
        temp = []
        for i in range(row * col):
            temp.append(planeCols[i - (i // col) * col] + str(i // col))
        data = {"seats": temp}
        self.seats = pd.DataFrame(data)
        self.seats["available"] = True
        self.seats["passenger"] = None
        # Add plane to dataframe. If already exists, replace it.
        if not (planes_df.loc[planes_df["flightNumber"] == self.flight_number].empty):
            planes_df = planes_df.loc[planes_df["flightNumber"] != self.flight_number]
        planes_df = pd.concat([planes_df, self.access_plane()], ignore_index=True)
        planes_df.to_csv("planes.csv", index=False)

    def access_plane(self):
        """Create a dataframe of the plane"""
        copy_plane = self.seats
        copy_plane["flightNumber"] = self.flight_number
        return copy_plane


class Passenger:
    """Class passenger"""

    def __init__(self, name, surname):
        """Creator"""
        global passengers_df
        self.name = name
        self.surname = surname
        self.flights = []
        self.seats = []
        if not (
            passengers_df.loc[
                (passengers_df["name"] == self.name)
                & (passengers_df["surname"] == self.surname)
            ].empty
        ):
            passengers_df = passengers_df.loc[
                (passengers_df["name"] != self.name)
                & (passengers_df["surname"] != self.surname)
            ]
        passengers_df = pd.concat(
            [passengers_df, self.access_passenger()], ignore_index=True
        )
        passengers_df.to_csv("passengers.csv", index=False)

    def access_passenger(self):
        """Create a dataframe of the passenger"""
        data = pd.DataFrame()
        if self.flights:
            for i in range(len(self.flights)):
                flight_data = pd.DataFrame(
                    {
                        "name": [self.name],
                        "surname": [self.surname],
                        "flightNumber": [self.flights[i]],
                        "seat": [self.seats[i]],
                    }
                )
                data = pd.concat([data, flight_data], ignore_index=True)
        else:
            data = pd.DataFrame(
                {
                    "name": [self.name],
                    "surname": [self.surname],
                    "flightNumber": [None],
                    "seat": [None],
                }
            )
        return data


# Global functions
def show_planes(info=[]):
    """Display dataframe of one or all planes"""
    if info != []:
        data = pd.DataFrame()
        for element in info:
            data = pd.concat(
                [data, planes_df.loc[planes_df["flightNumber"] == element]]
            )
        print(data)
    else:
        print(planes_df)


def show_passengers(info=[]):
    """Display dataframe of one or all passengers"""
    if info != []:
        data = pd.DataFrame()
        for element in info:
            data = pd.concat(
                [
                    data,
                    passengers_df.loc[
                        (passengers_df["name"] == element.split()[0])
                        & (passengers_df["surname"] == element.split()[1])
                    ],
                ]
            )
        print(data)
    else:
        print(passengers_df)


def show_reservation(info=[]):
    """Display"""
    if info != []:
        data = pd.DataFrame()
        data_flight = passengers_df.loc[(passengers_df["flightNumber"] == info[0])]
        for element in info[1:]:
            data = pd.concat(
                [
                    data,
                    data_flight.loc[
                        (data_flight["name"] == element.split()[0])
                        & (data_flight["surname"] == element.split()[1])
                    ],
                ]
            )
        print(data)
    else:
        print(passengers_df)


def allocate_seat(flight_number, seat, name, surname):
    """Gives a seat to a passenger, if seat's free and passenger hasn't already a seat"""
    global planes_df
    global passengers_df
    try:
        full_name = f"{name} {surname}"
        if planes_df.isin([flight_number]).any().any():
            # Check if passenger hasn't a seat already in this plane
            if (
                planes_df.loc[(planes_df["flightNumber"] == flight_number)]
                .isin([full_name])
                .any()
                .any()
            ):
                print(
                    f"Passenger {full_name} already has a seat in this flight ({flight_number})"
                )
            else:
                # Check if seat is available
                if (
                    planes_df.loc[
                        (planes_df["seats"] == seat)
                        & (planes_df["flightNumber"] == flight_number),
                        "available",
                    ].values[0]
                    == True
                ):
                    # Update planes_df to include passenger to plane
                    planes_df.loc[
                        (planes_df["flightNumber"] == flight_number)
                        & (planes_df["seats"] == seat),
                        "passenger",
                    ] = full_name
                    planes_df.loc[
                        (planes_df["flightNumber"] == flight_number)
                        & (planes_df["seats"] == seat),
                        "available",
                    ] = False
                    # If passenger doesn't exists, create it
                    if not (passengers_df.isin([name]).any().any()) & (
                        passengers_df.isin([surname]).any().any()
                    ):
                        Passenger(name, surname)
                        print(f"Passenger {name} {surname} created.")
                    # Update passengers_df to include flight number and seat to passenger
                    if pd.isnull(
                        passengers_df.loc[
                            (passengers_df["name"] == name)
                            & (passengers_df["surname"] == surname),
                            "flightNumber",
                        ].values
                    ):
                        # If passenger has no flight infos, fill it with new reservation
                        passengers_df.loc[
                            (passengers_df["name"] == name)
                            & (passengers_df["surname"] == surname),
                            "flightNumber",
                        ] = flight_number
                        passengers_df.loc[
                            (passengers_df["name"] == name)
                            & (passengers_df["surname"] == surname),
                            "seat",
                        ] = seat
                    else:
                        # If passenger already has a reservation on 
                        # another plane, create a new one for this plane
                        new_resa = passengers_df.loc[
                            (passengers_df["name"] == name)
                            & (passengers_df["surname"] == surname)
                        ]
                        new_resa["flightNumber"] = flight_number
                        new_resa["seat"] = seat
                        passengers_df = pd.concat([passengers_df, new_resa])
                    print(
                        f"Seat {seat} attributed to passenger {full_name} in flight {flight_number}"
                    )
                    # Update .csv files
                    planes_df.to_csv("planes.csv", index=False)
                    passengers_df.to_csv("passengers.csv", index=False)
                else:
                    print(
                        f"Seat {seat} of flight {flight_number} is not available. Already taken by {planes_df.loc[planes_df['seats']==seat, 'passenger'].values[0]}."
                    )
        else:
            print(
                f"Plane {flight_number} doesn't exists. Create plane with option create_plane."
            )
    except IndexError:
        print("IndexError : check if flight / seat / passenger exist.")
    except:
        print("ERROR")


def change_seat(flight_number, new_seat, name, surname):
    """Change the seat of a passenger in a given plane"""
    global planes_df
    global passengers_df
    full_name = f"{name} {surname}"
    # Check if passenger already has a seat in this plane
    if (
        planes_df.loc[(planes_df["flightNumber"] == flight_number)]
        .isin([full_name])
        .any()
        .any()
    ):
        # Check if seat is available
        if (
            planes_df.loc[
                (planes_df["seats"] == new_seat)
                & (planes_df["flightNumber"] == flight_number),
                "available",
            ].values[0]
            == True
        ):
            print(f"Change seat of {full_name} in flight {flight_number} to {new_seat}")
            planes_df.loc[
                (planes_df["flightNumber"] == flight_number)
                & (planes_df["passenger"] == full_name),
                "available",
            ] = True
            planes_df.loc[
                (planes_df["flightNumber"] == flight_number)
                & (planes_df["passenger"] == full_name),
                "passenger",
            ] = np.nan
            passengers_df.drop(
                index=passengers_df.loc[
                    (passengers_df["flightNumber"] == flight_number)
                    & (passengers_df["name"] == name)
                    & (passengers_df["surname"] == surname)
                ].index.values[0],
                inplace=True,
            )
            passengers_df = passengers_df.reset_index(drop=True)
            allocate_seat(flight_number, new_seat, name, surname)
        else:
            print(
                f"Seat {new_seat} of flight {flight_number} is not available. Already taken by {planes_df.loc[planes_df['seats']==new_seat, 'passenger'].values[0]}."
            )

    else:
        print(
            f"Passenger {name} {surname} has no reservation in flight {flight_number}"
        )
