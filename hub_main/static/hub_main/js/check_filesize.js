function checkFileSize(fileInput) {
    if (fileInput.files.length > 0) {
        const fileSize = fileInput.files[0].size; // in bytes
        const maxSize = 10 * 1024 * 1024;

        const submitBtn = document.getElementById('submit-btn');
        const errorText = document.getElementById('error-text');

        if (fileSize > maxSize) {

            errorText.style.display = 'block';
            submitBtn.disabled = true;

        }

        else {
            errorText.style.display = 'none';
            submitBtn.disabled = false;
        }
        const generateFromLinkBtn = document.getElementById('generate-link');
        generateFromLinkBtn.disabled = true;
    }

    else {
        generateFromLinkBtn.disabled = false;
    }
}

document.addEventListener('DOMContentLoaded', function(){
    let fileInput = document.getElementById('image');

    fileInput.addEventListener('change', function(){
        checkFileSize(fileInput)
    })

    const regexPattern = /https:\/\/github\.com\/([^/]+)\/([^/]+)$/;
    const githubRepoLink = document.getElementById('github_repo_link');

    githubRepoLink.addEventListener('change', function(){
        const match = githubRepoLink.value.match(regexPattern);
        const errorTextGithub = document.getElementById('error-text-github')
        if(!match){
            errorTextGithub.style.display = 'block';
        }
        else {
            errorTextGithub.style.display = 'none';
        }
    })
})