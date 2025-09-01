import React from 'react';

const Header = () => {
    return (
        <header>
            <h1>BigSignal</h1>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/portfolio">Portfolio</a></li>
                    <li><a href="/trades">Trades</a></li>
                    <li><a href="/analysis">Analysis</a></li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;