def log(tag="", message=""):
    with open("tools/log.txt", "w+") as log:
        log.write(f"{tag}: {message}\n")