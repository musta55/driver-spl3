const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const shell = require('node-powershell');

function analyzePythonFile(filePath) {
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
            // Open the generated HTML file in a webview
            const webpagePath = path.join(__dirname, 'pytracex.html');
            openWebview(webpagePath);
        })
        .catch(err => {
            console.error(err);
        });
}

function openWebview(webpagePath) {
    // Define the HTML content for the webview
    const htmlContent = `<iframe src="file://${webpagePath}" frameborder="0" width="100%" height="100%"></iframe>`;

    // Create and show a webview panel
    const panel = vscode.window.createWebviewPanel(
        'pytracexWebview',
        'pytracex Visualization',
        vscode.ViewColumn.One,
        {
            enableScripts: true,
        }
    );

    // Set the webview content
    panel.webview.html = htmlContent;
}

function activate(context) {
    console.log('pytracex extension is activated');
    let disposable = vscode.commands.registerCommand('pytracex.analyzePythonFile', () => {
        const editor = vscode.window.activeTextEditor;

        if (editor && editor.document.languageId === 'python') {
            const filePathToExamine = editor.document.uri.fsPath;
            analyzePythonFile(filePathToExamine);
            console.log('Analyzing path: '+ filePathToExamine);
        } else {
            vscode.window.showInformationMessage('Open a Python file before running this command.');
        }
    });

    context.subscriptions.push(disposable);
}
exports.activate = activate;
