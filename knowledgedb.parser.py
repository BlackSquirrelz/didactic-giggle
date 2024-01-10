import sqlite3
import argparse
import os, sys
import subprocess

# Create a backup of the Knowledge DB file
def create_backup(file_path, user=None):
    knowledge_db_path = file_path
    try:
        if not user:
            backup_path = os.path.join(os.curdir, "knowledgeC.db.backup")
        else:
            backup_path = os.path.join(os.curdir, f"{user}_knowledgeC.db.backup")
        print(backup_path)
        print(f"Creating a backup of the Knowledge DB file at {backup_path}")
        command = f"sudo rsync -avE '{knowledge_db_path}' '{backup_path}'"
        subprocess.run(command, shell=True)
        return backup_path
    except Exception as e:
        print(f"Error creating a backup of the Knowledge DB file: {e}")
        exit(0)
    

def get_working_database():
    # Get a list of all the users on the system
    users = os.listdir("/Users")
    ignore_list = ['.localized', 'Shared', 'Guest', 'root', 'daemon', 'nobody', 'www']

    list_of_backups = []

    # Check if the user passed a file path
    if not args.file:
        print("No file path passed, default to own knowledge DB file")
        # Create a backup of the file
        for user in users:
            if user in ignore_list:
                continue
            if os.path.exists(f"/Users/{user}/Library/Application Support/Knowledge/knowledgeC.db"):
                knowledge_db_path = f"/Users/{user}/Library/Application Support/Knowledge/knowledgeC.db"
                print(f"Found knowledge DB file at {knowledge_db_path}")
                list_of_backups.append(create_backup(knowledge_db_path))
                break
            else:
                print(f"Could not find knowledge DB file at /Users/{user}/Library/Application Support/Knowledge/knowledgeC.db")
                continue
    else:
        knowledge_db_path = args.file
        list_of_backups.append(create_backup(knowledge_db_path))
    
    return list_of_backups

# Parse the IOS Knowledge DB file
def ios_parser(db):
    pass
    
# Parse the MacOS Knowledge DB file   
def macos_parser(db):
    print("[+] Parsing MacOS Knowledge DB file")
    # Connect to the database
    c, conn = database_connect(db)
    # Query the database
    query = "SELECT * FROM ZOBJECT;"
    results = query_database(c, conn, query)
    print(results)
    

# Connect to any database
def database_connect(db):
    c, conn = sqlite3.connect(db)
    return c, conn

# Query the database and return the results
def query_database(c, conn, query):
    c.execute(query)
    conn.commit()
    return c.fetchall()


if __name__=="__main__":
    print("This is the parser module.")

    # Check if the user is root
    if not os.geteuid() == 0:
        print("You need to run this script as root. Exiting...")
        exit(0)

    # Parse the arguments supplied by the user
    # -i for IOS (either)
    # -m for MacOS (or)
    # -o for output path (optional)
    # -f for file path to the Knowledge DB file
    
    argparser = argparse.ArgumentParser(description="KnowledgeDB parser")
    argparser.add_argument("-i", "--ios", help="Parse IOS Knowledge DB file")
    argparser.add_argument("-o", "--output", help="Output path for the parsed file")
    argparser.add_argument("-m", "--macos", action="store_true", help="Parse MacOS Knowledge DB file")
    argparser.add_argument("-f", "--file", help="Path to the Knowledge DB file")

    args = argparser.parse_args()

    working_databases = get_working_database()

    if args.ios:
        for db in working_databases:
            ios_parser(db)
    elif args.macos:
        for db in working_databases:
            macos_parser(db)
    elif args.ios and args.macos:
        print("Both iOS and macOS arguments passed. Exiting...")
        exit(0)
    else:
        print("No arguments passed. Exiting...")
        exit(0)





    

