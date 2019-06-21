import React from "react";

import Header from './Header';
import NavBar from './NavBar';
import JsonToTable2 from './JsonToTable2';

import APIClient from '../apiClient';

function CodePiece(props) {
    return (
        <div className={props.className}>
            <h3>{props.heading}</h3>
                <p>{props.content}</p>
                <code><pre>{props.code}</pre></code>
        </div>
    )
}

function RestructuredData(props) {
    return (
        <div>
            <h3>Restructured data</h3>
            <CodePiece
                heading="" content="Cells" className="column"
                code={props.content.cells ? JSON.stringify(props.content.cells, null, 4) : ''} />
            <CodePiece
                heading="" content="Columns" className="column"
                code={props.content.columns ? JSON.stringify(props.content.columns, null, 4) : ''} />
            <CodePiece
                heading="" content="Rows" className="column"
                code={props.content.rows ? JSON.stringify(props.content.rows, null, 4) : ''} />
        <h3>Table-like form</h3>
            <JsonToTable2 data={props.content}/>
        </div>

    )
}

export default class NestedData extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            content: null,
            header: null,
            result: null
        };
        this.restructureTreeLikeData = this.restructureTreeLikeData.bind(this);
    }


    async componentDidMount() {
        this.apiClient = new APIClient();
        this.apiClient.getTreeLikeContent().then((data) =>
            this.setState({
                content: data['content'],
                structure: data.structure
            })
        )
    }

    restructureTreeLikeData() {
        this.apiClient.restructureTreeLikeData().then((data) =>
            this.setState({
                result: data
            })
        )
    }

    render() {
        return (
            <div>
            <NavBar />
                <section>
                    <Header
                        header="Nested data and recursion"
                        intro=
                            {<div>
                                <p><b>Problem statement</b></p>
                                <p>Based on hierarchical data, table-like interfaces had to be created on the client side.</p>
                                <p>Input data, both, content and information on the multi-level header, might have
                                    been organized either flat or hierarchically: in a few layers, where each layer
                                    would be a root node for the collection of children nodes, with objects being
                                    stored inside of similar objects and actual data available on the deepest level
                                    in the leaf (see the example below).</p>
                                <p>The process of rendering such data on the client size would take up to 40 seconds,
                                    therefore it was decided to take data processing to the backend.</p>
                            </div>}
                        skills={[]}
                    />
                    <div>
                    <CodePiece heading="Content example"
                               content="Hierarchy, with actual content hidden in the child nodes"
                               className="column_45"
                               code={this.state.content ? JSON.stringify(this.state.content, null, 4) : ''}

                    />
                    <CodePiece heading="Header information"
                               content="Information on output structure that might be hierarchical as well"
                               className="column_45"
                               code={this.state.content ? JSON.stringify(this.state.structure, null, 4) : ''}
                           />
                    </div>

    <div>
        <p>The goal was to return the data in the ready-to-use form: a matrix with information about:</p>
            <ul>
                <li>each cell: its position vertically and horizontally, value;</li>
                <li>each column: position, data type, and display properties;</li>
                <li>each row: position, its parent and children rows, indentation level;</li>
                <li>information about the table in general: number of rows and columns, including fixed ones, etc.</li>
            </ul>
        <p>All computations on the backend were made in a single iteration, using recusion and keeping track of the
            of the row/column numbers, assigning correct order, aggregating values and display attributes on the go.</p>
        <p>Logic included:</p>
        <ul>
            <li>aggregating values on all levels of parent nodes for different types of data: sum, avg, max, min for
                numbers, count for bools;</li>
            <li>assigning correct type  to be rendered on the front end  based on the data type, column type and set of
                conditions (example - boolen type & editable line would return CheckBox type, boolean type & not
                editable line - disabledCheckBox, etc);</li>
            <li>computing values display - based on display parameter it would be required to return the value
                short description, long description, code, etc</li>
            <li>defining style attributes - cell colors (based on set of conditions), column width etc</li>
        </ul>
        <p>With the data being passed to the front-end as a ready to use matrix, we achieved 1-6 seconds time for
            loading the form.</p>
        {this.state.result ? <RestructuredData content={this.state.result} /> :
            <input type="submit" value="Restructure" className="dark_button" onClick={this.restructureTreeLikeData}/>}

    </div>
    </section>
    </div>)
    }

}
