const rows = 50; // Number of rows
const cols = 3;   // Number of input columns (excluding Line Number column)
const tbody = document.querySelector('#textEditor'); // Reference to tbody

// Create table rows and cells with input fields
for (let r = 0; r < rows; r++) {
    let row = tbody.insertRow(r); // Insert a new row
    let rowNumCell = row.insertCell(0); // Insert first cell for row number
    rowNumCell.textContent = r + 1; // Set row number

    // Insert cells for inputs
    for (let c = 0; c < cols; c++) {
        let cell = row.insertCell(c + 1); // Insert cell
        let input = document.createElement('input'); // Create input element
        input.type = 'text'; // Set input type
        input.classList.add('form-control', 'form-control-sm', 'p-1'); // Add Bootstrap form-control class with small size
        input.style.lineHeight = '1'; // Inline style for tighter fit
        cell.appendChild(input); // Append input to cell
    }
}

// Add event listener to the Assemble button
document.getElementById('assembleButton').addEventListener('click', assemble);

// Function to collect input values into a two-dimensional array, ignoring blank rows
function assemble() {
    const data = []; // Initialize array to hold table data
    for (let r = 0; r < rows; r++) {
        const row = []; // Initialize array for each row
        let isRowEmpty = true; // Flag to check if the row is empty

        // Collect input values from each cell (excluding row number cell)
        for (let c = 1; c <= cols; c++) {
            const input = tbody.rows[r].cells[c].querySelector('input'); // Get input element
            row.push(input.value); // Add input value to row array
            if (input.value.trim() !== "") {
                isRowEmpty = false; // If any input has value, set flag to false
            }
        }

        // Add row array to data array only if the row is not empty
        if (!isRowEmpty) {
            data.push(row);
        }
    }
    console.log(data); // Log the two-dimensional array to the console
}