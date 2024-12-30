document.addEventListener("DOMContentLoaded",()=>{
    const editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/python");

    const runButton = document.getElementById("runButton");
    const outputElement = document.getElementById("output");

    runButton.addEventListener("click",()=>{
        const code = editor.getValue();
        fetch("/ide/run_code",{
            method: "POST",
            headers:{
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({code})
        })
        .then(response => response.json())
        .then(data => {
            outputElement.textContent = data.output;
        })
        .catch(err => {
            outputElement.textContent = `Error: ${err}`;
    });
});
    function getCSRFToken() {
        const cookieValue = document.cookie.split(';').find(row=>row.startsWith('csrftoken'))?.split('=')[1]
        return cookieValue || '';
    }
});