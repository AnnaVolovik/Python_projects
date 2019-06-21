import React from "react";
import { NavLink } from "react-router-dom";
import NestedData from "./NestedData";


export default function NavBar () {
    return (
        <div id='nav'>
            <nav>
                <NavLink to='/' exact activeClassName='active'>Home</NavLink>
                <NavLink to='/webscraping' activeClassName='active'>WebScraping</NavLink>
                <NavLink to='/selenium' activeClassName='active'>Selenium</NavLink>
                <NavLink to='/aiohttp' activeClassName='active'>AIOhttp</NavLink>
                <NavLink to='/nested_data' activeClassName='active'>NestedData</NavLink>
                <NavLink to='/pandas' activeClassName='active'>Pandas</NavLink>
            </nav>
        </div>
    )
}