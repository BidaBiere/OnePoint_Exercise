"""Main function, in which classes.py functions access is given through command lines"""

import argparse as ap
import pandas as pd
from classes import (
    Plane, Passenger, allocate_seat, change_seat,show_passengers, show_planes, show_reservation
)

planes_model = pd.read_json("planes_type.json", orient="index")

"""Add command lines"""
parser = ap.ArgumentParser(description="Manage planes and passengers.")
parser.add_argument(
    "--create_flight",
    type=str,
    metavar=("flight_number", "nb_rows", "nb_col"),
    nargs=3,
    dest="create_flight",
    help=
    "Create a flight with : [flight number] [number of rows] [number of columns]",
)
parser.add_argument(
    "--create_plane",
    type=str,
    metavar=("flight_number", "plane_model"),
    nargs=2,
    dest="create_plane",
    help=
    "Create a flight with : [flight number] [plane model]",
)
parser.add_argument(
    "--create_passenger",
    type=str,
    metavar=("full_name"),
    nargs="+",
    dest="create_passenger",
    help=
    "Create a passenger : [name surname]",
)
parser.add_argument(
    "--allocate_seat",
    type=str,
    metavar="flight_number seat full_name [seat full_name...]",
    nargs="+",
    dest="allocate_seat",
    help=
    'Allocate a seat in flight to passenger :' \
    '[flight number] [seat] [name surname] [seat...] [name surname...]',
)
parser.add_argument(
    "--change_seat",
    type=str,
    metavar="flight_number new_seat full_name [new_seat full_name...]",
    nargs="+",
    dest="change_seat",
    help=
    'Change seat in flight to passenger : ' \
    '[flight number] [new seat] [name surname] [new_seat...] [name surname...]',
)
parser.add_argument(
    "--show",
    nargs="+",
    help=
    'Show options : '
    'all (display all dataframes) / ' \
    'planes (display planes, can pass one or several flight numbers as argument) / ' \
    'passengers (display passengers, can pass one or several '\
    'full name as argument as following : "name surname") / ' \
    'reservations (display one or several reservations with flight number ' \
    'and one or several full names as following : "name surname")',
)

#Manage command lines received
args = parser.parse_args()
if args.create_flight:
    Plane(args.create_flight[0], int(args.create_flight[1]), int(args.create_flight[2]))
if args.create_plane:
    if args.create_plane[1] in planes_model.index:
        Plane(
            args.create_plane[0],
            planes_model.at[args.create_plane[1], "rows"],
            planes_model.at[args.create_plane[1], "col"],
        )
if args.create_passenger:
    for element in args.create_passenger:
        Passenger(element.split()[0], element.split()[1])
if args.allocate_seat:
    if len(args.allocate_seat) < 3:
        print("Too few arguments. Need at least 3 : flight_number seat full_name")
    else:
        if len(args.allocate_seat) % 2 != 1:
            print("After flight_number, arguments are required 2 by 2 : seat full_name")
        else:
            for i in range(1, len(args.allocate_seat), 2):
                allocate_seat(
                    args.allocate_seat[0],
                    args.allocate_seat[i],
                    args.allocate_seat[i + 1].split()[0],
                    args.allocate_seat[i + 1].split()[1],
                )
if args.change_seat:
    if len(args.change_seat) < 3:
        print("Too few arguments. Need at least 3 : flight_number seat full_name")
    else:
        if len(args.change_seat) % 2 != 1:
            print("After flight_number, arguments are required 2 by 2 : seat full_name")
        else:
            for i in range(1, len(args.change_seat), 2):
                change_seat(
                    args.change_seat[0],
                    args.change_seat[i],
                    args.change_seat[i + 1].split()[0],
                    args.change_seat[i + 1].split()[1],
                )
if args.show:
    if args.show[0] == "all":
        show_planes()
        show_passengers()
    elif args.show[0] == "planes":
        if len(args.show[0:]) > 1:
            show_planes(args.show[1:])
        else:
            show_planes()
    elif args.show[0] == "passengers":
        if len(args.show[0:]) > 1:
            show_passengers(args.show[1:])
        else:
            show_passengers()
    elif args.show[0] == "reservations":
        if len(args.show[0:]) > 2:
            show_reservation(args.show[1:])
        else:
            print("Error : Too few arguments")
