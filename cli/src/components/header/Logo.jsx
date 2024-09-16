 import React from 'react';
import './logo.css';
import smartLogo from '../../images/logo.png'

function Logo() {
  return (
    <div className='logo d-flex align-items-center justify-content-between'>
        <img src={smartLogo} alt='logo' className='logo-image'/>
        <span className='d-none d-lg-block'>Smart Entry System Admin Dashboard</span>
    </div>
  )
}

export default Logo