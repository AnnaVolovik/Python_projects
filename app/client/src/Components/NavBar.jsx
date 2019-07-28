import React from "react";
import { NavLink } from "react-router-dom";
import NestedData from "./NestedData";
import HyphothesisTesting from "./HypothesisTestingPage";


export default function NavBar () {
    return (
        <div id='nav'>
            <nav>
                <NavLink to='/' exact activeClassName='active'>Home</NavLink>
                <NavLink to='/hyphothesistesting' activeClassName='active'>Hyphothesis Testing</NavLink>
                <NavLink to='/pandas' activeClassName='active'>Pandas</NavLink>
                <NavLink to='/nested_data' activeClassName='active'>NestedData</NavLink>
                <NavLink to='/aiohttp' activeClassName='active'>AIOhttp</NavLink>
                <NavLink to='/selenium' activeClassName='active'>Selenium</NavLink>
                <NavLink to='/webscraping' activeClassName='active'>WebScraping</NavLink>
            </nav>
        </div>
    )
}