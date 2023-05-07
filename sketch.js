p5.disableFriendlyErrors = true;

let img;
let outputImg;
let processing = false;
let x = 0;
let y = 0;

function setup() {
    canvas = createCanvas(windowWidth - 100, windowHeight - 400);
    canvas.parent("previews");
    frameRate(500);
}

function draw() {
    if (outputImg != null) {
        image(outputImg, 0, 0, outputImg.width/16, outputImg.height/16);
    }
    
    if (processing) {
        if (x < img.width && y < img.height) {
            x += 32;
            outputImg.fill(img.get(x, y));
            outputImg.rect(x, y, 32, 32);
            if (x == img.width - (img.width % x)) {
                x = 0;
                y += 32;
            }
        } else {
            outputImg.save('outputImg', 'png');
            processing = false;
            x = 0;
            y = 0;
        }
    }
    // requestAnimationFrame(draw)
}

function windowResized() {
    resizeCanvas(windowWidth/2, windowHeight/2);
}

function loadFile(event) {
    var output = document.getElementById('file-preview');
    imageURL = event.target.files[0];
    output.src = URL.createObjectURL(event.target.files[0]);
    img = loadImage(output.src);
    /*
    output.onload = function() {
        URL.revokeObjectURL(output.src) // free memory
    }
    */
};

function applyFilter() {
    outputImg = createGraphics(img.width, img.height);
    processing = true;
}
