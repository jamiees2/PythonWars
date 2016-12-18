var loading = false;

// CodeMirror
var editor = CodeMirror.fromTextArea(document.getElementById('code'), {
    lineNumbers: true,
    mode:  "python"
});

var marker = editor.markText({line: 0, ch: 0}, {line: 1}, {readOnly: true});


// function called if the code is accepted
function process_response(data) {
    console.log(data.results);
    if(data.success == true) {
        document.getElementById("loading").style.display = "none";
        document.getElementById("success").style.display = "inline";
        console.log(data.victory);
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
    console.log(level);
    document.getElementById("success").style.display = "none";
    document.getElementById("loading").style.display = "inline";
    // timeout to see that it's loading
    setTimeout(function() {
        var code = editor.getValue();
        console.log(code)
        $.ajax({
          type: "POST",
          url: "/submit/" + LEVEL,
          data: {data: code},
          success: process_response,
          error: process_response
        });
    },1000);
}
