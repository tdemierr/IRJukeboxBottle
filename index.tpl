<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Jukebox</title>
       
       <script  language="JavaScript">
$(function() {
  $("#uploadform").on("submit", function(e) {
    e.preventDefault();

    $.ajax({
      url: '/uploadEmpData',
      type: 'POST',
      data: $('#uploadform').serialize(),
      dataType: 'json',
      success: function(data) {
        console.log(data);
        alert('file uploaded successfully');
      },
      error: function(data) {
        alert('upload fail');
        //console.log(error);
      }
    });
  });
});

	   var ok=0;
	   strChoix = "";
	   var Choix=0;
		strLecture = "";
		var Lecture = 0;
	function GetArduinoIO()
		{
			nocache = "&nocache=" + Math.random() * 1000000;
			var request = new XMLHttpRequest();
			request.onreadystatechange = function()
			{
				if (this.readyState == 4) {
					if (this.status == 200) {
						if (this.responseXML != null) {
							// XML file received - contains analog values, switch values and LED states
							Choix = this.responseXML.getElementsByTagName('vinyle')[0].childNodes[0].nodeValue;
							document.Choix.l.selectedIndex=Choix;
							 document.images["pochette"].src='/CoverArt/' + albums[ Choix];
							// get switch inputs
							ok=this.responseXML.getElementsByTagName('switch')[0].childNodes[0].nodeValue;	
							
							if(ok==1)
							{
								document.getElementById("bouton").disabled=false;
								document.getElementById("liste").disabled=false;
								//alert(1);
								
							}
							else
							{
								document.getElementById("bouton").disabled=true;
								document.getElementById("liste").disabled=true;
								//alert(0);
							}
							// LED 3
							if (this.responseXML.getElementsByTagName('lecture')[0].childNodes[0].nodeValue === "ON") {
								document.getElementById("bouton").innerHTML = "Lecture";
								Lecture = 1;
							}
							else {
								document.getElementById("bouton").innerHTML = "Pause";
								Lecture = 0;
							}
							
							
						}
					}
				}
			}
			// send HTTP GET request with LEDs to switch on/off if any
			request.open("GET", "ajax_inputs" + strChoix + strLecture + nocache, true);
			request.send(null);
			setTimeout('GetArduinoIO()', 1000);
			strChoix = "";
			strLecture = "";
		}
		
		
       function getChoix() {
	//album = document.Choix.l.selectedIndex;
	//alert('http://www.amicrade.ch/jukebox/image/' + albums[album] + '.jpg');
	//document.images["pochette"].src='http://www.amicrade.ch/jukebox/image/' + albums[album] + '.jpg';
	strChoix="&Choix="+document.Choix.l.selectedIndex;
}
function GetButton()
		{
			if (Lecture == 1) {
				Lecture = 0;
				strLecture = "&Lecture=0";
			}
			else {
				Lecture = 1;
				strLecture = "&Lecture=1";
			}
		}

</SCRIPT>
    </head>

     <body onLoad="GetArduinoIO()">


	<center>
    <h1>Jukebox</h1> <br />
<form method="post"  id="uploadform" onsubmit="formupload()"  enctype="multipart/form-data">
    <div class="form-group">
        <input type="file" id="exampleInputFile" name="file">
    </div>
    <div class="form-group ">
        <button type="submit" class="btn btn-primary pull-right" id="upload_button">Upload File</button>
    </div>
</form>

    <FORM method=GET NAME="Choix">
      <select name="l" id='liste' onChange="getChoix()" size="1">
        <script language=javascript>
	
	  var albums = new Array("The Skatalites-Walk with me", "The Valkyrians-Punkrocksteady", "Madness-One step beyond","The Offenders-Lucky enough to live","The Rebel Assholes-Split", "The Specials","Derozer-Mondo Perfetto","The Filaments-Land of Lions","Los Fastidios-Rebels'n'Revels","Guerilla Poubelle-Amor Fati", "Death or Glory-Cant Stop me","Maldonne", "Nine Eleven-Le reve de cassandre", "Brixton Robbers-Carved Livers", "Los Fastidios-Live 04", "Jaya the cat-First Beer of a new Day","Sonic Boom six-Rude Awakening","Comeback Kid-Symptoms + cures","The Creepshow-They all fall down","The Skatalites-Foundation Ska","Broadway Calls-Comfort Distraction", "The Specials-More... Or Less 1", "The Specials-More... Or Less 2", "Wank for peace-What will remain", "Brassens - III", "The Peacocks-After All", "Berurier Noir-Viva Bertaga 1", "Berurier Noir-Viva Bertaga 2");

              albums.sort();
			  
   for (var i=0; i<albums.length; i++) {
       document.write("<OPTION value=" + i +">"+albums[i] + "\n");
	   
   }
      </script>
      </select>
   
   <br /> 
     </FORM>


<section id="logo">
                <img  name="pochette" src="" alt="Pochette" height=400px" >
            </section>
             <SCRIPT language=javascript>
            document.images["pochette"].src='';
            </script>
            <br />       
                 <button type="button" id="bouton" onClick="GetButton()">Pause</button><br /><br />
</center>
    </body>
</html>
