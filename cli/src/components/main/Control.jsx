import React, { useState } from 'react';
import './control.css';
import entranceClosed from '../../images/entrance_closed.png';
import entranceOpen from '../../images/entrance_open.png';
import micOff from '../../images/mic_off.png';
import micOn from '../../images/mic_on.png';

function Control() {
  const [isGateOpen, setIsGateOpen] = useState(false);
  const [isMicOn, setIsMicOn] = useState(false);

  const toggleGate = () => {
    setIsGateOpen(!isGateOpen);
  };

  const toggleMic = () => {
    setIsMicOn(!isMicOn);
  };

  return (
    <div className="container">
      <h1 className="mb-4">Control</h1>
      <div className="row justify-content-center">
        <div className="col-md-4 text-center">
          <img
            src={isGateOpen ? entranceOpen : entranceClosed}
            alt={isGateOpen ? "entrance open" : "entrance closed"}
            className="control-image"
          />
          <button 
            className="btn btn-outline-primary mt-3 control-button"
            onClick={toggleGate}
          >
            {isGateOpen ? "CLOSE GATE" : "OPEN GATE"}
          </button>
        </div>
        <div className="col-md-4 text-center">
          <img
            src={isMicOn ? micOn : micOff}
            alt={isMicOn ? "microphone on" : "microphone off"}
            className="control-image"
          />
          <button 
            className="btn btn-outline-primary mt-3 control-button"
            onClick={toggleMic}
          >
            {isMicOn ? "MIC OFF" : "MIC ON"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Control;