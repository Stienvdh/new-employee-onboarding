var pages = {
  "Start": "provision-user.html",
  "Collaboration": "provision-collab.html",
  "Network Access": "provision-NA.html",
  "Security": "provision-SEC.html",
  "Done": "provision-Status.html"
};

var BASE = '../../'

function sayHello() {
  var collab = JSON.parse(localStorage.getItem("products-collab"));
  var na = JSON.parse(localStorage.getItem("products-na"));
  var sec = JSON.parse(localStorage.getItem("products-sec"));

  fetch(BASE + '/hello-webex', {
    method: "post",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "products-collab": JSON.stringify(collab),
      "products-na": JSON.stringify(na),
      "products-sec": JSON.stringify(sec),
      "user" : JSON.stringify(JSON.parse(localStorage.getItem("current-user"))),
      "user-items" : JSON.stringify(JSON.parse(localStorage.getItem("current-user-items")))
    })
  }).then(function (text) {
      return text.json();
  }).then(function (body) {
      console.log(body);
  });
}

function getUser() {
    document.getElementById("user").textContent = JSON.parse(localStorage.getItem("current-user"));
}

function startProvisioning() {
    var users = document.getElementById("users").children;
    var i=0;
    var selectedUser = "";
    var selectedUser = {};
    for (i = 0; i < users.length; i++){
        if (users[i].classList.contains("active")) {
            var u = users[i];
            selectedUser = u.children[0].textContent + " " + u.children[1].textContent;
            selectedUserItems = {
              "fname" : u.children[0].textContent,
              "lname" : u.children[1].textContent,
              "email" : u.children[2].textContent,
              "phone" : u.children[3].textContent,
            }
        }
    }
    localStorage.setItem("current-user", JSON.stringify(selectedUser));
    localStorage.setItem("current-user-items", JSON.stringify(selectedUserItems));
}

function deprovisionUser() {
    var user = JSON.parse(localStorage.getItem("current-user"));
    var userItems = JSON.parse(localStorage.getItem("current-user-items"));

    fetch(BASE + '/deprovision-user', {
      method: "post",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "user-name" : JSON.stringify(user),
        "user-items" : JSON.stringify(userItems)
      })
    }).then(function (text) {
        return text.json();
    }).then(function (body) {
        console.log(body);
    });
}

function startPipeline() {
    var boxes = document.getElementById("checkboxes").children;
    var i=0;
    var domains = [];
    for (i = 0; i < boxes.length; i++){
        if (boxes[i].getElementsByTagName('input')[0].checked) {
            domains.push(boxes[i].getElementsByClassName('checkbox__label')[0].textContent);
        }
    }

    var done = [];
    localStorage.setItem("domains-todo", JSON.stringify(domains));
    localStorage.setItem("domains-done", JSON.stringify(done));

    localStorage.setItem("products-collab", JSON.stringify([]));
    localStorage.setItem("products-na", JSON.stringify([]));
    localStorage.setItem("products-sec", JSON.stringify([]));

    if (domains.length == 0) {
      document.getElementById("pipeline-continue").href = pages["Done"];
    }
    else {
      document.getElementById("pipeline-continue").href = pages[domains[0]];
    }
  }

function checkProducts() {
    var current = JSON.parse(localStorage.getItem("domains-todo"))[0];
    var products = [];

    console.log(current);

    // Get selected products
    switch(current) {
      case "Collaboration":
        products = JSON.parse(localStorage.getItem("products-collab"));
        break;
      case "Network Access":
        products = JSON.parse(localStorage.getItem("products-na"));
        break;
      case "Security":
        products = JSON.parse(localStorage.getItem("products-sec"));
        break;
      default:
    }

    console.log(JSON.parse(localStorage.getItem("products-collab")));
    console.log(JSON.parse(localStorage.getItem("products-na")));
    console.log(JSON.parse(localStorage.getItem("products-sec")));

    // Check boxes
    var boxes = document.getElementById("checkboxes").children;
    var i=0;
    for (i = 0; i < boxes.length; i++){
      if (products.includes(boxes[i].getElementsByClassName('checkbox__label')[0].textContent)) {
          boxes[i].getElementsByTagName('input')[0].classList.add('checked');
          boxes[i].getElementsByTagName('input')[0].checked = true;
      }
    }

    console.log(JSON.parse(localStorage.getItem("current-user")));
}

function continuePipeline() {
    var done = JSON.parse(localStorage.getItem("domains-done"));
    var todo = JSON.parse(localStorage.getItem("domains-todo"));
    var current = todo[0];

    // Get selected products
    var boxes = document.getElementById("checkboxes").children;
    var i=0;
    var products = [];
    for (i = 0; i < boxes.length; i++){
        if (boxes[i].getElementsByTagName('input')[0].checked) {
            products.push(boxes[i].getElementsByClassName('checkbox__label')[0].textContent);
        }
    }

    // Set selected products in localStorage
    switch(current) {
      case "Collaboration":
        localStorage.setItem("products-collab", JSON.stringify(products));
        localStorage.setItem("mac-phone", JSON.stringify(document.getElementById("mac-input").value));
        localStorage.setItem("model-phone", JSON.stringify(document.getElementById("model-input").value));
        break;
      case "Network Access":
        localStorage.setItem("products-na", JSON.stringify(products));
        break;
      case "Security":
        localStorage.setItem("products-sec", JSON.stringify(products));
        break;
      default:
    }

    // Dynamic jumping, based on selected domains
    var new_done = [todo[0]].concat(done);
    localStorage.setItem("domains-done", JSON.stringify(new_done));
    if (todo.length == 1) {
      localStorage.setItem("domains-todo", JSON.stringify([]));
      document.getElementById("pipeline-continue").href = pages["Done"];
    }
    else {
      localStorage.setItem("domains-todo", JSON.stringify(todo.slice(1)));
      document.getElementById("pipeline-continue").href = pages[todo[1]];
    }
  }

function backPipeline() {
    var done = JSON.parse(localStorage.getItem("domains-done"));
    var todo = JSON.parse(localStorage.getItem("domains-todo"));

    // Get selected products
    var boxes = document.getElementById("checkboxes").children;
    var i=0;
    var products = [];
    for (i = 0; i < boxes.length; i++){
        if (boxes[i].getElementsByTagName('input')[0].checked) {
            products.push(boxes[i].getElementsByClassName('checkbox__label')[0].textContent);
        }
    }

    // Set selected products in localStorage
    switch(todo[0]) {
      case "Collaboration":
        localStorage.setItem("products-collab", JSON.stringify(products));
        break;
      case "Network Access":
        localStorage.setItem("products-na", JSON.stringify(products));
        break;
      case "Security":
        localStorage.setItem("products-sec", JSON.stringify(products));
        break;
      default:
    }

    // Dynamic jumping, based on selected domains
    localStorage.setItem("domains-done", JSON.stringify(done));
    if (done.length == 0) {
      document.getElementById("pipeline-back").href = pages["Start"];
    }
    else {
      localStorage.setItem("domains-todo", JSON.stringify([done[0]].concat(todo)));
      localStorage.setItem("domains-done", JSON.stringify(done.slice(1)));
      document.getElementById("pipeline-back").href = pages[done[0]];
    }
  }

function checkDomain() {
    var boxes = document.getElementById("checkboxes").children;
    var i=0;
    var checked = false;
    for (i = 0; i < boxes.length; i++){
        if (boxes[i].getElementsByTagName('input')[0].checked) {
            checked = true;
        }
    }
    if (checked) {
      document.getElementById("pipeline-continue").classList.remove('disabled');
    }
    else {
      document.getElementById("pipeline-continue").classList.add('disabled');
    }
}

function displayStatus() {
    document.getElementById('collab-products').textContent = "Selected services: " + JSON.parse(localStorage.getItem("products-collab")) + "\r\n";
    document.getElementById('na-products').textContent = "Selected services: " + JSON.parse(localStorage.getItem("products-na")) + "\r\n";
    document.getElementById('sec-products').textContent = "Selected services: " + JSON.parse(localStorage.getItem("products-sec")) + "\r\n";
}

function addMember(){
  // Get selected products
  var products = JSON.parse(localStorage.getItem("products-collab"))
  
  fetch(BASE + '/provision-user', {
    method: "post",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "products-selected": JSON.stringify(products),
      "user" : JSON.stringify(localStorage.getItem("current-user-items"))
    })
  }).then(function (text) {
      return text.json();
  }).then(function (body) {
      console.log(body);
      localStorage.setItem("user-list", body)
  });
}

function getUsers(){
  fetch(BASE + '/list-users', {
    method: "get",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  }).then(function (text) {
      return text.json();
  }).then(function (body) {
      console.log("list of users:");
      console.log(body);
      localStorage.setItem('azure-list', JSON.stringify(body));

      var table = document.getElementById('users')
  
      for (var i = 0; i < body.length; i++){
            var row = `<tr>
                    <td>${body[i].fname}</td>
                    <td>${body[i].lname}</td>
                    <td>${body[i].email}</td>
                    <td>${body[i].mobilephone}</td>
                  </tr>`
            table.innerHTML += row
          }
  });
  // var testObject = [{ 'fname': 'Mohamed', 'lname':'El Refaay', 'email': 'm.refaay@hotmail.com', 'mobilephone': '+971566599051' }, { 
  //   'fname': 'Zaid', 'lname':'Al Taher', 'email': 'zalthare@hotmail.com', 'mobilephone': '+971566599051' }]; 
  // localStorage.setItem('testObject', JSON.stringify(testObject));
  }

  function provisionAll() {
    var collab = JSON.parse(localStorage.getItem("products-collab"));
    var na = JSON.parse(localStorage.getItem("products-na"));
    var sec = JSON.parse(localStorage.getItem("products-sec"));

    var user = JSON.parse(localStorage.getItem("current-user"));
    var userItems = JSON.parse(localStorage.getItem("current-user-items"));
    var userMac = JSON.parse(localStorage.getItem("mac-phone"));
    var userModel = JSON.parse(localStorage.getItem("model-phone"));

    // Say hello using bot
    fetch(BASE + '/provision-user', {
      method: "post",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "products-collab": JSON.stringify(collab),
        "products-na": JSON.stringify(na),
        "products-sec": JSON.stringify(sec),
        "user-name" : JSON.stringify(user),
        "user-items" : JSON.stringify(userItems),
        "mac-phone" : JSON.stringify(userMac),
        "model-phone" : JSON.stringify(userModel)
      })
    }).then(function (text) {
        return text.json();
    }).then(function (body) {
        console.log(body);
        document.getElementById("loading").setAttribute("hidden", true);
        localStorage.setItem("status-message", JSON.stringify(body));

        document.getElementById('statustitle').textContent = "Completed"

        var domains = JSON.parse(localStorage.getItem("domains-done"));

        if (domains.includes("Collaboration")) {
            document.getElementById('collab-status').classList.add("text-success");
            document.getElementById('collab-status').classList.add("icon-check-outline");

            document.getElementById('collab-products').textContent += "Actions taken: " + body["Collab"];
        }
        else {
            document.getElementById('collab-status').classList.add("text-danger");
            document.getElementById('collab-status').classList.add("icon-error-outline");
        }

        if (domains.includes("Network Access")) {
            document.getElementById('na-status').classList.add("text-success");
            document.getElementById('na-status').classList.add("icon-check-outline");

            document.getElementById('na-products').textContent += "Actions taken: " + body["NA"];
        }
        else {
            document.getElementById('na-status').classList.add("text-danger");
            document.getElementById('na-status').classList.add("icon-error-outline");
        }

        if (domains.includes("Security")) {
            document.getElementById('sec-status').classList.add("text-success");
            document.getElementById('sec-status').classList.add("icon-check-outline");

            document.getElementById('sec-products').textContent += "Actions taken: " + body["Security"];
        }
        else {
            document.getElementById('sec-status').classList.add("text-danger");
            document.getElementById('sec-status').classList.add("icon-error-outline");
        }
    });
  }

  function dashboard() {
    fetch('./dashboard-data', {
      method: "get",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    }).then(function (text) {
        return text.json();
    }).then(function (body) {
        document.getElementById('collabnumber').textContent = body["no_collab_users"];
        document.getElementById('devicenumber').textContent = body["no_collab_devices"];
        document.getElementById('securitynumber').textContent = body["no_duo_users"];
    })
  }

  function activatePrompt() {
    // Get selected products
    var boxes = document.getElementById("checkboxes").children;
    var i=0;
    if (boxes[boxes.length-1].getElementsByTagName('input')[0].checked) {
        document.getElementById("mac-prompt").classList.remove('disabled');
        document.getElementById("model-prompt").classList.remove('disabled');
    } else {
        document.getElementById("mac-prompt").classList.add('disabled');
        document.getElementById("model-prompt").classList.add('disabled');
    }
  }


