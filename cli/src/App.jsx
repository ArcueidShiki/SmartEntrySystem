import { useState } from 'react';

// import Bootstrap and icons
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';

import './App.css';
import Header from './components/header/Header';
import SideBar from './components/SideBar';
import Display from './components/main/Display';
import Data from './components/main/Data';
import Control from './components/main/Control';

function App() {
  const [currentView, setCurrentView] = useState('display');

  const renderView = () => {
    switch(currentView) {
      case 'display':
        return <Display />;
      case 'data':
        return <Data />;
      case 'control':
        return <Control />;
      default:
        return <Display />;
    }
  };

  return (<>
    <Header/>
    <SideBar setView={setCurrentView} currentView={currentView}/>
    <main className='main'>{renderView()}</main>
  </>
  )
}

export default App;
