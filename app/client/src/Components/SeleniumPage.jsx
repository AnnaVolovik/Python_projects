import React from 'react';

import APIClient from '../apiClient';
import NavBar from './NavBar';
import Header from './Header';
import JsonToTable from './JsonToTable';

export default class SeleniumPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            url: 'https://www.103.ua/list/stomatologii/kiev/',
            entries: []
        };
        this.handleSubmit = this.handleSubmit.bind(this);
    }


    handleSubmit(event) {
        event.preventDefault();
        this.apiClient = new APIClient();
        this.apiClient.submitSeleniumPage().then((data) =>
            this.setState({
                entries: data
            })
        );
    }

    render() {
        return (
            <div>
            <NavBar />
                <section>
                    <Header header="Web Scraping: Selenium"
                            intro={<p>A parser that helps collecting contact information from the clinic's aggregator&nbsp;
                            <a href="https://www.103.ua/list/stomatologii/kiev/" target="_blank" rel="noopener noreferrer">website</a>
                             &nbsp;with the help of:</p>}
                            skills={[
                                'Selenium - to open and close pop up windows where necessary',
                                'Requests library is used as a backup',
                                'BeautifulSoup - for parsing HTML pages',
                                'SQLAlchemy - to save results to the database',
                                'openpyxl library - for exporting results into MS Excel spreadsheet']}
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