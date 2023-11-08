import Vue from "vue";
import VueRouter from "vue-router";
import { getToken } from "@/utils/auth";

Vue.use(VueRouter);

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
	return originalPush.call(this, location).catch((err) => err);
};

let routes = [
	{
		path: "/",
		name: "index",
		component: () => import("@/views/index.vue"),
		meta: {
			requireAuth: true,
		},
	},
	{
		path: "/login",
		name: "login",
		component: () => import("@/views/login.vue"),
		meta: {
			title: "登录",
		},
	},
	{
		path: "/:bot",
		name: "bot",
		component: () => import("@/views/bot.vue"),
		meta: {
			title: "",
		},
	},
	{
		path: "/*",
		redirect: "/",
	},
];
const router = new VueRouter({
	scrollBehavior: () => ({ y: 0 }),
	routes,
});

router.beforeEach(async (to, from, next) => {
	let token = getToken();
	console.log(token);
	if (to.meta.requireAuth && token == undefined) {
		next({
			path: "/login",
		});
	} else {
		window.document.title =
			to.meta.title == undefined
				? "Pama's GPT"
				: `${to.meta.title} - Pama's GPT`;
		if (to.params.bot != undefined) {
			window.document.title = `${to.params.bot} - Pama's GPT`;
		}
		next();
	}
});

export default router;
