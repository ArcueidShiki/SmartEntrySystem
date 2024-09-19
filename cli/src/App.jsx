// import Bootstrap and icons
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';

import './App.css';
import Header from './components/header/Header';
import SideBar from './components/SideBar';
import Main from './components/dashboard/Main';

function App() {
  return (<>
    <Header/>
    <SideBar/>
    <Main/>
  </>
  )
}

export default App;
