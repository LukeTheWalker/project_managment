let buildingsData;
let buildingsPile = [];
let draggingBuilding = null;

class Building {
    constructor(x, y, name, cost, effect, points, players) {
        this.x = x;
        this.y = y;
        this.name = name;
        this.cost = cost;
        this.effect = effect;
        this.points = points;
        this.players = players;
        this.size = 170;
        this.isDragging = false;
        this.rotation = 0;
        this.offsetX = 0;
        this.offsetY = 0;
    }

    display() {
        // Display the building as a parallelogram
        push();
        translate(this.x, this.y);
 
        noStroke();
        fill(200);

        push();
        let x1 = this.size;
        let y1 = 0;

        let x2 = this.size / 2;
        let y2 = this.size * sqrt(3) / 2;

        let x = (x1 + x2) / 2;
        let y = (y1 + y2) / 2;
        
        stroke(0);
        noFill();
        circle(x, y, 5);

        translate(x, y);
        rotate(this.rotation);
        translate(-x, -y);            

        fill(200);
        noStroke();

        // First equilateral triangle
        beginShape();
        vertex(0, 0);
        vertex(this.size, 0);
        vertex(this.size / 2, this.size * sqrt(3) / 2); // Height of an equilateral triangle
        endShape(CLOSE);

        // Second equilateral triangle (shifted to the right)
        beginShape();
        vertex(this.size, 0);
        vertex(1.5 * this.size, this.size * sqrt(3) / 2);
        vertex(this.size / 2, this.size * sqrt(3) / 2);
        endShape(CLOSE);

        // display the interaction border
        if (this.isMouseOver()) {
            stroke(255, 0, 0);
        } else {
            stroke(0);
        }

        noFill();
        strokeWeight(2);
        beginShape();
        vertex(0, 0);
        vertex(this.size, 0);
        vertex(1.5 * this.size, this.size * sqrt(3) / 2);
        vertex(0.5 * this.size, this.size * sqrt(3) / 2);
        endShape(CLOSE);

        pop();
        // Display text inside the building
        // if (this.flipped) translate(-this.size/2, 0);
        fill(0);
        textSize(12);
        textAlign(CENTER, CENTER);
        text(`Name: ${this.name}`, x - 30, y - 50);
        text(`Cost: ${this.cost}`, x - 20, y - 30);
        text(`Type: ${this.effect.type}`, x - 10, y - 10);
        // center left
        // textAlign(CENTER, TOP);
        let descriptionLines = this.effect.description.split('\n');
        for (let i = 0; i < descriptionLines.length; i++) {
            text(descriptionLines[i], x + 10 * i, y + 10 + i * 15);
        }
        // text(`${this.effect.description}`, x, y+12);
        
        pop();
    }

    // Check if mouse is over the building
    isMouseOver() {
        // Step 1: Calculate the midpoint of the parallelogram
        let centerX = this.x + this.size * 0.75; // Midpoint of the width
        let centerY = this.y + (this.size * sqrt(3) / 4); // Midpoint of the height
    
        // Step 2: Calculate mouse position relative to the building's center
        let mx = mouseX - centerX;
        let my = mouseY - centerY;
    
        // Step 3: Apply reverse rotation to the mouse coordinates
        // We rotate the mouse coordinates back by the negative of this.rotation to reverse the building's rotation
        let cosA = cos(-this.rotation);
        let sinA = sin(-this.rotation);
    
        // Apply reverse rotation to mouse coordinates
        let rotatedMouseX = cosA * mx - sinA * my;
        let rotatedMouseY = sinA * mx + cosA * my;
    
        // Step 4: Translate the rotated mouse coordinates back to the original building's local coordinates
        let transformedMouseX = rotatedMouseX + (this.size * 0.75);
        let transformedMouseY = rotatedMouseY + (this.size * sqrt(3) / 4);
    
        // Step 5: Check if the transformed mouse coordinates are inside either triangle
    
        // First triangle vertices
        let v0 = createVector(0, 0);
        let v1 = createVector(this.size, 0);
        let v2 = createVector(this.size / 2, this.size * sqrt(3) / 2);
    
        let inFirstTriangle = Building.pointInTriangle(v0, v1, v2, createVector(transformedMouseX, transformedMouseY));
    
        // Second triangle vertices
        v0 = createVector(this.size, 0);
        v1 = createVector(1.5 * this.size, this.size * sqrt(3) / 2);
        v2 = createVector(this.size / 2, this.size * sqrt(3) / 2);
    
        let inSecondTriangle = Building.pointInTriangle(v0, v1, v2, createVector(transformedMouseX, transformedMouseY));
    
        // Return true if the mouse is inside either triangle
        return inFirstTriangle || inSecondTriangle;
    }
        

    // Check if a point is inside a triangle
    static pointInTriangle(v0, v1, v2, v) {
        let b1 = Building.sign(v, v0, v1) < 0.0;
        let b2 = Building.sign(v, v1, v2) < 0.0;
        let b3 = Building.sign(v, v2, v0) < 0.0;

        return ((b1 == b2) && (b2 == b3));
    }

    // Helper function to calculate the sign of a point relative to a line
    static sign(p1, p2, p3) {
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y);
    }

    // Dragging functionality
    startDragging() {
        this.isDragging = true;
        this.offsetX = mouseX - this.x;
        this.offsetY = mouseY - this.y;
    }

    stopDragging() {
        this.isDragging = false;
    }

    drag() {
        if (this.isDragging) {
            this.x = mouseX - this.offsetX;
            this.y = mouseY - this.offsetY;
        }
    }

    rotate () {
        this.rotation += PI/3;
        this.rotation = this.rotation % (PI*2);
    }
}