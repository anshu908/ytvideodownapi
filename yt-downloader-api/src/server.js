const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());

app.use("/download", require("./routes/download"));
app.use("/info", require("./routes/info"));

module.exports = app;  // Vercel ke liye ye zaroori hai
