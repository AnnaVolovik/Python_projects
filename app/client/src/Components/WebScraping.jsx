import React from 'react';

import Header from './Header';
import NavBar from './NavBar';
import JsonToTable from './JsonToTable';
import APIClient from '../apiClient';


export default class WebScraping extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            parsedLine: null,
            showAllEntries: false,
            value: ''
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.addEntry = this.addEntry.bind(this);
        this.showEntries = this.showEntries.bind(this);
        this.returnResult = this.returnResult.bind(this);
    }

    handleChange(event) {
        this.setState({value: event.target.value});

    }

    handleSubmit(event) {
        event.preventDefault();
        let value = {url: this.state.value};
        this.apiClient = new APIClient();
        this.apiClient.addEntryProjectOne(value).then((data) =>
            this.setState({
                parsedLine: data,
                showAllEntries: false
            })
        );
    }

    addEntry() {
        this.setState({
            parsedLine: null,
            showAllEntries: false
        })
    }

    showEntries() {
        this.apiClient = new APIClient();
        this.apiClient.showEntriesProjectOne().then((data) =>
            this.setState({
                parsedLine: data,
                showAllEntries: true
            })
        );
    }

    returnResult() {
        if (this.state.parsedLine) {
            if ('error' in this.state.parsedLine) {
                return (<div className='error'>{this.state.parsedLine.error}</div>);
            } else return <JsonToTable jsonData={this.state.parsedLine} />
        }
    }

    render() {
        return (
            <div>
            <NavBar />
                <section>
                    <Header header="Web Scraping"
                            intro="A simple web parser that either computes a number of tags in the url provided or returns an exception"
                            skills={['requests & BeautifulSoup', 'SQLAlchemy']} />
                    <div>
                        <button key='add_entry' onClick={this.addEntry}>add entry</button>
                        <button key='show_entries' onClick={this.showEntries}>show entries</button>
                    </div>
                    <form onSubmit={this.handleSubmit}>
                        <label>
                            <input type="text" value={this.state.value} onChange={this.handleChange}/>
                            <input type="submit" value="Submit" className="dark_button"/>
                        </label>
                    </form>
                    {this.returnResult()}
                    </section>
            </div>
        )
    }
}