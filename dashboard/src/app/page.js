// pages/index.js
import MapWrapper from "./components/MapWrapper";
import Navbar from "./components/Navbar";
import BaseStats from "./components/BaseStats";
import Diagram from "./components/Diagram";
import Test from "./components/test";

export default function Home() {
  return (
    <div className="bg-gray-200">
      <Navbar />
      <Test />
      <Diagram />
    </div>
  );
}
