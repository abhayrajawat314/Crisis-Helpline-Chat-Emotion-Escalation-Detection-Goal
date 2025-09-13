import React, { useState, useEffect, useRef } from "react";
import {
    Box,
    Button,
    TextField,
    Typography,
    Paper,
    Grid,
    Divider,
    Container,
    MenuItem
} from "@mui/material";
import { format } from "date-fns";

const WS_URL = "ws://localhost:8000/ws";

function ChatApp() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [speaker, setSpeaker] = useState("user");
    const ws = useRef(null);

    useEffect(() => {
        ws.current = new WebSocket(WS_URL);

        ws.current.onopen = () => console.log("WebSocket connected");
        ws.current.onclose = () => console.log("WebSocket disconnected");

        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMessages((prev) => [
                ...prev,
                { type: "risk_update", data, timestamp: new Date() }
            ]);
        };

        return () => ws.current.close();
    }, []);

    const sendMessage = () => {
        if (input.trim() === "") return;

        const messagePayload = {
            speaker,
            text: input.trim()
        };

        ws.current.send(JSON.stringify(messagePayload));

        setMessages((prev) => [
            ...prev,
            { type: "user_message", data: messagePayload, timestamp: new Date() }
        ]);

        setInput("");
    };

    return (
        <Container maxWidth="sm" sx={{ mt: 5 }}>
            <Typography variant="h4" textAlign="center" gutterBottom>
                Crisis Helpline Chat
            </Typography>

            <Paper elevation={3} sx={{ padding: 2, maxHeight: "500px", overflowY: "auto" }}>
                {messages.map((msg, index) => (
                    <Box key={index} mb={2} p={1}>
                        <Typography variant="caption" color="gray">
                            {format(msg.timestamp, "PPpp")}
                        </Typography>

                        {msg.type === "user_message" && (
                            <Typography>
                                <strong>{msg.data.speaker.toUpperCase()}</strong>: {msg.data.text}
                            </Typography>
                        )}

                        {msg.type === "risk_update" && (
                            <Box sx={{ mt: 1, p: 1, backgroundColor: "#ffe0e0", borderRadius: "5px" }}>
                                <Typography color="error" variant="subtitle1">
                                    ⚠️ Risk Prediction
                                </Typography>
                                <Divider sx={{ mb: 1 }} />
                                <Typography><strong>Risk Level:</strong> {msg.data.risk_level}</Typography>
                                <Typography><strong>Events:</strong> {msg.data.events.join(", ")}</Typography>
                                <Typography><strong>Rationale:</strong> {msg.data.rationale}</Typography>
                            </Box>
                        )}
                    </Box>
                ))}
            </Paper>

            <Box mt={3}>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <TextField
                            label="Enter your message"
                            variant="outlined"
                            fullWidth
                            multiline
                            rows={3}
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                        />
                    </Grid>

                    <Grid item xs={12}>
                        <TextField
                            select
                            label="Speaker"
                            value={speaker}
                            onChange={(e) => setSpeaker(e.target.value)}
                            fullWidth
                        >
                            <MenuItem value="user">User</MenuItem>
                            <MenuItem value="consultant">Consultant</MenuItem>
                        </TextField>
                    </Grid>

                    <Grid item xs={12}>
                        <Button variant="contained" color="primary" fullWidth onClick={sendMessage}>
                            Send
                        </Button>
                    </Grid>
                </Grid>
            </Box>
        </Container>
    );
}

export default ChatApp;
