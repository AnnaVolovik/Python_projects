import React from "react";
import { JsonToTable } from "react-json-to-table";


export default function TableData(jsonData) {
    let data = jsonData['jsonData']
    if ('error' in data) {
        return (<div className='error'>{data['error']}</div>);
    }
    return (
        <JsonToTable json={data} />
    )

}
