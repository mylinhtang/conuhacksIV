"use client";

import React, { use, useEffect, useState } from "react";

const BaseStats = () => {
  // data to be fetched from backend
  //   const [data, setData] = useState(null);

  //   useEffect(() => {
  //     fetch("/api/python") // Calls the Next.js API route
  //       .then((res) => res.json())
  //       .then(setData)
  //       .catch((err) => console.error("Error fetching data:", err));
  //   }, []);

  return (
    <div className="bg-gray-200">
      <div className="container mx-auto mb-8">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <div className="grid grid-cols-4 gap-4 my-5">
          {/* call api from backend to display dynamically */}
          <div className="bg-white px-4 py-6 rounded-lg text-center">
            <h1 className="text-md font-bold pt-2">
              Total number of charging stations in Montreal
            </h1>
            <p className="pt-2 text-2xl">100</p>
          </div>
          <div className="bg-white p-4 rounded-lg text-center">
            <h1 className="text-md font-bold pt-2">
              Average air quality index in Montreal
            </h1>
            <p className="pt-2 text-2xl">1000</p>
          </div>
          <div className="bg-white p-4 rounded-lg text-center">
            <h1 className="text-md font-bold pt-2">
              Number of records for air quality in Montreal
            </h1>
            <p className="pt-2 text-2xl">10000</p>
          </div>
          <div className="bg-white p-4 rounded-lg text-center">
            <h1 className="text-md font-bold pt-2">
              Number of neighbourhood analyzed
            </h1>
            <p className="pt-2 text-2xl">10000</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BaseStats;
