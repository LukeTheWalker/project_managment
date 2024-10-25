let playerColors = ['red', 'blue', 'green', 'yellow']; // Define colors for each player
let playerSquares = []; // Store the draggable squares for players
let buttons = []; // Store buttons for players

const n_players = 4; // Number of players

function preload() {
    // Load the building data from JSON file
    buildingsData = loadJSON('../buildings.json');
}

function insertNewlines(str, n) {
    let result = '';
    let count = 0;

    for (let i = 0; i < str.length; i++) {
        if (str[i] === '\n') {
            count = 0; // Reset count if a newline is found
        }

        if (str[i] === ' ') {
            if (count >= n) {
                result += '\n'; // Replace space with newline if the limit is reached
                count = 0; // Reset the count
            } else {
                result += str[i]; // Otherwise, just add the space
            }
        } else {
            result += str[i];
            count++;
        }
    }

    return result;
}

function setup() {
    createCanvas(windowWidth, windowHeight);

    canvas = document.getElementById('defaultCanvas0'); // p5.js assigns the default canvas ID
    canvas.addEventListener('contextmenu', (e) => {
        e.preventDefault();
    });

    // Initialize buildings pile based on the JSON data
    let x = 100;
    let y = 100;

    console.log("Number of buildings: " + buildingsData.buildings.length);
    
    for (let building of buildingsData.buildings) {
        building.effect.description = insertNewlines("Effect: " + building.effect.description, 17);

        let b = new Building(x, y, building.name, building.cost, building.effect, building.points, building["#players"]);
        buildingsPile.push(b);
        // y += 20; // Stacking the buildings slightly offset from each other
    }

    // Create buttons for each player
    for (let i = 0; i < n_players; i++) {
        let btn = createButton('Player ' + (i + 1));
        btn.position(20, i * 40 + 20); // Adjust button positioning
        btn.style('background-color', playerColors[i]);
        btn.mousePressed(() => createPlayerSquare(i)); // Pass the player index
        buttons.push(btn); // Store button reference
    }
}

function draw() {
    background(255);

    // Display all buildings in the pile
    for (let i = 0; i < buildingsPile.length; i++) {
        let b = buildingsPile[i];
        b.display();
    }

    // If a building is being dragged, update its position
    if (draggingBuilding) {
        draggingBuilding.drag();
    }

    // Display all player squares
    for (let i = 0; i < playerSquares.length; i++) {
        let square = playerSquares[i];
        square.display();
    }
}

// Create a draggable square for a player
function createPlayerSquare(playerIndex) {
    let color = playerColors[playerIndex];
    let square = new PlayerSquare(mouseX, mouseY, 50, color); // Create a square at the mouse position
    playerSquares.push(square); // Add the square to the array
}

// Mouse press event to start dragging the top building
function mousePressed() {
    // Check only the top building (last in the array)
    for (let i = buildingsPile.length - 1; i >= 0; i--) {
        let b = buildingsPile[i];
        if (b.isMouseOver()) {
            if (mouseButton === LEFT) {
                draggingBuilding = b;
                draggingBuilding.startDragging();
            }
            if (mouseButton === RIGHT) {
                b.rotate();
            }
            break;
        }
    }

    // Check if a player square is clicked for dragging
    for (let i = playerSquares.length - 1; i >= 0; i--) {
        let square = playerSquares[i];
        if (square.isMouseOver()) {
            draggingBuilding = square; // Reuse dragging logic for player squares
            draggingBuilding.startDragging();
            break;
        }
    }
}

// Mouse release event to stop dragging
function mouseReleased() {
    if (draggingBuilding) {
        draggingBuilding.stopDragging();
        draggingBuilding = null;
    }
}

// Class for player draggable squares
class PlayerSquare {
    constructor(x, y, size, color) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.color = color;
        this.dragging = false;
        this.offsetX = 0;
        this.offsetY = 0;
    }

    display() {
        fill(this.color);
        rect(this.x, this.y, this.size, this.size);
    }

    isMouseOver() {
        return mouseX > this.x && mouseX < this.x + this.size && mouseY > this.y && mouseY < this.y + this.size;
    }

    startDragging() {
        this.dragging = true;
        this.offsetX = this.x - mouseX;
        this.offsetY = this.y - mouseY;
    }

    stopDragging() {
        this.dragging = false;
    }

    drag() {
        if (this.dragging) {
            this.x = mouseX + this.offsetX;
            this.y = mouseY + this.offsetY;
        }
    }
}
