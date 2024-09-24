import React from 'react';
import { Column } from '@ant-design/plots';
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
    </div>
  );
}

export default Data;