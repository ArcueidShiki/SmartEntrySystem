import React, { useEffect, useState } from 'react';
import { Column, Pie } from '@ant-design/plots';
import { forEach, groupBy } from 'lodash';
// import maskData from '../../data/mask_data.json';
// import tempData from '../../data/temp_data.json';
import maskData from '../../data/mask_data_test.json';
import tempData from '../../data/temp_data_test.json';
import dailyEntriesData from '../../data/daily_entry_test.json';
import dailyTempData from '../../data/daily_temp_test.json';
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

const pieChartConfig1 = {
    data: dailyEntriesData.data,
    angleField: 'value',
    colorField: 'type',
    radius: 0.8,
    label: {
      text: (d) => `${d.type}\n ${d.value}`,
      position: 'spider',
    },
    legend: {
      color: {
        title: false,
        position: 'right',
        rowPadding: 5,
      },
    },
  };

const pieChartConfig2 = {
    data:dailyTempData.data,
    angleField: 'value',
    colorField: 'temperature',
    legend: false,
    innerRadius: 0.6,
    labels: [
      { text: 'temperature', style: { fontSize: 10, fontWeight: 'bold' } },
      {
        text: (d, i, data) => (i < data.length - 3 ? d.value : ''),
        style: {
          fontSize: 9,
          dy: 12,
        },
      },
    ],
    style: {
      stroke: '#fff',
      inset: 1,
      radius: 10,
    },
    scale: {
      color: {
        palette: 'spectral',
        offset: (t) => t * 0.8 + 0.1,
      },
    },
  };

return (
  <div className="charts-container">
    {/* Upper Section with two column charts */}
    <div className="upper-section">
      <div className="chart-wrapper">
        <h2>Mask Data Visualization</h2>
        <Column {...maskConfig} />
      </div>
      <div className="chart-wrapper">
        <h2>Temperature Data Visualization</h2>
        <Column {...tempConfig} />
      </div>
    </div>

    {/* Lower Section with two pie charts */}
    <div className="lower-section">
      <div className="chart-wrapper">
        <h2>Daily Entries Chart</h2>
        <Pie {...pieChartConfig1} />
      </div>
       <div className="chart-wrapper">
        <h2>Daily Temperature Distribution</h2>
        <Pie {...pieChartConfig2} />
      </div>
    </div>
  </div>
);

}

export default Data;