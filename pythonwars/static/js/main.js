var loading = false;
var level = 1;

// CodeMirror
var editor = CodeMirror.fromTextArea(document.getElementById('code'), {
    lineNumbers: true,
    theme: "mdn-like",
    value: "def robot():\n#Implement your code here\n",
    mode:  "python"
});

var marker = editor.markText({line: 0, ch: 0}, {line: 1}, {readOnly: true});


// function called if the code is accepted
function process_response(data) {
    console.log(data.results);
    $("#spinner").hide();
    $("#code-form").show();
    if(data.success == true) {
      game.state.getCurrentState().run(data.results.moves, data.results.maze, function(){
        if (data.victory)
        {
          $('#finishedModal').openModal();
        }
      });
    } else {
        $(".error").show();
        $(".error").text(data.results)
    }

}

// function called when user clicks the submit button to submit his code
function submit_code(data) {
    $(".error").hide();
    $("#spinner").show();
    $("#code-form").hide();

    // timeout to see that it's loading
    setTimeout(function() {
        var code = editor.getValue();
        $.ajax({
          type: "POST",
          url: "/submit/" + LEVEL,
          data: {data: code},
          success: process_response,
          error: process_response
        });
    },1000);
}

$(function(){
  $(".error").hide();
  $("#spinner").hide();
});
