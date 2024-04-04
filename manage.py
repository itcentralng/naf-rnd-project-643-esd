from datetime import datetime
from app import app, db
from app.user.model import User
from app.location.model import Location
from app.command.model import Command
from app.vehicle.model import Vehicleallocation
from app.vehiclelog.model import Vehiclelog

with app.app_context():

    # TO CLEAR ALL LOGBOOK UNCOMMENT NEXT LINE AND RUN THIS FILE
    Vehiclelog.query.delete()

    # TO CREATE A USER UNCOMMENT THE NEXT LINE AND RUN THIS FILE
    try:
        User.create('admin@email.com', 'password', 'admin')
    except:
        pass

    # TO CREATE A LOCATIONS UNCOMMENT THE NEXT 2 LINES AND RUN THIS FILE
    Location.query.delete()
    for i in [
        "Makurdi",
        "Bauchi",
        "Yenagoa",
        "Enugu",
        "Port Harcourt",
        "Kainji",
        "Yola",
        "Ilorin",
        "Maiduguri",
        "Sokoto",
        "Calabar"
        ]:
        Location.create(i)
    
    # TO CREATE A COMMANDS UNCOMMENT THE NEXT 2 LINES AND RUN THIS FILE
    Command.query.delete()
    for i in [
        "Direct Reporting Units (DRUs)",
        "Tactical Air Command (TAC)",
        "Special Operations Command (SOC)",
        "Mobility Command (MC)",
        "Air Training Command (ATC)",
        "Ground Training Command (GTC)",
        "Logistics Command (LC)"
    ]:
        Command.create(i)
    print('Ready!')