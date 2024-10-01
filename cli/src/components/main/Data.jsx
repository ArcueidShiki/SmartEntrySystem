import React, { useEffect, useState } from 'react';
import { Column } from '@ant-design/plots';
import { forEach, groupBy } from 'lodash';
import maskData from '../../data/mask_data.json';
import tempData from '../../data/temp_data.json';
import './data.css';

function Data() {
  const [maskChartData, setMaskChartData] = useState([]);
  const [tempChartData, setTempChartData] = useState([]);

  useEffect(() => {
    setMaskChartData(maskData);
    setTempChartData(tempData);
  }, []);

  // Function to create annotations
  const createAnnotations = (data) => {
    const annotations = [];
    forEach(groupBy(data, 'date'), (values, k) => {
      const value = values.reduce((a, b) => a + b.value, 0);
      annotations.push({
        type: 'text',
        data: [k, value],
        style: {
          textAlign: 'center',
          fontSize: 14,
          fill: 'rgba(0,0,0,0.85)',
        },
        xField: 'date',
        yField: 'value',
        style: {
          text: `${value}`,
          textBaseline: 'bottom',
          position: 'top',
          textAlign: 'center',
        },
        tooltip: false,
      });
    });
    return annotations;
  };

  const chartConfig = {
    xField: 'date',
    yField: 'value',
    stack: true,
    colorField: 'type',
    label: {
      text: 'value',
      textBaseline: 'bottom',
      position: 'inside',
    },
  };

  const maskConfig = {
    ...chartConfig,
    data: maskChartData,
    annotations: createAnnotations(maskChartData),
  };

  const tempConfig = {
    ...chartConfig,
    data: tempChartData,
    annotations: createAnnotations(tempChartData),
  };

  return (
    <div className="charts-container">
      <div className="chart-wrapper">
        <h2>Mask Data Visualization</h2>
        <Column {...maskConfig} />
      </div>
      <div className="chart-wrapper">
        <h2>Temperature Data Visualization</h2>
        <Column {...tempConfig} />
      </div>
    </div>
  );
}

export default Data;