import pan_client, argparse, credentials
import policies, request

panclient = None

def process_policy_args(args):
    if args.action == "add":
        spo = policies.SecurityPolicyObject(args.object_type,args.object_value)
        policies.add_object_to_security_policy(panclient, spo, args.policy_name, device_group=args.device_group, pre_or_post=args.rulebase, vsys=args.vsys)

def process_commit_args(args):
    if args.device_group_name is not None:
        panclient.push_device_groups(args.device_group_name, include_template=not args.exclude_template,merge_with_candidate_config=not args.no_merge_candidate, validate_only=args.validate_only)

def process_request_args(args):
    if args.action == "reboot":
        request.reboot(panclient)
    if args.action = "shutdown":
        request.shutdown(panclient)

    

def main():
    global panclient
    panclient = pan_client.PanClient(credentials.hostname, credentials.username, credentials.password)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.add_argument("--commit", choices=["normal", "force"])
    parser.add_argument("--commit-partial-user")


    policy_group = subparsers.add_parser('policy')
    commit_group = subparsers.add_parser('commit')
    request_group = subparsers.add_parser('request')

    subparsers = policy_group.add_subparsers()
    security_group = subparsers.add_parser("security")
    security_group.add_argument("--device-group", default=None)
    security_group.add_argument("--rulebase", choices=["pre", "post"], default=None)
    security_group.add_argument("--vsys", default="vsys1")

    subparsers = security_group.add_subparsers()
    security_group_object = subparsers.add_parser("objects")
    security_group_object.add_argument("action", choices=["add"])
    security_group_object.add_argument("policy_name")
    security_group_object.add_argument("object_type", choices=policies.SecurityPolicyObject.object_types)
    security_group_object.add_argument("object_value")
    security_group_object.set_defaults(func=process_policy_args)

    subparsers = commit_group.add_subparsers()
    commit_group_object = subparsers.add_parser("device-group")
    commit_group_object.add_argument("device_group_name", metavar="device-group-name")
    commit_group_object.add_argument("--exclude-template", action="store_true")
    commit_group_object.add_argument("--no-merge-candidate", action="store_true")
    commit_group_object.add_argument("--validate-only", action="store_true")
    commit_group_object.set_defaults(func=process_commit_args)

    commit_group_object = subparsers.add_parser("local")
    commit_group_object.add_argument("--validate-only", action="store_true")
    commit_group_object.set_defaults(func=process_commit_args)

    subparsers = request_group.add_subparsers()
    power_group = subparsers.add_parser("power")
    power_group.add_argument("action", choices=["reboot", "poweroff"])
    power_group.set_defaults(func=process_request_args)


    args = parser.parse_args()
    args.func(args)

    if args.commit in ("normal", "force"):
        partial_user = args.commit_partial_user if args.commit_partial_user is not None else ""
        panclient.commit(force=args.commit == "force", partial_admin_commit=partial_user)

main()