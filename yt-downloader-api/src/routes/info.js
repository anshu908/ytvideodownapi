const express = require("express");
const fetchVideo = require("../utils/fetchVideo");
const router = express.Router();

router.get("/", async (req, res) => {
    const { url } = req.query;
    if (!url) return res.status(400).json({ error: "URL is required" });

    try {
        res.json(await fetchVideo(url));
    } catch (error) {
        res.status(500).json({ error: "Failed to fetch info" });
    }
});

module.exports = router;
