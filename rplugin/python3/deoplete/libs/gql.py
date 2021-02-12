from collections import namedtuple, Counter
import json
import subprocess
import time
import typing

from deoplete.util import Candidates
from pynvim import Nvim


Issue = namedtuple('Issue', ('number', 'title', 'body', 'labels', 'closed'))
Label = namedtuple('Label', ('name',))
Pull = namedtuple('PR', ('number', 'title', 'body', 'labels', 'closed'))
User = namedtuple('User', ('type', 'login', 'name'))


class GitHubCandidatesCreator:
    def __init__(self, vim: Nvim):
        self._GQL_handler = GqlHandler(vim)

    @property
    def user_candidates(self) -> Candidates:
        users = Counter(self._GQL_handler.get_users())
        max_login_length = max(len(user.login) for user in users) if users else None
        return [
            {
                'word': user.login,
                'abbr': '@{0:{width}}{1}'.format(user.login,
                                                 f" - {user.name}" if user.name else '',
                                                 width=max_login_length),
                'kind': user.type,

                # number of comments, issues and PRs sent by the user
                '_sort_key': users[user],

                '_data': user,
            } for user in users
        ]

    @property
    def issue_candidates(self) -> Candidates:
        issues = list(self._GQL_handler.get_issues())
        max_issue_num_digits = len(str(issues[0].number)) if issues else None

        def create_candidate(issue: Issue):
            labels = ' '.join(f"[{label.name}]" for label in issue.labels)
            body = issue.body.replace('\r', '')
            return {
                'word': str(issue.number),
                'abbr': '#{0:<{width}} {1}'.format(
                    issue.number, issue.title, width=max_issue_num_digits),
                'kind': 'Issue',
                'info': f" {labels or ' == No Labels == '} \n{body}",
                '_data': issue,
            }

        return [create_candidate(issue) for issue in issues]

    @property
    def pull_candidates(self) -> Candidates:
        pulls = list(self._GQL_handler.get_pulls())
        max_pull_num_digits = len(str(pulls[0].number)) if pulls else None

        def create_candidate(pull: Pull):
            labels = ' '.join(f"[{label.name}]" for label in pull.labels)
            body = pull.body.replace('\r', '')
            return {
                'word': str(pull.number),
                'abbr': '#{0:<{width}} {1}'.format(
                    pull.number, pull.title, width=max_pull_num_digits),
                'kind': 'PullReq',
                'info': f" {labels or ' == No Labels == '} \n{body}",
                '_data': pull,
            }

        return [create_candidate(pull) for pull in pulls]


class GqlHandler:
    def __init__(self, vim: Nvim):
        self.vim = vim
        buffer = self.vim.current.buffer

        # If the other instances have already hit the api, or are trying to hit now,
        # wait and get the data via vim variable
        if buffer.vars.get('deoplete_gh_is_started'):
            retry = 0
            while not buffer.vars.get('deoplete_gh_data'):
                time.sleep(0.01)
                retry += 1
                if retry > 300:
                    break
            else:
                self.data = json.loads(buffer.vars['deoplete_gh_data'])
                return

        # Tell vim this instance is trying to hit the api
        buffer.vars['deoplete_gh_is_started'] = True

        process = subprocess.run(
            ['gh', 'api', 'graphql', '-F', 'owner=:owner', '-F' 'name=:repo', '-f', '''query=
                query($name: String!, $owner: String!) {
                  repository(owner: $owner, name: $name) {
                    issues(last: 100) {
                      nodes {
                        number
                        title
                        body
                        closed
                        labels (last: 10) {
                          nodes {
                            name
                          }
                        }
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
                    pullRequests(last: 100) {
                      nodes {
                        number
                        title
                        body
                        closed
                        labels (last: 10) {
                          nodes {
                            name
                          }
                        }
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
        self.vim.current.buffer.vars['deoplete_gh_data'] = process.stdout
        self.data = json.loads(process.stdout)

    def get_users(self) -> typing.Generator[User, None, None]:
        if not self.data:
            return
        issues = self.data['data']['repository']['issues']['nodes']
        pulls = self.data['data']['repository']['pullRequests']['nodes']
        for target in issues + pulls:
            author = target['author']
            yield User(type=author['__typename'], login=author['login'], name=author.get('name'))
            for comment in target['comments']['nodes']:
                author = comment['author']
                yield User(type=author['__typename'], login=author['login'], name=author.get('name'))

    def get_issues(self) -> typing.Generator[Issue, None, None]:
        if not self.data:
            return
        issues = self.data['data']['repository']['issues']['nodes']
        for issue in issues:
            labels = [Label(name=n['name']) for n in issue['labels']['nodes']]
            yield Issue(
                number=issue['number'],
                title=issue['title'],
                body=issue['body'],
                labels=labels,
                closed=issue['closed'])

    def get_pulls(self) -> typing.Generator[Pull, None, None]:
        if not self.data:
            return
        pulls = self.data['data']['repository']['pullRequests']['nodes']
        for pull in pulls:
            labels = [Label(name=n['name']) for n in pull['labels']['nodes']]
            yield Pull(
                number=pull['number'],
                title=pull['title'],
                body=pull['body'],
                labels=labels,
                closed=pull['closed'])
