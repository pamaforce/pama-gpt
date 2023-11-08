/****   request.js   ****/
// 导入axios
import axios from "axios";
// 使用element-ui Message做消息提醒
// import { getToken } from "@/utils/auth";
// import { Message } from "element-ui";
// //1. 创建新的axios实例，
// import NProgress from "nprogress";
// import "nprogress/nprogress.css";
// import router from '../router'
const service = axios.create({
	baseURL: "http://127.0.0.1:5000/",
});
// 2.请求拦截器
//
// service.interceptors.request.use(
//     config => {
//         // do something before request is sent
//         NProgress.start();
//         //发请求前做的一些处理，数据转化，配置请求头，设置token,设置loading等，根据需求去添加
//         // config.data = JSON.stringify(config.data); //数据转化,也可以使用qs转换
//         config.headers.Authorization = getToken();

//         return config;
//     },
//     error => {
//         console.log(error);
//         Promise.reject(error);
//     }
// );

//3.响应拦截器
service.interceptors.response.use(
	(response) => {
		const res = response.data;
		return res;
	},
	(error) => {
		return Promise.reject(error);
	}
);
//4.导入文件
export default service;
