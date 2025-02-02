import React from "react";
import MapWrapper from "./MapWrapper";
import Image from "next/image";

const Diagram = () => {
  return (
    <div>
      <div className="container mx-auto">
        <div className="flex justify-center gap-6">
          <div className=" w-[500px] h-[500px] border border-gray-300">
            <MapWrapper />
          </div>
          <div>
            <Image
              src="/images/graph.png"
              alt="image1"
              width={480}
              height={680}
              className="m-2"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Diagram;
