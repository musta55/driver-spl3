const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

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

  // Example: Show the results in a VS Code panel or output channel
  const outputChannel = vscode.window.createOutputChannel('Your Extension Output');
  outputChannel.appendLine('Analysis results:');
  // Append more output as needed
  outputChannel.show();
}

vscode.commands.registerCommand('pytracex.analyzePythonFile', async (uri) => {
  if (uri && uri.fsPath) {
    analyzeFile(uri.fsPath);
  } else {
    vscode.window.showErrorMessage('No Python file selected for analysis.');
  }
});

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  const disposable = vscode.commands.registerCommand('pytracex.analyzeCurrentFile', () => {
    const activeEditor = vscode.window.activeTextEditor;
    if (activeEditor) {
      const filePath = activeEditor.document.uri.fsPath;
      analyzeFile(filePath);
    }
  });

  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};
