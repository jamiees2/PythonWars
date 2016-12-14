var loading = false;

// CodeMirror
var editor = CodeMirror.fromTextArea(document.getElementById('code'), {
    lineNumbers: true,
    value: "def robot():\n#Implement your code here\n",
    mode:  "python"
});


// function called if the code is accepted
function accept_code(data) {
    document.getElementById("loading").style.display = "none";
    document.getElementById("success").style.display = "inline";
    console.log(data);
}

// function called when user clicks the submit button to submit his code
function submit_code(data) {
    document.getElementById("success").style.display = "none";
    document.getElementById("loading").style.display = "inline";
    // timeout to see that it's loading
    setTimeout(function() {
        var code = editor.getValue();
        console.log(code)
        $.ajax({
          type: "POST",
          url: "/submit",
          data: {data: code},
          success: accept_code
        });
    },1000);
}