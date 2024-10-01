import React, { useEffect, useState } from 'react';
import { Pie } from '@ant-design/plots';

const MaskPieChart = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      // Fetch your data from API or use dummy data
      const result = await fetch('url-to-your-api');
      const chartData = await result.json();
      setData(chartData);
    };

    fetchData();
    const interval = setInterval(fetchData, 60000); // fetch data every minute for real-time updates
    return () => clearInterval(interval);
  }, []);

  const config = {
    appendPadding: 10,
    data,
    angleField: 'value',
    colorField: 'type',
    radius: 0.9,
    label: {
      type: 'inner',
      offset: '-30%',
      content: ({ percent }) => `${(percent * 100).toFixed(0)}%`,
      style: {
        fontSize: 14,
        textAlign: 'center',
      },
    },
    interactions: [
      { type: 'element-active' },
    ],
  };

  return <Pie {...config} />;
};

export default MaskPieChart;
