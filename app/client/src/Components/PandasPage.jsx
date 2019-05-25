import React from 'react';
import NavBar from './NavBar';
import ListSkills from './ListSkills';

import APIClient from '../apiClient';


export default class PandasPage extends React.Component {
    state = {};

    async componentDidMount() {
        this.apiClient = new APIClient();
        this.apiClient.getPandasDataFrame().then((data) =>
            this.setState({...this.state, df: data})
        )
    }
    render() {
        return (
            <div>
            <NavBar />
                <section>
                    <h2>Pandas</h2>
                    <p>Study materials. Analyzing data in the
                        <a href="{{ url_for('static', filename='olympics.csv') }}" >csv</a>
                        file derived from the
                        <a href="https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table">
                            All-time Olympic Games medal table Wikipedia</a> page with the help of:</p>
                        <ListSkills skills={['pandas']}/>

                </section>

            </div>
        )
    }
}