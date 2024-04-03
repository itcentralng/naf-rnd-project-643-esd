from datetime import datetime
from app import app
from app.user.model import User
from app.location.model import Location
from app.command.model import Command

with app.app_context():
    # TO CREATE A USER UNCOMMENT THE NEXT LINE AND RUN THIS FILE
    # User.create('admin@email.com', 'password', 'admin')

    # TO CREATE A LOCATIONS UNCOMMENT THE NEXT 2 LINES AND RUN THIS FILE
    # for i in ['Kano', 'Kaduna', 'Abuja', 'Lagos']:
    #     Location.create(i)
    
    # TO CREATE A COMMANDS UNCOMMENT THE NEXT 2 LINES AND RUN THIS FILE
    # for i in ['Command 1', 'Command 2', 'Command 3']:
    #     Command.create(i)
    print('Ready!')