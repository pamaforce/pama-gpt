import http from "../utils/http";

export function login(params) {
	return http.post(`/login`, params);
}

export function getSessions() {
	return http.get(`/sessions`);
}

export function getBots() {
	return http.get(`/bots?category=Official`);
}
