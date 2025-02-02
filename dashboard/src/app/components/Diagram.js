import React from "react";
import MapWrapper from "./MapWrapper";

const Diagram = () => {
  return (
    <div>
      <div className="container mx-auto">
        <div className=" w-96 h-96 border border-gray-300">
          <MapWrapper />
        </div>
      </div>
    </div>
  );
};

export default Diagram;
