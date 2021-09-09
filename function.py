#####################
# extract_id function
#####################
def extract_id(elem):
    try:
        target = elem.find("a", attrs={"class": "title"})
        return target['id']
    except:
        return 'Nothing_found'
