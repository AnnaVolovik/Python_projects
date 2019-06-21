import React from "react";


export default function DataframeToTable(df) {

    let data = df.df;
    let col_names = [];
    let cols = Object.keys(data).map((col, index) =>
        {
            col_names.push(col);
            return <th className='theader' key={'th_'+(index+1)}>{col}</th>
        });
    // add first empty column
    cols.unshift(<th key='th_0'></th>);

    // rows
    let rows = [];
    for (let i=0; i<Object.keys(data[col_names[0]]).length; i++) {
        let row = [];
        for (var col_name of col_names) {
            row.push(<td key={'td_' + i + '_' + col_name}>{data[col_name][Object.keys(data[col_name])[i]]}</td>)
        }
        row.unshift(<td key={'td_' + -1 + '_' + col_name}>{Object.keys(data[col_name])[i]}</td>);
        rows.push(<tr key={'tr_' + i}>{row}</tr>)
    }

    return (
        <div id="table-wrapper">
            <div id="table-scroll">
                <table>
                    <thead><tr>{cols}</tr></thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
        </div>
    )

}