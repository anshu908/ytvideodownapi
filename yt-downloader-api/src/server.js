const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());

app.get("/", (req, res) => {
  res.send("Server is running...");
});


app.get("/download", async (req, res) => {
  const url = req.query.url;
  if (!url) return res.status(400).send("URL is required");

  res.send({ message: "Download logic yaha implement karo" });
});

module.exports = app;
