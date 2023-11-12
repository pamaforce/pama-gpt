import http from "../utils/http";

export function login(params) {
	return http.post(`/login`, params);
}

export function getChatHistory(bot) {
	return http.get(`/chat_history?bot=${bot}`);
}

export function getBots() {
	return http.get(`/bots?category=Official`);
}

export function updateChatId(params) {
	return http.post(`/update_chat_id`, params);
}
