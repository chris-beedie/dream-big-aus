from pathlib import Path

from db import Db
from gdrive import GoogleDrive
from hivebrite import get_token, update_user
from settings import settings
from rich.console import Console
from rich.table import Table
from rich.live import Live

db = Db(settings.db_path)
gdrive = GoogleDrive()

## prep db
# db.create_db()
#db.load_users(settings.user_list_path)

# get new token
#get_token()

## find and replace to remove google drive url to id
# /view?usp=drive_link
# https://drive.google.com/file/d/
# https://drive.google.com/open?id=
# wrong link 259310 - 1EYyhOnOMgCoGL4h17mr1bGoXuuXTU0gg

table = Table(title="Dream Big Australia Upload")

table.add_column("User ID", style="cyan", no_wrap=True)
table.add_column("First Name", style="magenta")
table.add_column("Surname", style="magenta")
table.add_column("CV", style="green")
table.add_column("Headshot", style="green")
table.add_column("Uploaded", style="green")

console = Console()


with Live(table, refresh_per_second=1) as live:  # update 4 times a second to feel fluid

    for user in db.get_users():

        live.console.print(f"Processing {user.user_id} - {user.first_name} {user.last_name}")

        if not user.complete:

            base_path = settings.get_year_path(user.year)

            # download files
            if user.cv_id and not user.cv_path:
                cv_path = gdrive.get_file(user.cv_id, base_path=base_path)
                user.cv_path = str(cv_path)
                db.commit()

            if user.hs_id and not user.hs_path:
                hs_path = gdrive.get_file(user.hs_id, base_path=base_path)
                user.hs_path = str(hs_path)
                db.commit()

            cv_path = None
            hs_path = None

            if user.cv_path and not user.cv_loaded:
                cv_path = Path(user.cv_path)
                if not cv_path.exists():
                    raise KeyError(f"CV not found for: {user.user_id}")
                
            if user.hs_path and not user.hs_loaded:
                hs_path = Path(user.hs_path)
                if not hs_path.exists():
                    raise KeyError(f"Headshot not found for: {user.user_id}")


            if cv_path or hs_path:
                success = update_user(user.user_id, cv_path, hs_path)

                if cv_path and success:
                    user.cv_loaded = True

                if hs_path and success: 
                    user.hs_loaded = True

            if (not user.cv_id or user.cv_loaded) and (not user.hs_id or user.hs_loaded):
                user.complete = True    

            
            table.add_row(str(user.user_id), user.first_name, user.last_name, str(bool(cv_path)), str(bool(hs_path)), str(success))
            db.commit()
