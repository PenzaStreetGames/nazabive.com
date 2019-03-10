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

String.prototype.format = String.prototype.f = function () {
    var args = arguments;
    return this.replace(/\{\{|\}\}|\{(\d+)\}/g, function (m, n) {
        if (m == "{{") { return "{"; }
        if (m == "}}") { return "}"; }
        return args[n];
    });
};

function updateMessages(dialog) {
    let area = document.querySelector("#dialog-area")
    var xmlhttp = getXmlHttp();
    xmlhttp.open('POST', SITENAME + 'update_messages', true);
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send("dialog=" + encodeURIComponent(dialog));
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4) {
            if (xmlhttp.status == 200) {
                if (xmlhttp.responseText) {
                    area.innerHTML = ""
                    result  = JSON.parse(xmlhttp.responseText);
                    for (var i = 0; i < result["message_number"]; i++) {
                        block = '<div class="pt-3 pb-2"> <div class="row ml-0"><div class="col-1"><img src="/{0}" alt="1" class="avatar"/></div><div class="col-9 p-0"><p class="h6">{1}</p><div class="row ml-1"><p class="small mt-1">{2} </p></div></div><div class="col-2">{3}</div></div></div>'
                        block = block.format(result["avatars"][i], result["names"][i], result["messages_text"][i], result["messages_date"][i])
                        area.innerHTML += block
                    }
                }
            }
        }
    };
    initBaseUI();
}


initBaseUI();
