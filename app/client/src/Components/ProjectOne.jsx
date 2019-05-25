import React from 'react';

import NavBar from './NavBar';
import ListSkills from './ListSkills';
import JsonToTable from './JsonToTable';
import APIClient from '../apiClient';


export default class ProjectOne extends React.Component {

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
        )
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

    render() {
        return (
            <div>
            <NavBar />
                <section>
                    <h2>Web Parsing</h2>
                    <p>A simple web parser that computes a number of tags in the url provided or returns an exception</p>
                    <ListSkills skills={['requests & BeautifulSoup', 'SQLAlchemy']} />
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
                    {this.state.parsedLine ? <JsonToTable jsonData={this.state.parsedLine}/> : null}
                    </section>
            </div>
        )
    }
}