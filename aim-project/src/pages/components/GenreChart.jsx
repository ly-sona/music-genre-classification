// src/pages/components/GenreChart.jsx
import React from 'react';
import Chart from "react-apexcharts";
import PropTypes from 'prop-types';

const GenreChart = ({ genres }) => {
  const genreNames = genres.map(genre => genre.name);
  const confidenceData = genres.map(genre => genre.confidence);

  const chartConfig = {
    type: "bar",
    height: 240,
    series: [
      {
        name: "Confidence",
        data: confidenceData,
      },
    ],
    options: {
      chart: {
        toolbar: {
          show: false,
        },
      },
      title: {
        text: "", // Removed title as it's handled outside
      },
      dataLabels: {
        enabled: false,
      },
      colors: ["#c084fc"],
      plotOptions: {
        bar: {
          columnWidth: "40%",
          borderRadius: 2,
        },
      },
      xaxis: {
        axisTicks: {
          show: false,
        },
        axisBorder: {
          show: false,
        },
        labels: {
          style: {
            colors: "#616161",
            fontSize: "12px",
            fontFamily: "inherit",
            fontWeight: 400,
          },
        },
        categories: genreNames,
      },
      yaxis: {
        labels: {
          style: {
            colors: "#616161",
            fontSize: "12px",
            fontFamily: "inherit",
            fontWeight: 400,
          },
          formatter: function (value) {
            return value + "%";
          },
        },
        min: 0,
        max: 100,
      },
      grid: {
        show: true,
        borderColor: "#dddddd",
        strokeDashArray: 5,
        xaxis: {
          lines: {
            show: true,
          },
        },
        padding: {
          top: 5,
          right: 20,
        },
      },
      fill: {
        opacity: 0.8,
      },
      tooltip: {
        theme: "dark",
        y: {
          formatter: function (val) {
            return val + "%";
          },
        },
      },
    },
  };

  return (
    <div className="border-0 shadow-none"> {/* Ensures no border or shadow */}
      <Chart {...chartConfig} />
    </div>
  );
};

GenreChart.propTypes = {
  genres: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      confidence: PropTypes.number.isRequired,
    })
  ).isRequired,
};

export default GenreChart;

