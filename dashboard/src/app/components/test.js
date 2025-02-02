"use client"; // Marks this component as a client component

import { useState, useEffect } from "react";

export default function Home() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5004/api/data")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Network response was not ok");
        }
        return res.json();
      })
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching data:", err);
        setError(err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="p-8">
      <div className="container mx-auto">
        <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
        {loading && <p>Loading data...</p>}
        {error && <p className="text-red-500">Error: {error.message}</p>}
        {data && (
          <div className="grid grid-cols-4 gap-4 ">
            <div className="p-4 border shadow px-4 py-10 rounded-lg text-center bg-white hover:cursor-pointer hover:scale-105 transition-all duration-300">
              <h1 className="text-md font-bold">Total EV Charging Stations</h1>
              <p className="pt-2 text-md">{data.chargingStations}</p>
            </div>
            <div className="p-4 border px-4 py-10 rounded-lg text-center shadow bg-white hover:cursor-pointer hover:scale-105 transition-all duration-300">
              <h1 className="text-md font-bold">Average Air Quality Index</h1>
              <p className="pt-2 text-md">{data.AvgAirQuality}</p>
            </div>
            <div className="p-4 border px-4 py-10 rounded-lg text-center shadow bg-white hover:cursor-pointer hover:scale-105 transition-all duration-300">
              <h1 className="text-md font-bold">Number of Records (AQI)</h1>
              <p className="pt-2 text-md">{data.NumRecords}</p>
            </div>
            <div className="p-4 border px-4 py-10 rounded-lg text-center shadow bg-white hover:cursor-pointer hover:scale-105 transition-all duration-300">
              <h1 className="text-md font-bold">
                Number of Neighbourhoods analyzed
              </h1>
              <p className="pt-2 text-md">{data.NumNeighbourhoods}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
