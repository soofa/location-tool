var BBE = require('./bounding-box-entry');

function addBoundingBoxRow(tableID, data) {
    var tableRef = document.getElementById(tableID);
    var firstDataRowIdx = 1;
    var newRow = tableRef.insertRow(firstDataRowIdx);
    var newCell;

    newCell = newRow.insertCell(0);
    var newText = document.createTextNode(data.name);
    newCell.appendChild(newText);

    newCell = newRow.insertCell(1);
    var newText = document.createTextNode(data.created_at);
    newCell.appendChild(newText);

    newCell = newRow.insertCell(2);
    var newText = document.createTextNode(data.state);
    newCell.appendChild(newText);
}

function postBoundingBox(bb, button) {
    BBE.create(bb).
        then(function(response) {
            button.classList.remove('loading');
            addBoundingBoxRow("latest-bb-table", response.data);
        }).
        catch(function(response) {
            button.classList.remove('loading');
            alert('Bounding Box Creation failed');
        });
}

function initializeBoundingBoxEntry() {
    window.BBE = BBE;
    window.currentBoundingBox = null;

    var button = document.getElementById('bb-create-button');
    button.addEventListener('click', function(event) {
        var bb = window.currentBoundingBox;
        var nameInput = document.getElementById('bb-name-input-field');
        bb.name = nameInput.value;
        button.classList.add('loading');
        postBoundingBox(bb, button);
    });
}

initializeBoundingBoxEntry();
