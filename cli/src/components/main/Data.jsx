import React from 'react';
import { Column } from '@ant-design/plots';
import MaskPieChart from './MaskPieChart';  // Ensure the path is correct
import HourlyMaskBarChart from './HourlyMaskBarChart';  // Ensure the path is correct
import './data.css';

function Data() {
  const config = {
    data: {
      type: 'fetch',
      value: 'https://render.alipay.com/p/yuyan/180020010001215413/antd-charts/column-column.json',
    },
    xField: 'letter',
    yField: 'frequency',
    label: {
      text: (d) => `${(d.frequency * 100).toFixed(1)}%`,
      textBaseline: 'bottom',
    },
    axis: {
      y: {
        labelFormatter: '.0%',
      },
    },
    style: {
      radiusTopLeft: 10,
      radiusTopRight: 10,
    },
  };

  return (
    <div className="data-container">
      <h2>Data Visualization</h2>
      <Column {...config} />
      <h2>Mask Usage Overview</h2>
      <MaskPieChart />
      <h2>Hourly Mask Usage</h2>
      <HourlyMaskBarChart />
    </div>
  );
}

export default Data;

