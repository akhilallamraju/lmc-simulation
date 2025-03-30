// Add event listener to the Assemble button
document.getElementById('assembleButton').addEventListener('click', fetchCode);

let code = [] // Initialize array to hold table code

// Function to collect input values into a two-dimensional array, ignoring blank rows
function fetchCode() {
    // Fetches the input from the text editor.
    // The inputs are converted into a 2D array where each sub-array is a line in the code.
    // Blank lines are ignored as they are redundant.
    for (let r = 0; r < rows; r++) {
        const row = [] // Initialize array for each row
        let isRowEmpty = true // Flag to check if the row is empty

        // Collect input values from each cell (excluding row number cell)
        for (let c = 1; c <= cols; c++) {
            const input = tbody.rows[r].cells[c].querySelector('input') // Get input element
            row.push(input.value) // Add input value to row array
            if (input.value.trim() !== "") {
                isRowEmpty = false // If any input has value, set flag to false
            }
        }

        // Add row array to code array only if the row is not empty
        if (!isRowEmpty) {
            code.push(row);
        }
    }
    main(code)
    return code
}

function main(code) {
    // Updating console
    let consoleDiv = document.getElementById("console")
    const checkingForErrorsMessage = " Checking code for syntax errors...\n"
    // Appends the checking for errors message to the text of the console div
    consoleDiv.innerText = ">>>"
    consoleDiv.innerText += checkingForErrorsMessage
    // Time delay so that the text does not appear instantly (usability feature)
    setTimeout(getAndOutputCodeErrorStatus, 1000, code, consoleDiv)
}

function getAndOutputCodeErrorStatus(code, console) {
    // Instance of the SyntaxAnalyser class from syntax-analyser.js
    // As expected, this object makes sure the user-inputted code is syntactically correct
    // The value of isSyntaxValid is like this: [true] IF code is good
    //                                                                    OR
    //                                          [false, errorName, errorLineNumber] IF there is an error
    const isSyntaxValid = new SyntaxAnalyser(code)
    let codeVerdictMessage

    if (isSyntaxValid[0]) {
        codeVerdictMessage = "Your code is syntactically correct!\n"
    } else {
        if (isSyntaxValid[2] === null) {
            codeVerdictMessage = `Error: ${isSyntaxValid[1]}\n`
        } else {
            codeVerdictMessage = `Error: ${isSyntaxValid[1]} on line ${isSyntaxValid[2]}\n`
        }
    }

    console.innerText += codeVerdictMessage
}

function sendCodeToFlaskBackend() {
    // Packages the 2D array as a JSON object under the key 'code'
    // Sends a POST request to the backend (ie: informing the backend that data is intended to be sent to it)
    // Sends the JSON to the backend
    fetch('/receive-code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: fetchCode() }) // Convert 2D list to JSON
    })
}