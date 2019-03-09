var SITENAME = "http://127.0.0.1:8080/";

function getXmlHttp() {
	var xmlhttp;
	try {
		xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
	} catch (e) {
		try {
			xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
		} catch (E) {
			xmlhttp = false;
		}
	}
	if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
		xmlhttp = new XMLHttpRequest();
	}
	return xmlhttp;
}

function like(element) {
	var xmlhttp = getXmlHttp();
	xmlhttp.open('POST', SITENAME + 'like', true);
	xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xmlhttp.send("id=" + encodeURIComponent(1));
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4) {
			if(xmlhttp.status == 200) {
				if (xmlhttp.responseText)
				    element.children[0].src="/static/images/like.png";
				    element.children[1].innerText = "asdf";

			}
		}
	};
}
