import React from 'react'
import icon from './icon.svg';

export default class FormSubmission extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return  (
            <section class="section">
                <form action="/buscar" method="POST">
                    <input type="search" name="buscar" id="search" placeholder="O que deseja assistir?">
                    <button type="submit" class="btn_submit">
                        <img class="img_search" src="{icon}" alt="icon">
                    </button>
                </form>
            </section>
        );
    }
}





