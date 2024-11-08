import React, { useState, useEffect } from 'react';
import './control.css';
import entranceClosed from '../../images/entrance_closed.png';
import entranceOpen from '../../images/entrance_open.png';
import micOff from '../../images/mic_off.png';
import micOn from '../../images/mic_on.png';

function Control() {
  const [isGateOpen, setIsGateOpen] = useState(false);
  const [isMicOn, setIsMicOn] = useState(false);

  useEffect(() => {
    // Fetch the initial state of the gate from the server
    fetch('/latest_prediction')
      .then(response => response.json())
      .then(data => {
        if (data.final_result === "Open the door") {
          setIsGateOpen(true);
        } else {
          setIsGateOpen(false);
        }
      })
      .catch(error => console.error('Error fetching initial gate status:', error));
  }, []);

  const toggleGate = () => {
    const newGateStatus = !isGateOpen;
    setIsGateOpen(newGateStatus);

    // Send the gate status to the backend
    fetch('/gate_control', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ gateOpen: newGateStatus }),
    })
      .then(response => response.json())
      .then(data => console.log('Gate status updated:', data))
      .catch(error => console.error('Error updating gate status:', error));
  };

  const toggleMic = () => {
    setIsMicOn(!isMicOn);
  };

  return (
    <div className="container">
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