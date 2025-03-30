class SyntaxAnalyser {
    constructor(code) {
        this.code = code  // User-inputted LMC assembly code

        this.unfinishedBranches = []  // Branch endings in the label
        this.finishedBranches = []
        this.identifiers = []  // Variables

        const areLabelsValid = this.checkLabels()
        if (!(areLabelsValid[0])) {
            return areLabelsValid
        }

        const areOpcodesValid = this.checkOpcodes()
        if (!(areOpcodesValid[0])) {
            return areOpcodesValid
        }

        const areOperandsValid = this.checkOperands()
        if (!(areOperandsValid[0])) {
            return areOperandsValid
        }

        const finalChecksVerdict = this.postAnalysisChecks()
        if (!(finalChecksVerdict[0])) {
            return finalChecksVerdict
        }

        return [true]
    }

    checkLabels() {
        let lineNumber = 1
        const branchOpcodes = ["BRA", "BRP", "BRZ"]

        for (let line of this.code) {
            let label = line[0].toLowerCase()

            // If there is no label, there is no need to check it
            if (label === "") {
                lineNumber += 1
                continue
            }

            // Check 1: Label cannot be an integer
            if (!(isNaN(parseInt(label)))) {
                return [false, "integer-as-label-forbidden", lineNumber]
            }

            // Check 2: No whitespace
            if (label.includes(" ")) {
                return [false, "whitespace-in-label-forbidden", lineNumber]
            }

            // Check 3: Label cannot exceed 8 characters in length
            if (label.length > 8) {
                return [false, "label-greater-than-8-characters", lineNumber]
            }

            // Check 4: If the opcode is not DAT, the label data must be added to 'unfinishedBranches' as it must be...
            // ...for a branch.
            if (branchOpcodes.includes(line[1].toUpperCase())) {
                //                            label,   start, finish
                this.unfinishedBranches.push([line[0], null, lineNumber])
            }

            lineNumber += 1
        }

        return [true]
    }

    checkOpcodes() {
        let lineNumber = 1
        const validOpcodes = ["ADD", "SUB", "STO", "LDA", "BRA", "BRZ", "BRP", "HLT", "DAT", "INP", "OUT"]
        let hltPresent = false

        for (let line of this.code) {
            let opcode = line[1].toUpperCase()

            // Check 1: All opcodes are valid
            if (!(validOpcodes.includes(opcode))) {
                return[false, "invalid-operand", lineNumber]
            }

            // Check 2: No whitespace in any opcode
            if (opcode.includes((" "))) {
                return [false, "whitespace-in-opcode", lineNumber]
            }

            // Check 3: DAT opcodes must only be after the HLT opcode
            if (!(hltPresent) && opcode === "DAT") {
                return [false, "dat-before-hlt-forbidden", lineNumber]
            }

            // Check 4: Only DAT opcodes can be after the HLT opcode
            if (hltPresent && !(opcode === "DAT")) {
                return [false, "only-dat-after-hlt", lineNumber]
            }

            // Flags if a HLT opcode has been detected
            if (opcode === "HLT") {
                hltPresent = true
            }

            lineNumber += 1
        }
        // Check 5: There must be a HLT opcode present
        if (!(hltPresent)) {
            return [false, "no-hlt-opcode-present", null]
        } else {
            return [true]
        }
    }

    checkOperands() {
        let lineNumber = 1
        const operandRequiredOpcodes = ["ADD", "SUB", "STO", "LDA", "BRA", "BRZ", "BRP"]
        const operandForbiddenOpcodes = ["INP", "OUT", "HLT"]
        const branchOpcodes = ["BRA", "BRP", "BRZ"]

        for (let line of this.code) {
            let label = line[0].toLowerCase()
            let opcode = line[1].toUpperCase()
            let operand = line[2].toLowerCase()

            // Check 1: Operand cannot be greater than 8 characters
            if (operand.length > 8) {
                return [false, "operand-greater-than-8-characters", lineNumber]
            }

            // Check 2: No whitespace
            if (operand.includes(" ")) {
                return [false, "whitespace-in-operand-forbidden", lineNumber]
            }

            // Check 3: Certain opcodes must have an operand
            if (operandRequiredOpcodes.includes(opcode) && operand === "") {
                return [false, "operand-required", lineNumber]
            }

            // Check 4: Certain opcodes must NOT have an operand
            if (operandForbiddenOpcodes.includes(opcode) && !(operand === "")) {
                return [false, "operand-forbidden", lineNumber]
            }

            // Check 5: If there is no opcode or operand for a DAT opcode, that line can be ignored
            if (label === "" && opcode === "DAT" && operand === "") {
                lineNumber += 1
                continue
            }

            // Check 6: If opcode is DAT, operand must be an integer
            if (opcode === "DAT" && isNaN(parseInt(operand))) {
                if (operand === "") {}

                else {
                    return [false, "dat-operand-must-be-null-or-integer", lineNumber]
                }
            }

            // Check 7: All integer operands must be <= 49 (as there are only 50 memory locations: 0-49)
            if (!(isNaN(parseInt(operand)))) {
                if (parseInt(operand) > 49) {
                    return [false, "operand-too-large", lineNumber]
                }
            }

            // Check 8: If opcode is a branch, the operand must be a string
            if (branchOpcodes.includes(opcode) && !(isNaN(parseInt(operand)))) {
                return [false, "operand-for-branch-opcode-must-be-string", lineNumber]
            }

            // Check 9: If opcode is branch, there must be an item in the 'unfinishedBranches' array with the same name.
            //          If so, the loop is complete and the loop info will be moved into 'finishedBranches'.
            if (branchOpcodes.includes(opcode)) {
                let index = 0

                for (let item of this.unfinishedBranches) {
                    if (item[0] === operand) {
                        item[1] = lineNumber
                        this.finishedBranches.push(item)
                        delete this.unfinishedBranches[index]

                        index += 1
                    }
                }
            }

            //  Check(?) 10: If opcode is DAT, a variable must be initialised in the 'identifiers' array
            //           Item in 'identifiers': [varName, data]
            if (opcode === "DAT") {
                this.identifiers.push(label)
            }

            lineNumber += 1
        }

        return [true]
    }

    postAnalysisChecks() {
        // Check 1: Unfinished branches
        if (this.unfinishedBranches.length !== 0) {
            let firstUnfinishedBranch = this.unfinishedBranches[0]
            let branchEndLineNumber = firstUnfinishedBranch[2]
            return [false, "unfinished-branch", branchEndLineNumber]
        }

        let lineNumber = 1
        const nonBranchOperandRequiredOpcodes = ["ADD", "SUB", "STO", "LDA"]

        // Check 2: References in code to undeclared variables
        for (let line of this.code) {
            let label = line[0]; let opcode = line[1]; let operand = line[2]

            if (nonBranchOperandRequiredOpcodes.includes(opcode) && isNaN(parseInt(operand))) {
                if (!(this.identifiers.includes(operand))) {
                    return[false, "reference-to-undeclared-variable", lineNumber]
                }
            }
            lineNumber += 1
        }

        // Check 3: Multiple branches with the same name
        for (let branch of this.finishedBranches) {
            let lineNumber = 1
            let branchName = branch[0]
            let branchNamesAlreadySeen = []

            if (branchNamesAlreadySeen.indexOf(branchName) !== -1) {
                return [false, "multiple-branches-with-same-name"]
            }

            branchNamesAlreadySeen.push(branchName)
            lineNumber += 1
        }

        // Check 4: Multiple variables with the same name
        for (let identifier of this.identifiers) {
            let lineNumber = 1
            let identifiersAlreadySeen = []

            if (identifiersAlreadySeen.indexOf(identifier) !== -1) {
                return [false, "multiple-variables-with-same-name"]
            }

            identifiersAlreadySeen.push(identifier)
            lineNumber += 1
        }
    }
}