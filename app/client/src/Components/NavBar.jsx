import React from "react";
import { NavLink } from "react-router-dom";


const styles = {
        display: 'inline-block',
        float: 'left',
        color: '#404040',
        textDecoration: 'none',
        marginBottom: '10px',
        marginRight: '5px'
    };


export default function NavBar () {
    return (
        <nav>
            <NavLink to='/' exact style={styles} activeClassName='active'>Home</NavLink>
            <NavLink to='/project_one' style={styles} activeClassName='active'>Project 1</NavLink>
            <NavLink to='/project_two' style={styles} activeClassName='active'>Project 2</NavLink>
            <NavLink to='/project_three' style={styles} activeClassName='active'>Project 3</NavLink>
            <NavLink to='/recursion' style={styles} activeClassName='active'>Recursion</NavLink>
            <NavLink to='/pandas' style={styles} activeClassName='active'>Pandas</NavLink>
        </nav>
    )
}