import React from 'react';
import NavBar from './NavBar';

export default function Landing () {

        return (
            <div>
                {/*<LandingImage />*/}
                <NavBar/>
                <section>
                <header>
                    <h1>Portfolio</h1>
                    <h2>Anna Volovik</h2>
                </header>
                <p className="centered">
                    A series of projects on Python 3 & React in a single Flask app</p>
                <div className="column">
                    <h2>Screen</h2>
                    <p>Etiam porta sem malesuada magna mollis euismod. Integer posuere erat a ante venenatis dapibus posuere velit aliquet. Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum. Duis mollis, est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit.</p>
                </div>
                <div className="column">
                    <h2>Content</h2>
                    <p>Etiam porta sem malesuada magna mollis euismod. Integer posuere erat a ante venenatis dapibus posuere velit aliquet. Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum. Duis mollis, est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit.</p>
                </div>
                <div className="column">
                    <h2>Content</h2>
                    <p>Etiam porta sem malesuada magna mollis euismod. Integer posuere erat a ante venenatis dapibus posuere velit aliquet. Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum. Duis mollis, est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit.</p>
                </div>
            </section>
            </div>
        )
}