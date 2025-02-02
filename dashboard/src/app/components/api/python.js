// export default async function handler(req, res) {
//   try {
//     const response = await fetch("http://localhost:5004/api/data"); // Fetch from Flask server
//     const data = await response.json();
//     res.status(200).json(data); // Forward response to frontend
//   } catch (error) {
//     res.status(500).json({ error: "Failed to fetch data" });
//   }
// }
