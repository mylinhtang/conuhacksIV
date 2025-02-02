"use client";

import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function MapComponent() {
  const [geoData, setGeoData] = useState(null);

  useEffect(() => {
    fetch("/boroughs.geojson")
      .then((response) => response.json())
      .then((data) => setGeoData(data))
      .catch((error) => console.error("Error fetching GeoJSON:", error));
  }, []);

  return (
    <MapContainer
      center={[45.5, -73.8]}
      zoom={12}
      scrollWheelZoom={true}
      className="w-full h-full" // ensure it fills the container
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {geoData && <GeoJSON data={geoData} />}
    </MapContainer>
  );
}
