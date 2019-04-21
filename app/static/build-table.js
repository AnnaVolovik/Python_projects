
function generateOutput(result) {

    var res = document.getElementById("result");

    var div_centered = document.createElement('div');
    var code = document.createElement('code');
    var pre = document.createElement('pre');
    pre.textContent = JSON.stringify(result.request_info, undefined, 2);
    var header = document.createElement('h3');
    header.textContent = 'General information about the matrix';
    code.appendChild(pre);
    div_centered.appendChild(code);
    res.appendChild(header);
    res.appendChild(div_centered);

    var div_els = document.createElement('div');

    for (var key in result) {
        if (key == 'request_info') continue;

        else if (key == 'columns') {
            var header = 'Columns info';
        } else if (key == 'cells') {
            var header = 'Cells info';
        } else {var header = 'Rows info';}

        var div_cells = document.createElement('div');
        div_cells.className = "column";
        var code_cells = document.createElement('code');
        var pre_cells = document.createElement('pre');
        pre_cells.textContent = JSON.stringify(result[key], undefined, 2);
        var header_cells = document.createElement('h3');
        header_cells.textContent = header;
        code_cells.appendChild(pre_cells);
        div_cells.appendChild(header_cells);
        div_cells.appendChild(code_cells);
        div_els.appendChild(div_cells);
        }
    res.appendChild(div_els);
}

function generateTableHead(table, cells) {
    let thead = table.createTHead();
    let row = thead.insertRow();

    for (var i = 0; i < cells[0].length; i++) {
        let obj = cells[0][i];
        let th = document.createElement("th");
        let text = document.createTextNode(obj.value);
        th.appendChild(text);
        row.appendChild(th);
        }
    }

function generateTable(table, rows, cells) {

    for (let row_el of rows) {
        if (row_el.type == 'headerRow') continue;
        let row = table.insertRow();
        for (let cell_el of cells[row_el.id]) {
            let cell = row.insertCell();
            if (cell_el.type == "hierarchyCell") {
                var text = document.createTextNode("\xa0\xa0\xa0".repeat(row_el.level) + cell_el.value);
            } else {var text = document.createTextNode(cell_el.value != null ? cell_el.value : '')}

            cell.appendChild(text);
        }
    }
}


