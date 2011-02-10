function DispMagicEmot(MagicID,H,W){
  MagicFaceUrl = "happychristmas/wp-christmas.swf";
  document.getElementById("MagicFace").innerHTML = '<OBJECT codeBase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=4,0,2,0" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="' + W + '" height="' + H + '"><PARAM NAME=movie VALUE="'+ MagicFaceUrl +'"><param name=menu value=false><PARAM NAME=quality VALUE=high><PARAM NAME=play VALUE=false><param name="wmode" value="transparent"><embed src="' + MagicFaceUrl +'" quality="high" pluginspage="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash"; type="application/x-shockwave-flash" wmode="transparent" width="' + W + '" height="' + H + '"></embed>';
  //document.getElementById("MagicFace").style.top = (document.body.scrollTop+((document.body.clientHeight-300)/2))+"px";
  //document.getElementById("MagicFace").style.left = (document.body.scrollLeft+((document.body.clientWidth-480)/2))+"px";
  document.getElementById("MagicFace").style.top = (window.screen.availHeight-300)/2+"px";
  document.getElementById("MagicFace").style.left = (window.screen.availWidth-480)/2+"px"; 
  document.getElementById("MagicFace").style.visibility = 'visible';
  MagicID += Math.random();
  setTimeout("document.getElementById('MagicFace').style.visibility = 'hidden'",10000);
  NowMeID = MagicID;
}
DispMagicEmot(144,350,500);