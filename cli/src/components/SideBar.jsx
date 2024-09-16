import React from 'react';
import './sideBar.css';

function SideBar() {
  return (
    <aside className='sidebar'>
        <ul className='sidebar-nav' id='sidebar-nav'>
            <li className='nav-item'>
                <a href='/' className='nav-link'>
                    <i className='bi bi-display'></i>
                    <span>Display</span>
                </a>
            </li>

            <li className='nav-item'>
                <a href='/' className='nav-link'>
                    <i className='bi bi-clipboard-data'></i>
                    <span>Data</span>
                </a>
            </li>

            <li className='nav-item'>
                <a href='/' className='nav-link'>
                    <i className='bi bi-box-arrow-in-right'></i>
                    <span>Control</span>
                </a>
            </li>
        </ul>
    </aside>
  )
}

export default SideBar