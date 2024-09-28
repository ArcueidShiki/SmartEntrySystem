import React from 'react';
import './header.css';
import Logo from './Logo';
import Login from './Login';

function Header() {
  return (
    <header id='header' className='header fixed-top d-flex align-items-center'>
    {/* {logo} */}
    <Logo />
    {/* {mic and login in button} */}
    <Login />
    </header>
  )
}

export default Header