import Cookies from "js-cookie";

const TokenKey = "pama_gpt_data_";

export function getData(key) {
	return JSON.parse(Cookies.get(TokenKey + key) || "{}");
}

export function setData(key, data) {
	return Cookies.set(TokenKey + key, JSON.stringify(data));
}

export function setLargeData(key, data) {
	return window.localStorage.setItem(TokenKey + key, JSON.stringify(data));
}
export function getLargeData(key) {
	return JSON.parse(window.localStorage.getItem(TokenKey + key) || "{}");
}
