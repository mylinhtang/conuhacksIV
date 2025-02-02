import React from "react";
import MapWrapper from "./MapWrapper";
import Image from "next/image";
import Diagram1 from "./Diagram1";

const Diagram = () => {
  return (
    <div>
      <div className="container mx-auto">
        <div className="flex justify-center gap-6">
          <div className=" w-[500px] h-[500px] border border-gray-300">
            <MapWrapper />
          </div>
          <div className="w-[500px] h-full border border-gray-300">
            <Diagram1 />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Diagram;
