import urllib2
import json


class AuthError(Exception):
    pass


class NoAuthTokenError(Exception):
    pass


class DataCollectError(Exception):
    pass


def urljoin(base, path):
    return "%s/%s/" % (base.rstrip("/"), path.strip("/"))


class ItemCollector(object):
    def __init__(self, server, user):
        self.server = server
        self.user = user
        self._token = None

    @property
    def token(self):
        if not self._token:
            raise NoAuthTokenError
        return self._token

    def login(self, password):
        request = urllib2.Request(
            urljoin(self.server, "api/auth/"),
            json.dumps({"u": self.user, "p": password}),
            {"Content-Type": "application/json"},
        )
        response = urllib2.urlopen(request)
        if response.code / 10 != 20:
            raise AuthError(response.read())

        result = json.loads(response.read())
        token = result.get("token")
        if not token:
            raise AuthError("token is missed")
        self._token = token

    def collect_item(self, project, item, value):
        data = {
            "auth": self.token, "project": project,
            "item": item, "value": value,
        }
        request = urllib2.Request(
            urljoin(self.server, "api/monitoritems/collector/"),
            json.dumps(data),
            {"Content-Type": "application/json"},
        )
        response = urllib2.urlopen(request)
        if response.code / 10 != 20:
            raise DataCollectError(response.read())

        result = json.loads(response.read())
        if result["ok"] != True:
            raise DataCollectError(result["detail"])
        return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("server", help="server of banbrick")
    parser.add_argument("user", help="user of banbrick")
    parser.add_argument("password", help="password of user")
    parser.add_argument("project", help="project to collect")
    parser.add_argument("item", help="item to collect")
    parser.add_argument("value", help="value to refresh")

    args = parser.parse_args()
    collector = ItemCollector(args.server, args.user)
    try:
        collector.login(args.password)
    except AuthError as err:
        print(err.message)
    try:
        collector.collect_item(args.project, args.item, args.value)
    except DataCollectError as err:
        print(err.message)
    print "ok"