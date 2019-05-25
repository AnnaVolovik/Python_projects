import React from "react";

export default function ListSkills(props) {

    let skills = props.skills
    let skillsListed = skills.map((skill, index) =>
            <li key={index}>{skill}</li>);

    return (<ul>{skillsListed}</ul>)
};