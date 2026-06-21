import express from "express";
import { Ollama } from "ollama";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

const ollama = new Ollama();

app.post("/", async (req, res) => {
    res.type("text/plain");

    const body = req.body;

    const response = await ollama.chat({
        model: "llama3.2",
        messages: [ { role: "user", content: body.question }],
        stream: true,
    });

    for await (const part of response) {
        res.write(part.message.content);
        console.log(part);
    }
    res.end();
});

app.listen(8000, () => {
    console.log("Server is running on http://localhost:8000");
});