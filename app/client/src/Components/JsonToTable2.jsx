import React from  "react";

export default function JsonToTable2(props) {

    let data = props.data;

    if (data === undefined | data === null) {
        return <table></table>
    } else {

        // let col_names = [];
        // let cols = data.columns.map((col, index) =>
        // {
        //     col_names.push(col.col_name);
        //     return <th className='theader' key={'th_'+(index+1)}>{col.col_name}</th>
        // });

        let rows = [];
        for (let i=0; i<data.rows.length; i++) {

            let row = [];
            let row_el = data.rows[i];
            // if (row_el.type == 'headerRow') continue;

            for (let y=0; y<data.cells[row_el.id].length; y++) {
            // for (let cell_el of data.cells[row_el.id]) {
                let cell_el = data.cells[row_el.id][y];
                if (cell_el.type == "hierarchyCell") {
                    var value = "\xa0\xa0\xa0".repeat(row_el.level) + cell_el.value;
                } else {
                    var value = cell_el.value != null ? cell_el.value : ''
                }
                row.push(<td key={'td_' + i + '_' + y} className={cell_el.type}>{value}</td>)
            }
        rows.push(<tr key={'tr_' + row_el.id}>{row}</tr>)
    }

        return (
                <table>
                    {/*<thead><tr>{cols}</tr></thead>*/}
                    <tbody>{rows}</tbody>
                </table>
            )
        }

    }

// function generateTableHead(table, cells) {
//
//     let thead = table.createTHead();
//     let row = thead.insertRow();
//
//     for (var i = 0; i < cells[0].length; i++) {
//
//         let obj = cells[0][i];
//         let th = document.createElement("th");
//         let text = document.createTextNode(obj.value);
//
//         th.appendChild(text);
//         row.appendChild(th);
//         }
//     thead.appendChild(row);
//     return thead;
//     }
//
// function generateTable(table, rows, cells) {
//
//     for (let row_el of rows) {
//         if (row_el.type == 'headerRow') continue;
//
//         let row = table.insertRow();
//
//         for (let cell_el of cells[row_el.id]) {
//
//             let cell = row.insertCell();
//
//             if (cell_el.type == "hierarchyCell") {
//                 var text = document.createTextNode("\xa0\xa0\xa0".repeat(row_el.level) + cell_el.value);
//             } else {
//                 var text = document.createTextNode(cell_el.value != null ? cell_el.value : '')
//             }}
//
//             cell.appendChild(text);
//         }
//     return table;
//     }






