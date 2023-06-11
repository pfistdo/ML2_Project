// Send request to server to classify image
function classify_image(event, text) {
  var form_data = new FormData();
  var img = document.getElementById("upload_image").files[0];
  form_data.append("file", img);

  if (img != undefined) {
    var btn = document.getElementById("classify_btn");
    btn.classList.add("button--loading");
    btn.textContent = ''
    $.ajax({
      url: "model/image", // point to server-side URL
      dataType: "text", // what to expect back from server
      cache: false,
      contentType: false,
      processData: false,
      data: form_data,
      type: "post",
      success: function (response) {
        response = JSON.parse(response);
        console.log(response)

        var resultDiv = document.getElementById("result");
        resultDiv.innerHTML = ""; // Clear previous results

        // Create HTML elements dynamically to display the JSON response
        for (var key in response) {
          var row = document.createElement("tr");
          var keyCell = document.createElement("th");
          var valueCell = document.createElement("td");

          keyCell.textContent = key;
          valueCell.textContent = response[key];

          row.appendChild(keyCell);
          row.appendChild(valueCell);
          resultDiv.appendChild(row);
        }

        document.getElementById("classify_btn").disabled = false; // activate classify button
      },
      error: function (response) {
        alert(response, "danger");
      },
      complete: function (response) {
        btn.classList.remove("button--loading")
        btn.textContent = 'Classify image'
      }
    });
  } else {
      // alert("Please select an image to upload!", "danger");
  }
}

// Upload image to server using AJAX Post
function upload_image() {
  var form_data = new FormData();
  var ins = document.getElementById("upload_image").files[0];
  form_data.append("file", ins);

  if (ins != undefined) {
    $.ajax({
      url: "upload", // point to server-side URL
      dataType: "text", // what to expect back from server
      cache: false,
      contentType: false,
      processData: false,
      data: form_data,
      type: "post",
      success: function (response) {
        alert(response, "success");
        document.getElementById("classify_btn").disabled = false; // activate classify button
      },
      error: function (response) {
        alert(response, "danger");
      },
    });
  } else {
    alert("Please select an image to upload!", "danger");
  }
}

// Preview image before upload
function preview_image() {
  const preview = document.querySelector("#imagePreview");
  const file = document.querySelector("input[type=file]").files[0];
  const reader = new FileReader();

  reader.addEventListener(
    "load",
    function () {
      preview.classList.add("mb-3")
      preview.innerHTML = '<img src="' + reader.result + '" class="img-fluid">';
    },
    false
  );

  if (file) {
    reader.readAsDataURL(file);
  }
}

// Bootstrap alert
const alert = (message, type) => {
  const alertPlaceholder = document.getElementById('alerts')
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible fade show" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)
}