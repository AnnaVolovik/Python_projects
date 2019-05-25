import React from  "react";


export default function JsonToTable(jsonData) {

    let data = jsonData.jsonData;

    // handle errors
    if ('error' in data) {
        return (<div className='error'>{data['error']}</div>);
    }

    // create columns based on the first object keys
    let cols = Object.keys(data[0]).map((col, index) => {
        return <th key={'th_'+ index}>{col}</th>
    });

    // create a number of rows equal to the data length
    let rows = [];
    for (let i=0; i<data.length; i++) {
        let row = Object.values(data[i]).map((val, index) => {
            return <td key={"td_"+i+'_'+index}>{val}</td>
        });
        rows.push(<tr key={'row_'+i}>{row}</tr>)
    }
    console.log(rows);

    return (
        <table>
            <thead><tr>{cols}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
        )
    }


