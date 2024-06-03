const gs = require('github-scraper');

const usernames = process.argv.slice(2);

if (usernames.length === 0) {
  console.error('Please provide at least one GitHub username.');
  process.exit(1);
}

usernames.forEach((username, index) => {
  const userUrl = username; 
  gs(userUrl, function(err, userData) {
    if (err) {
      console.error(`Error fetching user data for ${username}:`, err);
    } else {
      console.log(JSON.stringify({ username: username, user: userData }));
    }
  });

  const reposUrl = `${username}?tab=repositories`;
  gs(reposUrl, function(err, reposData) {
    if (err) {
      console.error(`Error fetching repositories data for ${username}:`, err);
    } else {
      console.log(JSON.stringify({ username: username, repos: reposData }));
    }
  });
});
