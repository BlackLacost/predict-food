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

async function predict() {
  let upload_files = el('.predict--choose-image').files;
  if (upload_files.length !== 1) {
    return alert("Выберете картинку");
  }
  let formData = new FormData();
  formData.append('file', upload_files[0])
  let response = await fetch('predict', {
    method: 'POST',
    body: formData,
  });

  if (response.ok) {
    let json = await response.json();
    el('.predict--result').innerHTML = `Нейросеть думает, что это ${json.result}`;
    console.log(json)
  } else {
    alert("Ошбика HTTP: " + response.status);
  }
}