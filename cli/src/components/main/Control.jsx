import React from 'react';
import './control.css';
import entranceClosed from '../../images/entrance_closed.png';
import micOff from '../../images/mic_off.png';

function Control() {
  return (
    <div className="container">
      <h1 className="mb-4">Control</h1>
      <div className="row justify-content-center">
        <div className="col-md-4 text-center">
          <img
            src={entranceClosed}
            alt="entrance closed"
            className="control-image"
          />
          <button className="btn btn-outline-primary mt-3 control-button">GATE</button>
        </div>
        <div className="col-md-4 text-center">
          <img
            src={micOff}
            alt="microphone off"
            className="control-image"
          />
          <button className="btn btn-outline-primary mt-3 control-button">MIC</button>
        </div>
      </div>
    </div>
  );
}

export default Control;