from datetime import datetime
from app import app
from app.user.model import User
from app.location.model import Location
from app.command.model import Command

with app.app_context():
    # User.create('admin@email.com', 'password', 'admin')
    # for i in ['Kano', 'Kaduna', 'Abuja', 'Lagos']:
    #     Location.create(i)
    
    # for i in ['Command 1', 'Command 2', 'Command 3']:
    #     Command.create(i)
    print('Ready!')