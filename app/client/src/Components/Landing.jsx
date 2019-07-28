import React from 'react';
import NavBar from './NavBar';
import ListSkills from './ListSkills';

export default function Landing () {

        return (
            <div>
                {/*<LandingImage />*/}
                <NavBar/>
                <section>
                <header>
                    <h2>Anna Volovik</h2>
                </header>

                <p className="centered">
                    A series of projects on Python 3 & React in a single Flask app</p>
                <div className="column">
                    <h3>Data analysis</h3>
                    <p>Demonstrating the ability to acquire, manipluate, clean and run basic data analysis
                        with pandas - probably the most popular library for
                        data analysis in Python programming language.</p>
                    <ListSkills skills={['pandas', 'data analysis', 'hypothesis testing']}/>
                </div>
                    <div className="column">
                    <h3>NESTED DATA</h3>
                    <p>Using recursion to restructure tree-like data into ready-to-use table-like format.</p>
                    <ListSkills skills={["recursion"]}/>
                </div>
                    <div className="column">
                    <h3>Web Scraping</h3>
                    <p>Example parsing web sites & exporting data to database / excel spreadsheet, using </p>
                    <ListSkills skills={['Requests', 'BeautifulSoup', 'Selenium', 'asyncio', 'aiohttp', 'SQLAlchemy', 'openpyxl']} />
                </div>


            </section>
            </div>
        )
}