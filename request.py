import pan_client

def reboot(panclient: pan_client.PanClient):
    try:
        response = panclient.get_xml_response("op", {"cmd" : "<request><restart><system></system></restart></request>"})
    except Exception as e:
        #All good - we rebooted here so it will time out
        pass
    


def shutdown(panclient: pan_client.PanClient):
    try:
        response = panclient.get_xml_response("op", {"cmd" : "<request><shutdown><system></system></shutdown></request>"})
    except Exception as e:
        #All good - we rebooted here so it will time out
        pass

