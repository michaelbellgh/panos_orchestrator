import pan_client

def reboot(panclient: pan_client.PanClient):
    response = panclient.get_xml_response("op", {"cmd" : "<request><restart><system></system></restart></request>"})

def shutdown(panclient: pan_client.PanClient):
    response = panclient.get_xml_response("op", {"cmd" : "<request><shutdown><system></system></shutdown></request>"})

