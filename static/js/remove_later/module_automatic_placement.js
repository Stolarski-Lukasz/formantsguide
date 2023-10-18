import { create_element, remove_element } from "./module_elements.js"

export function draw_vq(base_size, margin, myCanvas) {
  myCanvas.addLayer({
    id: 'vq',
    render: function (canvas, ctx) {
      canvas.width = base_size + (2 * margin)
      canvas.height = (0.75 * base_size) + (2 * margin)

      ctx.beginPath(); // initializes a new line drawing
      ctx.moveTo(margin, margin);
      ctx.lineTo(base_size + margin, margin);
      ctx.lineTo(base_size + margin, (0.75 * base_size) + margin);
      ctx.lineTo((0.5 * base_size) + margin, (0.75 * base_size) + margin);
      ctx.lineTo(margin, margin);
      ctx.moveTo((0.1666666666667 * base_size) + margin, (0.25 * base_size) + margin);
      ctx.lineTo(base_size + margin, (0.25 * base_size) + margin);
      ctx.moveTo((0.3333333333334 * base_size) + margin, (0.5 * base_size) + margin);
      ctx.lineTo(base_size + margin, (0.5 * base_size) + margin);
      ctx.moveTo((0.5 * base_size) + margin, margin);
      ctx.lineTo((0.75 * base_size) + margin, (0.75 * base_size) + margin);
      // accepts any css color declaration...
      // use it each time you want to change color to a new one
      ctx.strokeStyle = 'black';
      ctx.lineWidth = 2;
      ctx.stroke();
    }
  })
  myCanvas.render();
};


export function draw_coordinate_grid(base_size, margin, myCanvas) {
  myCanvas.addLayer({
    id: 'coordinate_grid',
    render: function (canvas, ctx) {

      // drawing grid
      ctx.beginPath();
      ctx.moveTo(margin, margin - (0.03 * base_size))
      ctx.lineTo(margin, (0.75 * base_size) + margin + (0.03 * base_size));
      ctx.moveTo((0.1 * base_size) + margin, margin - (0.03 * base_size));
      ctx.lineTo((0.1 * base_size) + margin, (0.75 * base_size) + margin + (0.03 * base_size))
      ctx.moveTo((0.2 * base_size) + margin, margin - (0.03 * base_size));
      ctx.lineTo((0.2 * base_size) + margin, (0.75 * base_size) + margin + (0.03 * base_size))
      ctx.moveTo((0.3 * base_size) + margin, margin - (0.03 * base_size));
      ctx.lineTo((0.3 * base_size) + margin, (0.75 * base_size) + margin + (0.03 * base_size))
      ctx.moveTo((0.4 * base_size) + margin, margin - (0.03 * base_size));
      ctx.lineTo((0.4 * base_size) + margin, (0.75 * base_size) + margin + (0.03 * base_size))
      ctx.moveTo((0.5 * base_size) + margin, margin - (0.03 * base_size));
      ctx.lineTo((0.5 * base_size) + margin, (0.75 * base_size) + margin + (0.03 * base_size))
      ctx.moveTo((0.6 * base_size) + margin, margin - (0.03 * base_size));
      ctx.lineTo((0.6 * base_size) + margin, (0.75 * base_size) + margin + (0.03 * base_size))
      ctx.moveTo((0.7 * base_size) + margin, margin - (0.03 * base_size));
      ctx.lineTo((0.7 * base_size) + margin, (0.75 * base_size) + margin + (0.03 * base_size))
      ctx.moveTo((0.8 * base_size) + margin, margin - (0.03 * base_size));
      ctx.lineTo((0.8 * base_size) + margin, (0.75 * base_size) + margin + (0.03 * base_size))
      ctx.moveTo((0.9 * base_size) + margin, margin - (0.03 * base_size));
      ctx.lineTo((0.9 * base_size) + margin, (0.75 * base_size) + margin + (0.03 * base_size))
      ctx.moveTo(base_size + margin, margin - (0.03 * base_size));
      ctx.lineTo(base_size + margin, (0.75 * base_size) + margin + (0.03 * base_size));

      ctx.moveTo(margin - (0.03 * base_size), (0.75 * base_size) + margin)
      ctx.lineTo(base_size + margin + (0.03 * base_size), (0.75 * base_size) + margin);
      ctx.moveTo(margin - (0.03 * base_size), (0.65 * base_size) + margin)
      ctx.lineTo(base_size + margin + (0.03 * base_size), (0.65 * base_size) + margin);
      ctx.moveTo(margin - (0.03 * base_size), (0.55 * base_size) + margin)
      ctx.lineTo(base_size + margin + (0.03 * base_size), (0.55 * base_size) + margin);
      ctx.moveTo(margin - (0.03 * base_size), (0.45 * base_size) + margin)
      ctx.lineTo(base_size + margin + (0.03 * base_size), (0.45 * base_size) + margin);
      ctx.moveTo(margin - (0.03 * base_size), (0.35 * base_size) + margin)
      ctx.lineTo(base_size + margin + (0.03 * base_size), (0.35 * base_size) + margin);
      ctx.moveTo(margin - (0.03 * base_size), (0.25 * base_size) + margin)
      ctx.lineTo(base_size + margin + (0.03 * base_size), (0.25 * base_size) + margin);
      ctx.moveTo(margin - (0.03 * base_size), (0.15 * base_size) + margin)
      ctx.lineTo(base_size + margin + (0.03 * base_size), (0.15 * base_size) + margin);
      ctx.moveTo(margin - (0.03 * base_size), (0.05 * base_size) + margin)
      ctx.lineTo(base_size + margin + (0.03 * base_size), (0.05 * base_size) + margin);

      ctx.font = "15px Arial";
      ctx.fillStyle = "grey";
      ctx.fillText("0.0", margin - (base_size * 0.013), (base_size * 0.75) + margin + (0.055 * base_size));
      ctx.fillText("0.1", (0.1 * base_size) + margin - (base_size * 0.013), (base_size * 0.75) + margin + (0.055 * base_size));
      ctx.fillText("0.2", (0.2 * base_size) + margin - (base_size * 0.013), (base_size * 0.75) + margin + (0.055 * base_size));
      ctx.fillText("0.3", (0.3 * base_size) + margin - (base_size * 0.013), (base_size * 0.75) + margin + (0.055 * base_size));
      ctx.fillText("0.4", (0.4 * base_size) + margin - (base_size * 0.013), (base_size * 0.75) + margin + (0.055 * base_size));
      ctx.fillText("0.5", (0.5 * base_size) + margin - (base_size * 0.013), (base_size * 0.75) + margin + (0.055 * base_size));
      ctx.fillText("0.6", (0.6 * base_size) + margin - (base_size * 0.013), (base_size * 0.75) + margin + (0.055 * base_size));
      ctx.fillText("0.7", (0.7 * base_size) + margin - (base_size * 0.013), (base_size * 0.75) + margin + (0.055 * base_size));
      ctx.fillText("0.8", (0.8 * base_size) + margin - (base_size * 0.013), (base_size * 0.75) + margin + (0.055 * base_size));
      ctx.fillText("0.9", (0.9 * base_size) + margin - (base_size * 0.013), (base_size * 0.75) + margin + (0.055 * base_size));
      ctx.fillText("1", base_size + margin - (base_size * 0.006), (base_size * 0.75) + margin + (0.055 * base_size));

      ctx.fillText("0.0", margin - (0.065 * base_size), (0.75 * base_size) + margin + (0.008 * base_size));
      ctx.fillText("0.1", margin - (0.065 * base_size), (0.65 * base_size) + margin + (0.008 * base_size));
      ctx.fillText("0.2", margin - (0.065 * base_size), (0.55 * base_size) + margin + (0.008 * base_size));
      ctx.fillText("0.3", margin - (0.065 * base_size), (0.45 * base_size) + margin + (0.008 * base_size));
      ctx.fillText("0.4", margin - (0.065 * base_size), (0.35 * base_size) + margin + (0.008 * base_size));
      ctx.fillText("0.5", margin - (0.065 * base_size), (0.25 * base_size) + margin + (0.008 * base_size));
      ctx.fillText("0.6", margin - (0.065 * base_size), (0.15 * base_size) + margin + (0.008 * base_size));
      ctx.fillText("0.7", margin - (0.065 * base_size), (0.05 * base_size) + margin + (0.008 * base_size));

      ctx.strokeStyle = 'grey';
      ctx.lineWidth = 0.3;
      ctx.stroke();
    }
  })
  myCanvas.render();
};


function draw_dot(base_size, margin, myCanvas, backness, height) {
  myCanvas.removeLayer( 'dot' );
  myCanvas.addLayer({
    id: 'dot',
    render: function (canvas, ctx) {
      // drawing dot
      ctx.beginPath();
      // x, y, radius, beginning gradient, ending gradient - I do not know what these gradients are - may be checked leter, stroke direction (if true, they counter clock-wise)
      ctx.fillStyle = 'black';
      var adjusted_backness = (backness * base_size) + margin;
      var adjusted_height = ((0.75 - height) * base_size) + margin;
      ctx.arc(adjusted_backness, adjusted_height, 10, 0, Math.PI * 2, false);
      ctx.fill(); // for cicles, this additional command neccessary for filling...
      ctx.strokeStyle = 'black';
      ctx.stroke();
    }
  })
  myCanvas.render();
};


export function submit_measurement_results(measurement_results_submit_button, f0_input,
  f1_input, f2_input, f3_input, base_size, margin, myCanvas, results_info, results_info_contents) {

  // adding click event
  measurement_results_submit_button.addEventListener('click', function (e) {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status == 200) {

        // removing spinner
        remove_element("diagram_spinner");

        // obtaining measurement results
        let json_response = xhr.responseText;
        let response_object = JSON.parse(json_response);
        let backness = response_object.backness;
        let height = response_object.height;

        // drawing dot
        draw_dot(base_size, margin, myCanvas, backness, height)

        // showing placement coordinates
        results_info_contents.innerHTML = "";
        create_element({ tag: "h5", className: "results_paragraph", innerText: "Predicted coordinates: ", parent_id: "results_info_contents" });
        create_element({ tag: "h5", className: "results_paragraph", innerText: "x = " + parseFloat(backness).toFixed(2) + ", y = " + parseFloat(height).toFixed(2), parent_id: "results_info_contents" });
        results_info.hidden = false;

        // activating download image button - I resigned with deactivating it by deafault
        // image_download_button.style.cursor = 'pointer';
        // image_download_button.className = "btn btn-success";
        // image_download_button.disabled = false;
      };
    };

    // collecting data to be sent to server
    let f0_final = f0_input.value;
    let f1_final = f1_input.value;
    let f2_final = f2_input.value;
    let f3_final = f3_input.value;
    let acoustic_measurements_id = measurement_results_submit_button.dataset.acousticMeasurementsId;
    var formData = new FormData();
    formData.append('f0_final', f0_final);
    formData.append('f1_final', f1_final);
    formData.append('f2_final', f2_final);
    formData.append('f3_final', f3_final);
    formData.append('acoustic_measurements_id', acoustic_measurements_id);

    // activating spinner
    create_element({ tag: "div", className: "spinner-border spinner-border-sm text-primary", role: "status", id: "diagram_spinner", parent_id: "measurement_results_submit_button", style_marginLeft: "1em" });

    // sending the request
    xhr.open('POST', '/get_vq_coordinates/', true);
    xhr.send(formData);
  });
};


// grid switch functionality
export function grid_switch_behaviour(grid_switch, base_size, margin, myCanvas) {
  grid_switch.addEventListener("change", function (e) {
    if (e.target.checked == false) {
      myCanvas.removeLayer('coordinate_grid');
      myCanvas.render();
    } else if (e.target.checked == true) {
      draw_coordinate_grid(base_size, margin, myCanvas);
    }
  })
};
