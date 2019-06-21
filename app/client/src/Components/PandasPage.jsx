import React from 'react';

import DataframeToTable from './DataframeToTable';
import Header from './Header';
import NavBar from './NavBar';

import APIClient from '../apiClient';

export function returnDF (props) {

    if (props) {
        return <DataframeToTable df={props} />
    } else return <table></table>
}

export default class PandasPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            df: null,
            onlyGold: null,
            onlyGoldCount: null
        };
        this.getOnlyGoldResults = this.getOnlyGoldResults.bind(this);
    }

    async componentDidMount() {
        this.apiClient = new APIClient();
        this.apiClient.getPandasDataFrame().then((data) =>
            this.setState({...this.state, df: data})
        )
    }

    getOnlyGoldResults() {
        this.apiClient.getOnlyGoldResults().then((data) =>
            this.setState({
                onlyGold: data,
                onlyGoldCount: Object.keys(data).length
            })
        );
    }

    render() {
        return (
            <div>
            <NavBar />
                <section>
                    <Header
                        header="Pandas"
                        intro={<p>Study materials. Analyzing data in the csv file derived from the&nbsp;
                               <a href="https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table"
                                  target="_blank" rel="noopener noreferrer">
                                   All-time Olympic Games medal table Wikipedia</a>&nbsp;page with the help of:</p>}
                        skills={['pandas']}
                    />
                    <h4>Total National Olympic Committees with medals</h4>
                    {this.state.df ? <DataframeToTable df={this.state.df}/> : null}
                    <h4>Only National Olympic Committees with gold medals {this.state.onlyGoldCount ? ' - ' + this.state.onlyGoldCount : ''}</h4>
                    {returnDF(this.state.onlyGold)}
                    {this.state.onlyGold ? null : <input type="submit" value="See results" className="dark_button" onClick={this.getOnlyGoldResults}/>}
                </section>
            </div>
        )
    }
}