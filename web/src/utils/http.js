/****   http.js   ****/
// 导入封装好的axios实例
import request from "./request";
import { getToken } from "./auth";

const http = {
	/**
	 * methods: 请求
	 * @param url 请求地址
	 * @param params 请求参数
	 */
	get(url, params) {
		const config = {
			method: "get",
			url: url,
		};
		config.headers = {
			"Content-Type": "application/json", //配置请求头
			Authorization: "Bearer " + getToken(),
		};
		if (params) config.params = params;
		return request(config);
	},
	post(url, params) {
		const config = {
			method: "post",
			url: url,
		};
		config.headers = {
			"Content-Type": "application/x-www-form-urlencoded", //配置请求头
			Authorization: "Bearer " + getToken(),
		};
		if (params) config.data = params;

		return request(config);
	},
	postFormData(url, params, headers) {
		const config = {
			method: "post",
			url: url,
		};
		config.headers = headers;
		if (params) config.data = params;

		return request(config);
	},
	put(url, params) {
		const config = {
			method: "put",
			url: url,
		};
		config.headers = {
			"Content-Type": "application/json", //配置请求头
			Authorization: "Bearer " + getToken(),
		};
		if (params) config.params = params;
		return request(config);
	},
	delete(url, params) {
		const config = {
			method: "delete",
			url: url,
		};
		config.headers = {
			"Content-Type": "application/json", //配置请求头
			Authorization: "Bearer " + getToken(),
		};
		if (params) config.params = params;
		return request(config);
	},
};
//导出
export default http;
