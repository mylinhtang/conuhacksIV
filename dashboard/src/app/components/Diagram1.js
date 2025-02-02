"use client";

import React, { useEffect, useState } from "react";
import { Scatter } from "react-chartjs-2";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  PointElement,
  Legend,
  LinearScale,
} from "chart.js";

ChartJS.register(Title, Tooltip, PointElement, Legend, LinearScale);

export default function Home() {
  const [chartData, setChartData] = useState(null);
  const [correlation, setCorrelation] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5004/api/graph-data")
      .then((res) => res.json())
      .then((data) => {
        const neighborhoods = data.data.map((d) => d.Neighborhood);
        const uniqueNeighborhoods = [...new Set(neighborhoods)];

        const datasets = uniqueNeighborhoods.map((neighborhood) => {
          const filteredData = data.data.filter(
            (d) => d.Neighborhood === neighborhood
          );

          return {
            label: neighborhood,
            data: filteredData.map((d) => ({
              x: d["Number of EV Charging Stations"],
              y: d["AVERAGE INDEX"],
            })),
            backgroundColor: `hsl(${Math.random() * 360}, 70%, 50%)`,
            pointRadius: 6,
          };
        });

        setChartData({
          datasets,
        });

        setCorrelation(data.correlation.toFixed(2));
      })
      .catch((error) => console.error("Error fetching graph data:", error));
  }, []);

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-gray-100">
      <h1 className="text-2xl font-bold mb-4 text-center">
        Correlation Between Air Quality & EV Stations
      </h1>
      {chartData ? (
        <>
          <Scatter
            data={chartData}
            options={{
              responsive: true,
              scales: {
                x: {
                  type: "linear",
                  position: "bottom",
                  title: {
                    display: true,
                    text: "Number of EV Charging Stations",
                  },
                },
                y: {
                  title: {
                    display: true,
                    text: "Average Air Quality Index",
                  },
                },
              },
              plugins: {
                legend: {
                  labels: {
                    usePointStyle: true, // Makes the legend use round points
                    pointStyle: "circle", // Ensures round shapes in the legend
                    boxWidth: 5, // Adjusts the size of the round marker
                    boxHeight: 5, // Helps maintain proportionality
                  },
                },
              },
            }}
          />
          <p className="mt-4 text-lg">
            Pearson Correlation Coefficient: {correlation}
          </p>
        </>
      ) : (
        <p>Loading chart...</p>
      )}
    </div>
  );
}
