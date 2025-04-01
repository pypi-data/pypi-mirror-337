
import json


def getJsonResponse(success, mensaje, data):
    jsonObject = {"result":{"successful":success,"message": mensaje, "data":data}}
    return json.dumps(jsonObject)