const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const shell = require('node-powershell');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  console.log('Congratulations, your extension "py2" is now active!');
  let disposable = vscode.commands.registerCommand('py2.analyzefile', function () {
    vscode.window.showInformationMessage('Analyze file from py2!');

    const activeEditor = vscode.window.activeTextEditor;
    if (activeEditor) {
      const filePath = activeEditor.document.uri.fsPath; // Use fsPath to get the file path
      const fileName = path.basename(filePath);
      console.log("active file path is: " + fileName);
      analyzeFile(filePath); // Pass the file path as a string
    }
  });
  context.subscriptions.push(disposable);
}

function deactivate() { }

// Function to analyze a Python file
function analyzeFile(filePath) {
    // Read the content of the selected file
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    
    // Load the Python code template
    const pythonCodeTemplatePath = path.join(__dirname, 'injectCodepython.py');
    const pythonCodeTemplate = fs.readFileSync(pythonCodeTemplatePath, 'utf-8');
    
    // Replace placeholders with actual file content
    const pythonCode = pythonCodeTemplate
        .replace(/<__b__s__>/gi, fileContent)
        .replace(/<__f__n__>/gi, path.basename(filePath));
    
    // Create a temporary Python script
    const pythonScriptPath = path.join(__dirname, 'python_output.py');
    fs.writeFileSync(pythonScriptPath, pythonCode, 'utf-8');
    
    // Create a new PowerShell instance
    const ps = new shell({
        executionPolicy: 'Bypass',
        noProfile: true
    });
    
    // Change the working directory to the script's location
    ps.addCommand(`cd "${__dirname}"`);

    
    // Execute the Python script
    ps.addCommand('py python_output.py');
    
    ps.invoke()
        .then(output => {
            // Open the generated HTML file in a web browser
            const webpagePath = path.join(__dirname, 'pytracex.html');
            openWebpage(webpagePath);
        })
        .catch(err => {
            console.error(err);
        });
}

function openWebpage(webpagePath) {
    switch (process.platform) {
        case 'darwin':
            exec(`open "${webpagePath}"`);
            break;
        case 'win32':
            exec(`start "" "${webpagePath}"`);
            break;
        default:
            exec(`xdg-open "${webpagePath}"`);
            break;
    }
}

module.exports = {
  activate,
  deactivate
};
