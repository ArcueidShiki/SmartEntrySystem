import React from 'react';
import './sideBar.css';

function SideBar({ setView, currentView }) {
  const navItems = [
    { id: 'display', icon: 'bi-display', label: 'Display' },
    { id: 'data', icon: 'bi-clipboard-data', label: 'Data' },
    { id: 'control', icon: 'bi-box-arrow-in-right', label: 'Control' }
  ];

  return (
    <aside className='sidebar'>
      <ul className='sidebar-nav' id='sidebar-nav'>
        {navItems.map((item) => (
          <li key={item.id} className='nav-item'>
            <button
              className={`nav-link ${currentView === item.id ? 'active' : ''}`}
              onClick={() => setView(item.id)}
            >
              <i className={`bi ${item.icon}`}></i>
              <span>{item.label}</span>
            </button>  
          </li>
        ))}
      </ul>
    </aside>
  );
}

export default SideBar;