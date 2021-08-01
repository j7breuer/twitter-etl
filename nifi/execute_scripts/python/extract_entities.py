

import json
import java.io
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback

def extract_entities(inpt_json):
    '''
    inpt:
        inpt_json [dict]:   dict of tweet, does not matter if truncated or not

    oupt:  
        inpt_json [dict]:   dict with up to 3 new keys
                            list of hashtags, urls, and user mentions

    '''
    # Initiate dict for entities/key pairs to extract as lists for flowfile
    list_dict = {
        'urls': 'expanded_url',
        'hashtags': 'text',
        'user_mentions': 'screen_name'
    }

    
    # Alter json for entities if truncated so we always get all the entities
    is_trunc = inpt_json['truncated']    
    if is_trunc == "true":
        test_json = inpt_json['extended_tweet']
    else:
        test_json = inpt_json
    
    # Loop through entities to extract - hashtags/urls/user names
    for i in list(list_dict.keys()):
        
        # Check if there is anything extracted
        if len(test_json['entities'][i]) > 0:
            
            # Initiate list that will go into flowfile json for elasticsearch
            new_ff_json_key = []
            
            # Loop through all entities within that category and add to list
            for j in range(0, len(test_json['entities'][i])):
                new_ff_json_key.append(test_json['entities'][i][j][list_dict[i]])
                
            # Add list extracted entiites to flowfile
            inpt_json['extr_'+i] = new_ff_json_key
            
    return inpt_json

class ModJson(StreamCallback):
    def __init__(self):
        pass

    def process(self, inputStream, outputStream):
        str_ff = IOUtils.toString(inputStream, "UTF-8")
        json_ff = json.loads(str_ff)
        json_ff = extract_entities(json_ff)
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