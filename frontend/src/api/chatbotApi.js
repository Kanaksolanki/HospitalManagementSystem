import axiosClient from "./axiosClient";

export const sendChatMessage = (message) => axiosClient.post("/chatbot/", { message });