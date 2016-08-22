<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />

<script type="text/javascript">
var xmlhttp;
// Are we using a modern browser or ...
if (window.XMLHttpRequest) {
  // code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
} else {
  // code for IE6, IE5
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
}
// This will render the two output which substitute the
// elements id="raw" and id="forin"
function GetItems()
{
  if (xmlhttp.readyState==4 && xmlhttp.status==200) {
    // var jsonobj = eval ("(" + xmlhttp.responseText + ")"); 
    var jsonobj = JSON.parse(xmlhttp.responseText); 
    var output = xmlhttp.responseText;
    document.getElementById("raw").innerHTML = output;
    output = "";
    for (i in jsonobj) {
      output += '<p>';
      output += i + " : " + jsonobj[i];
      output += '</p>';
    }
    document.getElementById("forin").innerHTML = output;
  } else {
    alert("data not available");
  }
}
// xmlhttp.onreadystatechange = GetArticles;
// the GetItems function will be triggered once the ajax
// request is terminated.
xmlhttp.onload = GetItems;
// send the request in an async way
xmlhttp.open("GET", "/getallitems.json", true);
xmlhttp.send();
</script>
<script type="text/javascript"
  src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<script type="text/javascript">
  var $SCRIPT_ROOT = "{{ request.script_name }}";
</script>

<script type="text/javascript">
  $(function() {
    var submit_form = function(e) {
      $.getJSON($SCRIPT_ROOT + '_add_numbers', {
        a: $('input[name="a"]').val(),
        b: $('input[name="b"]').val()
      }, function(data) {
        $('#result').text(data.result);
        $('input[name=a]').focus().select();
      });
      return false;
    };

    $('a#calculate').bind('click', submit_form);

    $('input[type=text]').bind('keydown', function(e) {
      if (e.keyCode == 13) {
        submit_form(e);
      }
    });

    $('input[name=a]').focus();
  });
</script>

</head>
<h1>jQuery Example</h1>
<p>

  <input type="text" size="5" name="a"> +
  <input type="text" size="5" name="b"> =
  <span id="result">?</span>
<p><a href=# id="calculate">calculate server side</a>
<body>
  <p>The raw result from the ajax json request is:</p>
  <div id="raw"></div>
  <br />
  <p>The for cycle produces :</p>
  <div id="forin"></div>
</body>
</html>