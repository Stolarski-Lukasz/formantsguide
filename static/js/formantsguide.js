function draw_dot(base_size, margin, myCanvas, backness, height, id) {
    // myCanvas.removeLayer('dot');
    myCanvas.addLayer({
        id: id,
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





// var myCanvas = new layeredCanvas("theCanvas")

// // VARIABLE DECLARATIONS
// const grid_switch = document.getElementById("grid_switch");
// let base_size = 800;
// let margin = 0.1 * base_size;

// // FUNCTIONS
// grid_switch_behaviour(grid_switch, base_size, margin, myCanvas);
// draw_vq(base_size, margin, myCanvas);
// draw_coordinate_grid(base_size, margin, myCanvas);

// // drawing dot
// draw_dot(base_size, margin, myCanvas, 0, 0.75, "01")
// draw_dot(base_size, margin, myCanvas, 0.5, 0.75, "02")
// draw_dot(base_size, margin, myCanvas, 1, 0.75, "03")