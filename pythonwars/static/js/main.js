var loading = false;

// CodeMirror
var editor = CodeMirror.fromTextArea(document.getElementById('code'), {
    lineNumbers: true,
    value: "def robot():\n#Implement your code here\n",
    mode:  "python"
});


// function called if the code is accepted
function process_response(data) {
    console.log(data.results);
    if(data.success == true) {
        document.getElementById("loading").style.display = "none";
        document.getElementById("success").style.display = "inline";
        $("#error").text('');
        game.state.getCurrentState().run(data.results.moves, data.results.maze);
    } else {
        document.getElementById("loading").style.display = "none";
        //document.getElementById("fail").style.display = "inline";
        $("#error").text(data.results)
        console.log("goes here");
        console.log(data.results);
    }

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
          success: process_response,
          error: process_response
        });
    },1000);
}
