import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header style={{ padding: '1rem', backgroundColor: '#f8f9fa', borderBottom: '1px solid #e9ecef' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Link to="/" style={{ fontSize: '1.5rem', fontWeight: 'bold', textDecoration: 'none', color: '#333' }}>
          BigSignal
        </Link>
        <nav style={{ display: 'flex', gap: '1rem' }}>
          <Link to="/" style={{ textDecoration: 'none', color: '#333' }}>홈</Link>
          <Link to="/analysis" style={{ textDecoration: 'none', color: '#333' }}>분석 결과</Link>
          <a href="https://t.me/bigsignal_ai" target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none', color: '#007bff' }}>
            텔레그램
          </a>
        </nav>
      </div>
    </header>
  );
};

export default Header;