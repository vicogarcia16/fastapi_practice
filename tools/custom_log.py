from fastapi.requests import Request

def log(tag="MyAPI", message="", request: Request = None):
    with open("tools/log.txt", "a+") as log:
        log.write(f"{tag}: {message}\n")
        if request:
            log.write(f"\t{request.url}\n")
        else:
            log.write("\tNo request available\n")