def readJSON(file):
        with open(file, "r") as read_file:
                data = json.load(read_file)
        return data
    
def writeJSON(data, file):
    with open(file, "w") as write_file:
            json.dump(data, write_file, indent=4)
    return True