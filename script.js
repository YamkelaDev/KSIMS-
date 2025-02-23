// Array to hold the file structure
let fileStructure = [];

// Function to create a new folder
function createFolder() {
    const folderName = prompt("Enter the name of the folder:");
    if (folderName) {
        fileStructure.push({ type: "folder", name: folderName, files: [] });
        updateFileStructure();
    }
}

// Function to create a new file inside a folder
function createFile() {
    const folderName = prompt("Enter the folder name to add a file:");
    const folder = fileStructure.find(f => f.name === folderName && f.type === "folder");
    if (folder) {
        const fileName = prompt("Enter the name of the file:");
        if (fileName) {
            folder.files.push({ name: fileName });
            updateFileStructure();
        }
    } else {
        alert("Folder not found!");
    }
}

// Function to display the file structure
function updateFileStructure() {
    const fileStructureDiv = document.getElementById("file-structure");
    fileStructureDiv.innerHTML = ""; // Clear the current display

    fileStructure.forEach(folder => {
        const folderDiv = document.createElement("div");
        folderDiv.classList.add("folder");
        folderDiv.innerHTML = `<strong>${folder.name}</strong>`;

        folder.files.forEach(file => {
            const fileDiv = document.createElement("div");
            fileDiv.classList.add("file");
            fileDiv.textContent = file.name;
            folderDiv.appendChild(fileDiv);
        });

        fileStructureDiv.appendChild(folderDiv);
    });
}
