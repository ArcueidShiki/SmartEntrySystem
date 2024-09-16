import React from 'react';
import './pageContent.css'
import mask from '../../images/Mask-Detection.png'
import { useEffect, useState } from 'react';


function PageContent() {
  return (
    <div className="dashboard">
      <div className="upper-section">
        <h1>Display real time image/video</h1>
        <img src={mask} alt="" />
      </div>

      <div className="lower-section">
        <div className="text-box"><h2>Temperature: </h2></div>
        <div className="text-box"><h2>Mask: </h2></div>
      </div>
    </div>
  )
}

export default PageContent