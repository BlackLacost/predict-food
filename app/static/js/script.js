let el = x => document.querySelector(x)

function click_hidden_input() {
  el('.predict--choose-image').click()
}

function showImage(input) {
  let file = input.files[0];

  el('.predict--food').innerHTML = file.name;

  let reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = function() {
    el('.predict--image').src = reader.result;
    el('.predict--image').className = "predict--image";
  }
}