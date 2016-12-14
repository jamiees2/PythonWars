

var editor = CodeMirror.fromTextArea(document.getElementById('code'), {
    lineNumbers: true,
    value: "def robot():\n#Implement your code here\n",
    mode:  "python"
});
$('#code').data('CodeMirrorInstance', editor);
var myInstance = $('code').data('CodeMirrorInstance');