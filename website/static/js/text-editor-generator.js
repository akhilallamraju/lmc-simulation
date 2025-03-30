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