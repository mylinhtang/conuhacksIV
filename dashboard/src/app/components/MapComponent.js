// File: components/MapComponent.jsx
"use client";

import React, { useEffect, useState, useRef } from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

export default function MapComponent() {
  const [geoData, setGeoData] = useState(null);
  // regionInfoMapping maps a region name (as in the GeoJSON property) to extra info.
  const [regionInfoMapping, setRegionInfoMapping] = useState({});
  // hoveredInfo holds the extra info for the region currently hovered.
  const [hoveredInfo, setHoveredInfo] = useState(null);
  const geoJsonLayerRef = useRef();

  // Fetch the GeoJSON data for the map regions.
  useEffect(() => {
    fetch("/boroughs.geojson")
      .then((response) => response.json())
      .then((data) => setGeoData(data))
      .catch((error) => console.error("Error fetching GeoJSON:", error));
  }, []);

  // Fetch region extra info from the Python back‑end.
  useEffect(() => {
    // Change the URL if your Flask server is hosted elsewhere.
    fetch("http://localhost:5004/region-info")
      .then((response) => response.json())
      .then((data) => {
        // Convert the array data into an object for quick lookup.
        // Each item in data is: [regionName, chargingStations, airQualityIndex]
        const infoMap = {};
        data.forEach(([name, chargingStations, airQualityIndex]) => {
          infoMap[name] = { chargingStations, airQualityIndex };
        });
        setRegionInfoMapping(infoMap);
      })
      .catch((error) => console.error("Error fetching region info:", error));
  }, []);

  // Define a default style for each GeoJSON feature.
  const defaultStyle = {
    fillColor: "#3388ff",
    weight: 2,
    opacity: 1,
    color: "white",
    fillOpacity: 0.5,
  };

  // Attach event listeners to each GeoJSON feature.
  const onEachFeature = (feature, layer) => {
    // Apply the default style.
    layer.setStyle(defaultStyle);

    layer.on({
      mouseover: (e) => {
        const target = e.target;
        // Update the style on hover.
        target.setStyle({
          weight: 4,
          color: "#666",
          fillOpacity: 0.7,
        });

        // Bring the hovered feature to front.
        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
          target.bringToFront();
        }

        // Optionally, apply a CSS transform for a scale effect.
        const path = target._path;
        if (path) {
          path.style.transition = "transform 0.3s";
          path.style.transform = "scale(1.05)";
        }

        // Retrieve the region name from the GeoJSON feature (adjust property name if needed).
        const regionName = feature.properties.NOM;
        // Look up extra info from our regionInfoMapping.
        const regionExtraInfo = regionInfoMapping[regionName];

        // Update the hoveredInfo state.
        setHoveredInfo({
          name: regionName,
          chargingStations: regionExtraInfo
            ? regionExtraInfo.chargingStations
            : "N/A",
          airQualityIndex: regionExtraInfo
            ? regionExtraInfo.airQualityIndex
            : "N/A",
        });
      },
      mouseout: (e) => {
        const target = e.target;
        // Reset the style.
        if (geoJsonLayerRef.current) {
          geoJsonLayerRef.current.resetStyle(target);
        }
        // Reset the transform.
        const path = target._path;
        if (path) {
          path.style.transform = "scale(1)";
        }
        // Clear the hovered info.
        setHoveredInfo(null);
      },
    });
  };

  return (
    <div className="relative w-full h-full">
      <MapContainer
        center={[45.5, -73.8]}
        zoom={12}
        scrollWheelZoom={true}
        className="w-full h-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {geoData && (
          <GeoJSON
            data={geoData}
            style={defaultStyle}
            onEachFeature={onEachFeature}
            ref={geoJsonLayerRef}
          />
        )}
      </MapContainer>

      {/* Information overlay displayed when hovering over a region */}
      {hoveredInfo && (
        <div
          className="absolute top-4 left-4 bg-white p-4 shadow-lg rounded-md pointer-events-none"
          style={{ zIndex: 1000 }}
        >
          <h2 className="font-bold text-lg mb-2">{hoveredInfo.name}</h2>
          <p>
            <strong>Number of charging stations:</strong>{" "}
            {hoveredInfo.chargingStations}
          </p>
          <p>
            <strong>Average air quality index:</strong>{" "}
            {hoveredInfo.airQualityIndex}
          </p>
        </div>
      )}
    </div>
  );
}
