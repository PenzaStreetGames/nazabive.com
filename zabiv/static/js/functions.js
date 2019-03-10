var SITENAME = "http://127.0.0.1:8080/";


function initBaseUI() {
    let left_content = document.querySelector("#left_content");
    let main_content = document.querySelector("#main_content");
    left_content.style.height = getComputedStyle(main_content).height;

}

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
    if (!xmlhttp && typeof XMLHttpRequest != 'undefined') {
        xmlhttp = new XMLHttpRequest();
    }
    return xmlhttp;
}

function like(element, post_id) {
    var xmlhttp = getXmlHttp();
    xmlhttp.open('POST', SITENAME + 'like', true);
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send("post_id=" + encodeURIComponent(post_id));
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4) {
            if (xmlhttp.status == 200) {
                if (xmlhttp.responseText)
                    data = element.children[0].src;
                if (data == SITENAME + "static/images/like.png") {
                    element.children[0].src = "/static/images/like2.png";
                    element.children[1].innerText = "0";
                } else {
                    element.children[0].src = "/static/images/like.png";
                    element.children[1].innerText = "1";
                }

            }
        }
    };
}


function setFriend(element, user) {
    var xmlhttp = getXmlHttp();
    xmlhttp.open('POST', SITENAME + 'setfriend', true);
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send("user=" + encodeURIComponent(user));
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4) {
            if (xmlhttp.status == 200) {
                if (xmlhttp.responseText) {
                    d1 = "Удалить из друзей";
                    d2 = "Добавить в друзья";
                    if (element.innerText == d1) {
                        element.innerText = d2;
                    } else {
                        element.innerText = d1;
                    }
                }
            }
        }
    };
}

function sendMessage(dialog) {
    message = document.querySelector("#message")
    var xmlhttp = getXmlHttp();
    xmlhttp.open('POST', SITENAME + 'send_message', true);
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send("message=" + encodeURIComponent(message.value) + "&" + "dialog=" + encodeURIComponent(dialog));
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4) {
            if (xmlhttp.status == 200) {
                if (xmlhttp.responseText) {
                    message.value = "";
                }
            }
        }
    };
}


initBaseUI();
