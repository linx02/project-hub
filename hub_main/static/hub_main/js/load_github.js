document.addEventListener('DOMContentLoaded', function(){

    const regexPattern = /https:\/\/github\.com\/([^/]+)\/([^/]+)$/;

    const match = githubRepoLink.match(regexPattern);
    let githubUsername;
    let repo;

    if (match) {
        githubUsername = match[1];
        repo = match[2];
      } else {
        console.log('Invalid GitHub URL');
      }

    const path = 'README.md';
    const githubApiUrl = `https://api.github.com/repos/${githubUsername}/${repo}/contents/${path}`;

    fetch(githubApiUrl)
        .then((response) => response.json())
        .then((data) => {

            const content = atob(data.content);

            let readmeDiv = document.querySelector('.project-readme');
            let contentElement = document.createElement('pre');

            contentElement.innerHTML = content;
            readmeDiv.appendChild(contentElement);

        })
        .catch((error) => {
            let readmeDiv = document.querySelector('.project-readme');
            let contentElement = document.createElement('p');

            contentElement.innerHTML = 'Readme.md not available';
            readmeDiv.appendChild(contentElement);
        });
    

});