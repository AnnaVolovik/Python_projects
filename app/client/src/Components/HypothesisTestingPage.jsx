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

export function generateHTML(props) {
    if (props) {
        return (
            <div>
                <div dangerouslySetInnerHTML={{ __html: props.code }}/>
                {props.result ? <pre><div dangerouslySetInnerHTML={{ __html: props.result }}/></pre> : null}
            </div>
        );
    } else return <div></div>
}

export default class HyphothesisTesting extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            df: null,
            function1: null
        };
    }

    async componentDidMount() {
        this.apiClient = new APIClient();
        this.apiClient.getCodeContentHypotesisTesting().then((data) =>
            this.setState(data)
        );
        console.log(this.setState.keys)
    }

    render() {
        return (
            <div>
            <NavBar />
                <section>
                    <Header
                        header="Data Analysis & Hypothesis Testing"
                        intro={
                        <p>Demonstrating the ability to acquire, manipluate, clean and run basic data analysis.
                        Providing evidence for (or against!) a given hypothesis as part of&nbsp;
                            <a href="https://www.coursera.org/learn/python-data-analysis"
                               target="_blank" rel="noopener noreferrer">
                                "Introduction to Data Science in Python"</a> Coursera course by University of Michigan.
                        </p>}
                        skills={['pandas', 'data analysis', 'ttest']}
                    />
                    <h4>Hypothesis:</h4>
                    <p>University towns have their mean housing prices less effected by
                        recessions. Run a t-test to compare the ratio of the mean price of houses in university
                        towns the quarter before the recession starts compared to the recession bottom.</p>
                    <h4>Definitions</h4>
                    <p>A <i>quarter</i> is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.</p>
                    <p>A <i>recession</i> is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.</p>
                    <p>A <i>recession bottom</i> is the quarter within a recession which had the lowest GDP.</p>
                    <p>A <i>university town</i> is a city which has a high percentage of university students compared to the total population of the city.</p>

                    <h4>Data</h4>
                    <p>The following data files are available</p>
                    <ul>

                        <li>From the Zillow research data site there is housing data for the United States.
                        In particular the datafile for all homes at a city level, <a href="..../static/City_Zhvi_AllHomes.csv">City_Zhvi_AllHomes.csv</a>,
                        has median home sale prices at a fine grained level.</li>
                        <li>From the Wikipedia page on college towns is a list of university towns in the United States
                            which has been copy and pasted into the file university_towns.txt.</li>
                        <li>From Bureau of Economic Analysis, US Department of Commerce, the GDP over time of the
                            United States in current dollars (use the chained value in 2009 dollars),
                            in quarterly intervals, in the file gdplev.xls. For this assignment, only look at GDP data
                            from the first quarter of 2000 onward.</li>
                    </ul>
                    <h4>1. Return a DataFrame of towns and the states  from the university_towns.txt list.</h4>
                    {generateHTML(this.state.get_list_of_university_towns)}
                    <h4>2. Return information about recession timeframes with the help of gdplev.xls on the GDP over
                        time of the United States from Bureau of Economic Analysis, US Department of Commerce,</h4>
                    <p>GDP Dataframe</p>
                    {generateHTML(this.state.get_gdp_data)}
                    <p>Helper function on location recession time frame, which is defined as starting with two consecutive quarters
                        of GDP decline, and ending with two consecutive quarters of GDP growth.</p>
                    {generateHTML(this.state.get_recession_start_or_end)}
                    <p>The recession start time defined with two consecutive quarters of GDP decline</p>
                    {generateHTML(this.state.get_recession_start)}
                    <p>The recession end time defined with two consecutive quarters of GDP growth</p>
                    {generateHTML(this.state.get_recession_end)}
                    <p>The recession bottom time -
                        the quarter within a recession which had the lowest GDP</p>
                    {generateHTML(this.state.get_recession_bottom)}
                    <h4>3. Convert the housing data to quarters and return it as mean values</h4>
                    {generateHTML(this.state.convert_housing_data_to_quarters)}
                    <h4>Run t-test and return the results </h4>
                    {generateHTML(this.state.run_ttest)}

                </section>
            </div>
        )
    }
}