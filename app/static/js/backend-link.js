fetch('./hello-flask')
  .then(function (response) {
      return response.json();
  }).then(function (text) {
      console.log(text.greeting); 
  });