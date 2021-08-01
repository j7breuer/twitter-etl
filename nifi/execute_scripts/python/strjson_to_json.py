
import json
import java.io
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback

def convert_strlist_list(inpt_json):
    try:
        if inpt_json['extr_hashtags'] == "[]":
            inpt_json['extr_hashtags'] = []
        else:
            inpt_json['extr_hashtags'] = json.loads(inpt_json['extr_hashtags'])
    except:
        pass
    # URL conversion
    try:
        if inpt_json['extr_domain_urls'] == "[]":
            inpt_json['extr_domain_urls'] = []
        else:
            inpt_json['extr_domain_urls'] = json.loads(inpt_json['extr_domain_urls'])
    except:
        pass
    # User Mention conversion
    try:
        if inpt_json['extr_user_mentions'] == "[]":
            inpt_json['extr_user_mentions'] = []
        else:
            inpt_json['extr_user_mentions'] = json.loads(inpt_json['extr_user_mentions'])
    except:
        pass
    return inpt_json

class ModJson(StreamCallback):
    def __init__(self):
        pass

    def process(self, inputStream, outputStream):
        str_ff = IOUtils.toString(inputStream, "UTF-8")
        json_ff = json.loads(str_ff)
        json_ff = convert_strlist_list(json_ff)
        outputStream.write(json.dumps(json_ff, indent=4))


# Begin Script #
flowFile = session.get()

if (flowFile != None):
    try:
        flowFile = session.write(flowFile, ModJson())
        session.transfer(flowFile, REL_SUCCESS)
    except:
        session.transfer(flowFile, REL_FAILURE)

session.commit()