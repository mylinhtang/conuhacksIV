import React from "react";
import { RxDashboard } from "react-icons/rx";
import Image from "next/image";

const Navbar = () => {
  return (
    <div className="bg-gray-200">
      <div className="flex justify-between items-center bg-blue-200 p-4 w-full shadow-md mb-5">
        <div className="flex items-center justify-between p-4 w-40 ">
          <div>
            <RxDashboard className="text-3xl hover:cursor-pointer hover:scale-105 transition-all duration-300" />
          </div>
          <div>
            <h1 className="text-2xl font-bold hover:cursor-pointer ">
              {/* button for source code */}
              GeoAir
            </h1>
          </div>
        </div>

        <div className="flex items-center justify-between p-1 w-[370px]">
          <button className="bg-blue-500 hover:bg-blue-300 text-white font-bold py-2 px-4 rounded-lg">
            <a
              href="https://www.google.ca/"
              target="_blank"
              rel="noopener noreferrer"
            >
              {" "}
              Source Code{" "}
            </a>
          </button>
          <div className="flex justify-between items-center">
            <Image
              src="/images/image.png"
              alt="image1"
              width={50}
              height={50}
              className="m-2"
            />
            <div className="flex flex-col items-center">
              <p>StackOverFlower</p>
              <p className="text-gray-600">Admin</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Navbar;
