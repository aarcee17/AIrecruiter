const fs = require('fs');
const gs = require('github-scraper');

const username = 'iteles';

gs(username, function(err, data) {
    if (err) {
        console.error('Error:', err);
    } else {
        fs.writeFileSync('github_data.json', JSON.stringify(data));
        console.log('Data written to github_data.json');
    }
});
