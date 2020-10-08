import pan_client

class SecurityPolicyObject:
    #Initial supported objects - to add profiles, device, logging etc
    object_types = [
        "from",
        "to",
        "source",
        "destination",
        "user",
        "application",
        "category",
        "action",
        "tag",
        "service"
    ]

    policy_object_type = ""
    policy_object_value = ""

    def __init__(self, object_type_value, value):
        if object_type_value not in self.object_types:
            raise Exception("Must be one of the following object types: " + ", ".join(self.object_types))

        self.policy_object_type = object_type_value
        self.policy_object_value = value


def add_object_to_security_policy(panclient : pan_client.PanClient, object_type : SecurityPolicyObject, policy_name : str, device_group=None, pre_or_post="post", vsys="vsys1"):
    if device_group != None:
        security_policy_xpath_root = "/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='" + device_group + "']/" + pre_or_post + "-rulebase/security/rules/"
    else:
        security_policy_xpath_root = "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='" + vsys +"']/rulebase/security/rules/"
    
    security_policy_xpath_root += "entry[@name='" + policy_name + "']"
    element = ""

    #The following types are a simple <member> list - we can process them the same
    if object_type.policy_object_type in ("from", "to", "source", "destination", "user", "application", "category", "tag", "service"):
        #Xpath corresponds exactly to object_types values - important to keep them the same
        security_policy_xpath_root += "/"+ object_type.policy_object_type
        if isinstance(object_type, list):
            for obj in object_type:
                element += "<member>" + obj.policy_object_value + "</member>"
        elif isinstance(object_type, SecurityPolicyObject):
            element += "<member>" + object_type.policy_object_value + "</member>"

    panclient.get_xml_response("config", {"action" : "set", "xpath" : security_policy_xpath_root, "element" : element})
        
