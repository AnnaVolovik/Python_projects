import React from "react";

import APIClient from '../apiClient';
import NavBar from './NavBar';
import Header from './Header';
import JsonToTable from './JsonToTable';

export default class AioHttp extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            url: 'https://www.houzz.com/professionals/architect/c/Woodbridge--ON',
            entries: []
        };
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        event.preventDefault();
        this.apiClient = new APIClient();
        this.apiClient.submitAioHttpPage().then((data) =>
            this.setState({
                entries: data
            })
        );
        console.log(this.state.entries);
    }

    render() {
        return (
            <div>
            <NavBar />
                <section>
                    <Header header="asyncIO & AIOHTTP"
                            intro={<p>A web parser that helps gather information on&nbsp;
                                <a href={this.state.url} target="_blank" rel="noopener noreferrer">
                                    architecture companies</a>, that demontrates using asynchronous libraries
                                to speed up I/O operations:</p>}
                            skills={['asyncio', 'aiohttp']}
                    />
                    <form onSubmit={this.handleSubmit}>
                        <label>
                            <input type="text" placeholder={this.state.url} value={this.state.value} />
                            <input type="submit" value="Submit"  className="dark_button"/>
                        </label>
                    </form>
                    {(typeof this.state.entries !== 'undefined' && this.state.entries.length > 0) ? <JsonToTable jsonData={this.state.entries}/> : null}
                    </section>
            </div>
        )
    }

}