module.exports = {
  // feed: require('./feed'),               // activity feed (RSS)
  followers: require('./followers'),     // also scrapes following or stargazers
  issue: require('./issue'),
  // issues: require('./issues'),
  // issues_search: require('./issues_search'),
  // labels : require('./labels'),
  // milestones : require('./milestones'),
  org: require('./org'),
  org_repos: require('./org_repos'),
  people: require('./people'),
  profile: require('./profile'),
  repo: require('./repo'),
  // repos: require('./repos'),
  repos_user: require('./repos_user'),
  // starred: require('./starred')
  stars_watchers: require('./stars_watchers')
}
