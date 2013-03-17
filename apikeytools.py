import apikeys
import argparse
from datetime import datetime
from canary import app


def main():
    parser = argparse.ArgumentParser(description="API Key Tools")
    subparsers = parser.add_subparsers(title="Operation", description="The operation to perform")
    parser_add = subparsers.add_parser('add', help="Add an API key")
    parser_add.add_argument('key', nargs='?', help="(Optional) The key string to add")
    parser_add.add_argument('restricted', type=int, choices=[0, 1], help="Whether the API key should be restricted to use from one IP")
    parser_add.add_argument('ip', help="The IP from which requests will be made")
    parser_add.add_argument('email', help="An email to associate with the key")
    parser_add.set_defaults(func=add)
    parser_inf = subparsers.add_parser('info', help="Get info about an API key")
    parser_inf.add_argument('field', choices=['key', 'ip', 'email'], help="The field to check")
    parser_inf.add_argument('value', help="The value to check")
    parser_inf.set_defaults(func=info)
    parser_rem = subparsers.add_parser('remove', help="Remove an API key")
    parser_rem.add_argument('key', help="The key to remove")
    parser_rem.set_defaults(func=remove)
    parser_chr = subparsers.add_parser('changerest', help="Change the restriction level of an API key")
    parser_chr.add_argument('key', help="The key to change")
    parser_chr.add_argument('restricted', type=int, choices=[0, 1], help="The new value for whether the API key should be restricted to use from one IP")
    parser_chr.set_defaults(func=changerest)
    args = parser.parse_args()
    with app.test_request_context():
        args.func(args)


def add(args):
    try:
        key = apikeys.makenew(args.restricted, args.ip, args.email, args.key)
    except apikeys.ExistingKeyError:
        print "Error: Key %s exists already." % args.key
        return
    except Exception:
        print "An error occurred."
        return
    print 'Key created: %s' % key


def info(args):
    try:
        if args.field == 'key':
            row = apikeys.getrecord(args.value)
            if not row:
                print "Key %s is not in database." % args.value
                return
            rows = [row]
        elif args.field == 'ip':
            rows = apikeys.getiprecords(args.value)
        elif args.field == 'email':
            rows = apikeys.getemailrecords(args.value)
    except Exception:
        print "An error occurred."
        return
    if len(rows) == 0:
        print "No records matched."
        return
    for row in rows:
        row['isocreated'] = datetime.fromtimestamp(row['created']).isoformat()
        print "Key:%(apikey)s, restricted:%(restricted)s, ip:%(ip)s, email:%(email)s, created:%(isocreated)s" % row


def remove(args):
    try:
        apikeys.removekey(args.key)
    except Exception:
        print "An error occurred."
        return
    print "Successfully deleted key %s" % args.key


def changerest(args):
    try:
        apikeys.changerestricted(args.key, args.restricted)
    except Exception:
        print "An error occurred."
        return
    print "Restriction level for key %s changed if the key existed." % args.key

if __name__ == "__main__":
    main()
