from collections import namedtuple, Counter
from deoplete.util import Candidates
import json
import subprocess
import typing


GitHubUser = namedtuple('GitHubUser', ('type', 'login', 'name'))


def candidates_from_github_users() -> Candidates:
    data = query_GQL()
    counter = Counter(generate_github_users(data))
    width = counter and max(len(user.login) for user in counter)
    return [
        {
            'word': user.login,
            'abbr': '@{0:{width}}{1}'.format(user.login,
                                             f" - {user.name}" if user.name else '',
                                             width=width),
            'kind': user.type,
            '_sort_key': counter[user],
        } for user in counter
    ]


def query_GQL() -> GitHubUser:
    process = subprocess.run(
        ['gh', 'api', 'graphql', '-F', 'owner=:owner', '-F' 'name=:repo', '-f', '''query=
            query($name: String!, $owner: String!) {
              repository(owner: $owner, name: $name) {
                issues(last: 100) {
                  nodes {
                    author {
                      __typename
                      login
                      ... on User {
                        name
                      }
                    }
                    comments(last: 100) {
                      nodes {
                        author {
                          __typename
                          login
                          ... on User {
                            name
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
        '''], capture_output=True)
    if not process.stdout:
        return {}
    return json.loads(process.stdout)


def generate_github_users(data: typing.Dict) -> GitHubUser:
    if not data:
        return
    for issue in data['data']['repository']['issues']['nodes']:
        author = issue['author']
        yield GitHubUser(type=author['__typename'], login=author['login'], name=author['name'])
        for comment in issue['comments']['nodes']:
            author = comment['author']
            yield GitHubUser(type=author['__typename'], login=author['login'], name=author['name'])
