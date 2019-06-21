import React from "react";
import ListSkills from './ListSkills';

export default function Header(props) {

    return (
        <div>
            <h2>{props.header}</h2>
            {props.intro}
            <ListSkills skills={props.skills} />
        </div>
    )
}